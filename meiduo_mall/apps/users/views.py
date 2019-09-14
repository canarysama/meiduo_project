from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse
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


