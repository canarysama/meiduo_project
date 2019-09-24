import json

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
from meiduo_mall.cookiesecret import CookieSecret
from utils.response_code import RETCODE

#购物车____
class CartsView(View):
    def post(self,request):

        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected',True)

        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.HttpResponseForbidden("商品不村咋")

        try:
            count = int(count)
        except:
            return http.HttpResponseForbidden('COUNT不是整形')

        if selected:
            if not isinstance(selected,bool):
                return http.HttpResponseForbidden('selected不是bool类型')

        user = request.user

        response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加购物车成功'})


        if user.is_authenticated:
            redis_carts_client = get_redis_connection('carts')

            client_data = redis_carts_client.hgetall(user.id)


            # print('哦按段之前',client_data)

            if str(sku_id).encode() in client_data:
                # print(client_data)
                bytes_carts = client_data[str(sku_id).encode()]
                str_carts = bytes_carts.decode()
                dict_carts = json.loads(str_carts)
                dict_carts['count'] += count

                redis_carts_client.hset(user.id,sku_id,json.dumps(dict_carts))


            else:
                redis_carts_client.hset(user.id,sku_id,json.dumps({'count':count,"selected":selected}))


        else:
            #weidenglu

            #获取cookie中所有的数据

            cookie_str = request.COOKIES.get('carts')

            if cookie_str:
                carts_dict = CookieSecret.loads(cookie_str)
            else:
                carts_dict = {}
            #解密
            # carts_dict = CookieSecret.loads(cookie_str)

            # 判断是否存在
            if sku_id in carts_dict:
                # carts_dict[sku_id]['count'] += count

                origi_count = carts_dict[sku_id]['count']
                count += origi_count

            carts_dict[sku_id] = {
                    'count':count,
                    'selected':selected
                }

            dumps_str = CookieSecret.dumps(carts_dict)

            response.set_cookie('carts',dumps_str,max_age=14*24*3600)

            #存在 累加
            # 不存在新增

        return response

    def get(self,request):

        user = request.user
        if user.is_authenticated:
            carts_dict = {}

            client  = get_redis_connection('carts')

            carts_redis = client.hgetall(user.id)
            carts_dict = {}

            for key,value in carts_redis.items():
                cart_key = int(key.decode())
                carts_redis_dict = json.loads(value.decode())
                carts_dict[cart_key] = carts_redis_dict

            # carts_dict = {int(key.decode()):json.loads(value.decode()) for key,value in carts_redis.items() }

        else:
            pass
            cookie_str = request.COOKIES.get('carts')

            if cookie_str:
                carts_dict = CookieSecret.loads(cookie_str)
            else:
                carts_dict = {}


        sku_ids = carts_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        cart_skus = []

        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': carts_dict.get(sku.id).get('count'),
                'selected': str(carts_dict.get(sku.id).get('selected')),  # 将True，转'True'，方便json解析
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount': str(sku.price * carts_dict.get(sku.id).get('count')),

            })
        context = {
            'cart_skus':cart_skus,
        }
        print(context)
        return render(request,'cart.html',context)

    def put(self,request):
        #收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected',True)

        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return  http.HttpResponseForbidden('商品不存在')

        user = request.user
        dumps_dict_str =''
        if user.is_authenticated:
          redis_client = get_redis_connection('carts')

          new_data = {'count':count,'selected':selected}

          redis_client.hset(user.id,sku_id,json.dumps(new_data))


        else:
            cart_str = request.COOKIES.get('carts')

            if cart_str:
                cart_dict = CookieSecret.loads(cart_str)

            else:
                cart_dict = {}
            cart_dict[sku_id] = {

                'count':count,
                'selected':selected,

            }

            dumps_dict_str = CookieSecret.dumps(cart_dict)




        cart_sku = {
            'id': sku_id,
            'count': count,
            'selected': selected,
            'name': sku.name,
            'default_image_url': sku.default_image.url,
            'price': sku.price,
            'amount': str(sku.price * count),
        }
        response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改购物车成功', 'cart_sku': cart_sku})

        if not user.is_authenticated:
            response.set_cookie('carts',dumps_dict_str)
        return response

    def delete(self,request):
       #接收参数

        sku_id = json.loads(request.body.decode()).get('sku_id')

        try:
            sku = SKU.objects.get(id= sku_id)
        except Exception as e:
            return http.HttpResponseForbidden('商品不存在')

        user = request.user

        response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除购物车成功'})

        if user.is_authenticated:
            redis_client = get_redis_connection('carts')
            redis_client.hdel(user.id, sku_id)
            return response
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str is not  None:
                cart_dict = CookieSecret.loads(cart_str)

                if sku_id in cart_dict:
                    del cart_dict[sku_id]

                    cart_str_dumps = CookieSecret.dumps(cart_dict)

                    response.set_cookie('carts',cart_str_dumps,max_age=24 * 30 * 3600)
            return response
            pass

class CartsSelectAllView(View):
    def put(self,request):

        selected = json.loads(request.body.decode()).get('selected')

        if selected:
            if not isinstance(selected,bool):
                return http.HttpResponseForbidden('参数类型有误')

        user = request.user

        repsonse = http.JsonResponse({'code': RETCODE.OK, 'errmsg': '全选购物车成功'})

        if user.is_authenticated:
            redis_client = get_redis_connection('carts')

            carts_dict = redis_client.hgetall(user.id)

            for key,value in carts_dict.items():
                sku_id = int(key.decode())
                sku_dict = json.loads(carts_dict[key].decode())

                #全选
                sku_dict['selected'] = selected

                redis_client.hset(user.id,sku_id,json.dumps(sku_dict))



        else:

            carts_str = request.COOKIES.get('carts')

            if carts_str:
                carts_dict = CookieSecret.loads(carts_str)

                for key in carts_dict:

                    carts_dict[key]['selected'] = selected

                dumps_carts_str = CookieSecret.dumps(carts_dict)

                repsonse.set_cookie('carts',dumps_carts_str,max_age=12*24*3600)

        return repsonse

class CartsSimpleView(View):
    def get(self,request):
        if request.user.is_authenticated:

            redis_client = get_redis_connection('carts')

            carts_data = redis_client.hgetall(request.user.id)

            # for key,value in carts_data.itams():
            #
            #     key = int(key.decode())
            #     value = json.loads(value.decode())
            #     carts_dict[key] = value
            #
            cart_dict = {int(key.decode()): json.loads(value.decode()) for key,value in carts_data.items()}

        else:
            cookie_str = request.COOKIES.get('carts')

            if cookie_str:
                carts_dict = CookieSecret.loads(cookie_str)
            else:
                carts_dict = {}
            skus = SKU.objects.filter(id__in = carts_dict.keys())

            skus_list = []

            for sku in skus:
                skus_list.append({
                    'id': sku.id,
                    'name': sku.name,
                    'count': carts_dict.get(sku.id).get('count'),
                    'default_image_url': sku.default_image.url



                })
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'cart_skus': cart_skus})
