from django import views
from django.conf.urls import url, include
from django.contrib import admin
from apps.carts import views
urlpatterns = [



    url('^carts/$', views.CartsView.as_view(),name='carts'),

    url('^carts/selection/$', views.CartsSelectAllView.as_view(),name='cartss'),

    url('^carts/simple/$', views.CartsSimpleView.as_view(),name='cartss'),

]
