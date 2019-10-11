from django.conf.urls import url
from django.contrib import admin

from apps.goods import views

urlpatterns = [


    #统计分类商品访问量
    url(r'^detail/visit/(?P<category_id>\d+)/$', views.DetailVisitView.as_view(), name='detailvisit'),

]
