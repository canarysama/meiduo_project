from django.conf.urls import url
from django.contrib import admin

from apps.areas import views

urlpatterns = [
    url(r'^areas/', views.AreasView.as_view()),


]
