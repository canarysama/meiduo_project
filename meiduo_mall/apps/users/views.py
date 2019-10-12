import base64
import json
import os
import re

from django.contrib.auth import authenticate, login, logout
# from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, response
from django import http
from django_redis import get_redis_connection

from apps.goods.models import SKU
from apps.users.models import User, Address
from apps.verifications import constants
from utils.response_code import RETCODE
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# 忘记密码
from utils.secret import SecretOauth


class FindPasswordView(View):
    def get(self,request):
        return render(request,'find_password.html')

class PasswordOneView(View):
    def get(self, request, username):

        image_code = request.GET.get('image_code')
        image_code_id = request.GET.get('image_code_id')

        image_client = get_redis_connection('verify_image_code')

        image_code_data = image_client.get("img_%s"%image_code_id)

        # print(image_code.lower())
        # print(image_code_data.decode().lower())

        token_str = bytes.decode(base64.b64encode(os.urandom(48)))


        try:
            user = User.objects.get(username=username)
            mobile = user.mobile

            if image_code.lower() == image_code_data.decode().lower():

                image_client.setex('token_%s'% mobile,constants.IMAGE_CODE_REDIS_EXPIRES,token_str)

                from utils.secret import SecretOauth
                token_str_go = SecretOauth().dumps(token_str)

                return http.JsonResponse({"status": 5000, "mobile": mobile, "access_token": token_str_go})
            else:
                return http.JsonResponse({"status": 5001,})

        except:
            #5004 用户名或手机号不存在
            return http.JsonResponse({"status": 5004,})

class PasswordTwoView(View):
     def get(self,request,mobile):


        access_token = SecretOauth().loads(request.GET.get('access_token'))

        redis_client  =  get_redis_connection('verify_image_code')

        access_token_redis = redis_client.get('token_%s'% mobile).decode()
        # loads_acces_token = SecretOauth().loads(access_token)

        if access_token == access_token_redis:


            return http.JsonResponse({"status": 5000,'message': "短信发送成功!"} )

        else:

            return http.JsonResponse({"status": 5001,'message': "token有误"})


class SmsView(View):
    def get(self,request,mobile):

        one_sms_code = request.GET.get('sms_code')

        user = User.objects.get(mobile=mobile)

        token_data = get_redis_connection('verify_image_code')

        token_str = token_data.get('token_%s'% mobile).decode()

        from random import randint
        sms_code = '06%d'%randint(0,999999)
        sms_code_redis = get_redis_connection('sms_code')
        sms_code_redis.setex('sms_%s' % mobile, 300, sms_code)
        redis_sms = sms_code_redis.get('sms_%s'%mobile)
        print(sms_code)

        if one_sms_code != redis_sms.decode():
            return http.JsonResponse({
                "status": 5001,})
        return http.JsonResponse({
            "status": 5000,
            "user_id": user.id,
            "access_token":token_str})



class PasswordThreeView(View):



    def post(self,request,user_id ):
        user_dict = request.body.decode()

        try:
            user = User.objects.get(id=user_id)
            mobile = user.mobile
        except:
            return http.JsonResponse({  "status": 5002, 'message': "user_id有误!" })
        token_data = get_redis_connection('verify_image_code')
        token_str = token_data.get('token_%s'% mobile)
        user_dict = eval(user_dict)

        if user_dict['access_token'] == token_str.decode():
            if user_dict['password'] == user_dict['password2']:

                password2 = user_dict['password2']
                print(password2)

                user.set_password(password2)
                user.save()


                return http.JsonResponse({"status": 5000, 'message': "成功!"})

        else:
            return http.JsonResponse({"status": 5001, 'message': "token有误!"})

class BrowseHistoriesView(View):

    def post(self,request):
        sku_id = json.loads(request.body.decode())['sku_id']

        try:
            sku = SKU.objects.get(id = sku_id)
        except:
            return http.HttpResponseForbidden('商品不存在')
        client = get_redis_connection('history')
        redis_key = 'history_%d' % request.user.id

        client.lrem(redis_key,0,sku_id)
        client.lpush(redis_key,sku_id)

        client.ltrim(redis_key,0,4)

        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

    def get(self,request):
        client = get_redis_connection('history')

        sku_ids = client.lrange('history_%d'%request.user.id,0,-1)

        # for sku_id in sku_ids:
        #     sku =SKU.objects.filter(id__in = sku_ids)
        #
        sku_list =[]
        for sku_id in sku_ids:
            sku = SKU.objects.get(id=sku_id)
            sku_list.append({

                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':sku.default_image.url
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'skus': sku_list})

#修改密码
class ChangPwdAddView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'user_center_pass.html')
    def post(self,request):

        old_password = request.POST.get('old_pwd')
        new_password = request.POST.get('new_pwd')
        newcp_password = request.POST.get('new_cpwd')

        user = request.user


        if not user.check_password(old_password):
            return render(request,'user_center_pass.html')
        user.set_password(new_password)
        user.save()

        response = redirect(reverse('users:login'))

        logout(request,user)

        response.delete_cookie('username')

        return response

#增加收货地址
class AddressAddView(LoginRequiredMixin,View):
    def post(self,request):

        count = Address.objects.filter(user = request.user,is_deleted=False).count()
        if count >  20:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})




        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        #校验判空和正则


        address = Address.objects.create(
            user=request.user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email,
        )
        if not request.user.default_address:
            request.user.default_address = address
            request.user.save()
        # 新增地址成功，将新增的地址响应给前端实现局部刷新
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email,
        }

        # 响应保存结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address_dict})


#展示收获地址
class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址界面"""
        # 获取用户地址列表
        login_user = request.user
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)

        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_dict_list,
        }

        return render(request, 'user_center_site.html', context)

class EmailView(LoginRequiredMixin,View):
    def put(self,request):
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')
        try:
            request.user.email = email
            request.user.save()
        except:
            print()

        #发邮件
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})

#用户中心
class UserInfoView(LoginRequiredMixin,View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }
        return render(request, 'user_center_info.html', context=context)


#用户名重复检测
class UsernameCountView(View):
    def get(self,rquest,username):
        # 接收参数


        #校验

        #业务逻辑判断
        count = User.objects.filter(username=username).count()

        #返回响应对象
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})

#手机号重复检测
class MobileCountView(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()

        return http.JsonResponse({'count': count})

class RegisterView(View):
    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        #1.接收参数

        # return HttpResponse('haha')
        return render(request, 'register.html')


    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code = request.POST.get('msg_code')

        allow = request.POST.get('allow')

        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden("缺少必备参数")

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')

        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return http.HttpResponseForbidden('请输入8-20位de的密码')

        if password != password2:
            return http.HttpResponseForbidden('请再次输入密码')

        if not re.match(r'^1[345789]\d{9}$',mobile):
            return http.HttpResponseForbidden('请输入正确的手机号')

        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')


        # 3.注册
        user = User.objects.create_user(username=username,password=password,mobile=mobile),

        # 3.保持登录状态
        login(request,user)
        response = redirect(reverse("contents:index"))
        response.set_cookie('username',username,max_age=3600 * 24 * 15)

        sms_code_redis = get_redis_connection('sms_code')
        x_sms_code = sms_code_redis.get('sms_%s'%mobile)
        if x_sms_code != sms_code:
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})
        return response
        # return HttpResponse("首页")

class LoginView(View):
    def get(self,request):



        return render(request, 'login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # print("-----",username)
        user = authenticate(request,username=username, password=password)
        # print("----",username)

        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        # 4.保持登录状态
        login(request, user)



        # 5.是否记住用户名
        if remembered != 'on':
            # 不记住用户名, 浏览器结束会话就过期
            request.session.set_expiry(0)
        else:
            # 记住用户名, 浏览器会话保持两周
            request.session.set_expiry(None)

        # 6.返回响应结果
        response =  redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        from apps.carts.utils import merge_cart_cookie_to_redis
        merge_cart_cookie_to_redis(request=request, response=response)

        return response

class LogoutView(View):
        """退出登录"""

        def get(self, request):
            """实现退出登录逻辑"""
            # 清理session
            logout(request)
            # 退出登录，重定向到登录页
            response = redirect(reverse('contents:index'))
            # 退出登录时清除cookie中的username
            response.delete_cookie('username')

            return response
