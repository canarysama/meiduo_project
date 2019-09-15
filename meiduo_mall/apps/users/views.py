import re
from audioop import reverse

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.http import HttpResponse, response
from django import http

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


        # 3.保持登录状态


        # 4.重定向
        return redirect('/')


class LoginView(View):
    def get(self,request):



        return render(request, 'login.html')

    def post(self,requset):
        username = requset.POST.get('uesrname')
        password = requset.POST.get('password')
        remembered = requset.POST.get('remembered')


        user = authenticate(username=username,password=password,)

        # user 不存在登失败
        if user is None:
            return  render(requset,'login.html')
        login(requset,user)

        if remembered != 'on':
            requset.session.set_expiry(0)
        else:
            requset.session.set_expiry(None)

        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)


        return redirect(reverse('contents:index'))
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

from django.contrib.auth.mixins import LoginRequiredMixin

class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        return render(request, 'user_center_info.html')