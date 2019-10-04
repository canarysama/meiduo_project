from django.conf.urls import url, include
# from django.contrib import admin

from apps.orders import views

urlpatterns = [
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view()),


    url(r'^orders/commit/$', views.OrderCommitView.as_view()),

    url(r'^orders/success/$', views.OrderSuccessView.as_view()),

    url(r'^orders/info/(?P<page_num>\d+)/$', views.OrderShowView.as_view(),name='order_all'),
#                      (?P<mobile>[a-zA-Z0-9_-]{5,20})

]
