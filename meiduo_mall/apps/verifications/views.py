from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from django import http

from apps.verifications import constants


class ImageCodeView(View):
    def get(self,request,uuid):
        #接收参数


        #校验正则 uuid

        #生成图形验证码
        from libs.captcha.captcha import captcha
        text,image_code = captcha.generate_captcha()


        #保存到redis中,为后面发送短信验证码做准备
        image_client = get_redis_connection('verify_image_code')

        image_client.setex("img_%s" %uuid,constants.IMAGE_CODE_REDIS_EXPIRES,text)

        #返回响应对象
        from django.http import HttpResponse, response
        return http.HttpResponse(image_code,content_type='image/jpg')

#校验图形验证码发短信
class SMSCodeView(View):
    def get(self,request,mobile):
        #接收参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        image_client = get_redis_connection('verify_image_code')
        redis_img_code = image_client.get('img_%s'%uuid)

        if not redis_img_code:
            return http.JsonResponse({'code':"4001",'errmsg':"验证码失效了"})

        image_client.delete('img_%s'%uuid)

        if image_code != redis_img_code.decode().lower():
            return http.JsonResponse({'code':"4001",'errmsg':"验证有误"})

        #对比图形验证码





        return http.JsonResponse({'code':'0','errmsg':'发送成功'})