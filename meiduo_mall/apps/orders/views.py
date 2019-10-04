import json
from datetime import datetime

from decimal import Decimal

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
from apps.orders.models import OrderInfo, OrderGoods
from apps.users.models import Address, User
from meiduo_mall.settings.dev import logger
from utils.response_code import RETCODE


class OrderSettlementView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        try:
            addresses = Address.objects.filter(user=user,is_deleted=False)

        except Exception as e:
            addresses = None

        redis_client = get_redis_connection('carts')
        carts_data = redis_client.hgetall(user.id)

        carts_dict = {}

        for key,value in carts_data.items():
            sku_key = int(key.decode())
            sku_dict = json.loads(value.decode())
            if sku_dict["selected"]:
                carts_dict[sku_key] = sku_dict

        skus = SKU.objects.filter(id__in = carts_dict.keys())

        total_count = 0
        total_amount = Decimal('0.00')
        for sku in skus:
            sku.count = carts_dict[sku.id]['count']
            sku.amount = sku.price * sku.count
            total_count += sku.count
            total_amount += sku.price * sku.count

        freight = Decimal('10.00')

        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight,
            'default_address_id': user.default_address_id
        }
        return render(request, 'place_order.html', context)


class OrderCommitView(LoginRequiredMixin,View):
    def post(self,request):
        #接收参数
        json_dict = json.loads(request.body.decode())
        address_id = json.loads(request.body.decode())['address_id']
        pay_method = json.loads(request.body.decode())['pay_method']
        user = request.user
        #效验
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return http.HttpResponseForbidden('WUXIAO')

        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'],OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return http.HttpResponseForbidden('不支持')

        #订单表__生成订单号 时间戳+9为
        # user = request.user

        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

        #事务
        from django.db import transaction
        with transaction.atomic():
            # --------事物保存点--------
            save_id = transaction.savepoint()
            try:
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user = user,
                    address = address,
                    total_count = 0,
                    total_amount = Decimal('0.00'),
                    freight = Decimal("10.00"),
                    pay_method = pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )

                redis_client = get_redis_connection('carts')
                carts_data = redis_client.hgetall(user.id)
                carts_dict = {}
                for key,value in carts_data.items():
                    sku_id = int(key.decode())
                    sku_dict = json.loads(value.decode())
                    if sku_dict['selected']:
                        carts_dict[sku_id] = sku_dict

                sku_ids = carts_dict.keys()
                for sku_id in sku_ids:
                    while True:
                        sku = SKU.objects.get(id=sku_id)

                        # sku.stock -= cart_count
                        # sku.sales += cart_count
                        # sku.sava()

                        original_stock = sku.stock

                        original_sales = sku.sales



                        #判断库存
                        cart_count = carts_dict[sku_id]['count']
                        if cart_count > sku.stock:

                            transaction.savepoint_rollback(save_id)

                            return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

                        import time
                        # time.sleep(10)

                        new_stock = original_stock - cart_count
                        new_sales = original_sales + cart_count

                        result = SKU.objects.filter(id=sku_id, stock=original_stock).update(stock=new_stock,sales=new_sales)

                        if result == 0:
                            continue


                        sku.stock -= cart_count
                        sku.sales += cart_count
                        sku.save()

                        sku.spu.sales += cart_count
                        sku.spu.save()



                        # 创建订单商品数据
                        OrderGoods.objects.create(
                            order_id = order_id,
                            sku = sku,
                            count = cart_count,
                            price = sku.price,
                        )

                        #总个数和总金额(没运费)
                        order.total_count += cart_count
                        order.total_amount += sku.price * cart_count

                        #下单成功或者失败退出
                        break

                    #加运费 总金额
                order.total_amount += order.freight

                order.save()
            except Exception as e :
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

            transaction.savepoint_commit(save_id)

            #清空购物车
            # redis_client.hdel(user.id, *carts_dict)


            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})


class OrderSuccessView(View):
    def get(self,request):

        order_id = request.GET.get("order_id")
        pay_method = request.GET.get("pay_method")
        payment_amount = request.GET.get("payment_amount")

        context={
            "order_id":order_id,
            "pay_method":pay_method,
            "payment_amount":payment_amount,
        }

        return render(request,'order_success.html',context)

class OrderShowView(LoginRequiredMixin,View):
    def get(self,request,page_num):

        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)
        user_id = user.id

        order_data = OrderInfo.objects.all()
        goods_data = OrderGoods.objects.all()

        order_ids = order_data.filter(user_id=user_id).values('order_id')

        # order_ids = OrderInfo.objects.filter(user_id=user_id)

        page_orders = {}

        for order_id in order_ids:

            order_id = order_id['order_id']  # 订单号
            time_old = order_data.filter(order_id=order_id).values('create_time')    #  时间
            time = str(time_old[0]['create_time'])
            print(goods_data.values())
            time_new = time[0:16] # 时间
            freight = time_old.values('freight')[0]['freight'] # 运费


            """<QuerySet [{'address_id': 1, 'user_id': 19, 'total_count': 1,
            'order_id': '20190927003440000000019',
             'status': 1, 'pay_method': 2,
             'create_time': datetime.datetime(2019, 9, 27, 0, 34, 40, 214624, tzinfo=<UTC>),
             'update_time': datetime.datetime(2019, 9, 27, 0, 34, 40, 235034, tzinfo=<UTC>),
             'freight': Decimal('10.00'), 'total_amount': Decimal('6698.00')}]>
            """

            # if total_amount-freight == 0.00 or total_amount == 0.00:
            #     continue
            #
            # page_orders = {}
            # for Goods in goods_data:
            #     page_orders.setdefault(order_id,[time,freight,]).append(Goods)



        page_num = 1
        """
        下单时间 订单号
        商品信息 数量 单价 总价 运费  支付方式 订单状态 """

        context = {

             "page_orders": page_orders,
        # #     # 总页数
        # #     'total_page': total_page,
        # #     # 当前页
              'page_num': page_num,
        }

        return render(request,'user_center_order.html',context)


