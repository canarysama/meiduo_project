import os

from alipay import AliPay
from django import http
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.orders.models import OrderInfo
from apps.payment.models import Payment
from utils.response_code import RETCODE

class PaySucessView(View):
    def get(self,request):

        params_query = request.GET
        data = params_query.dict()


        singnature = data.pop('sign')

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url

            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem'),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                'keys/alipay_public_key.pem'),

            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG,

        )

        sucess = alipay.verify(data,singnature)

        if sucess:
            order_id = data.get('out_trade_no')
            trade_id = data.get('trade_no')

            Payment.objects.create(

                order_id = order_id,
                trade_id = trade_id
            )

            OrderInfo.objects.filter(order_id=order_id, status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(

            status = OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT']
        )
            context = {
                'trade_id':trade_id
            }

        else:
            context = {
                'trade_id':'支付失败'
            }

        return render(request,'pay_success.html',context)







class PaymentView(View):
    def get(self,request,order_id):
        user = request.user

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单信息错误')

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url

            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'keys/app_private_key.pem'),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'keys/alipay_public_key.pem'),


            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        order_str =  alipay.api_alipay_trade_page_pay(
        subject = '美多商城%s' % order_id,
        out_trade_no = order_id,
        total_amount =str(order.total_amount) ,
        return_url = settings.ALIPAY_RETURN_URL,

        )


        alipay_url = settings.ALIPAY_URL +"?"+ order_str

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})
