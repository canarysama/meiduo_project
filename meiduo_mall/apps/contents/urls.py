from django.conf.urls import url, include
from django.contrib import admin

from apps.contents import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='index'),

]