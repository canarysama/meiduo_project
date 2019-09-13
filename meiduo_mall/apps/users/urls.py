from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^', views.test.as_view),

]
