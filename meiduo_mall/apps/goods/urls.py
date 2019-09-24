from django.conf.urls import url, include
from django.contrib import admin

from apps.goods import views

urlpatterns = [

    # list/(?P<category_id>\d+)/(?P<page_num>\d+)/?sort=排序方式
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view(), name='list'),

    # 热销排行 hot/(?P<category_id>\d+)/
    # url(r'^hot/(?P<category_id>\d+)/$', views.HotView.as_view(), name='list'),
    url(r'^hot/(?P<category_id>\d+)/$', views.HotView.as_view(), name='list'),

    url(r'^detail/(?P<sku_id>\d+)/$', views.DetailView.as_view(), name='detail'),

    #统计分类商品访问量
    url(r'^detail/visit/(?P<category_id>\d+)/$', views.DetailVisitView.as_view(), name='detailvisit'),

]
