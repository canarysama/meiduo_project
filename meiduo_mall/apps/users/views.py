from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse

class RegisterView(View):
    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        # return HttpResponse('haha')
        return render(request, 'register.html')