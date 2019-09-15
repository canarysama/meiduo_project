from django.conf.urls import url, include
from django.contrib import admin

from apps.users import views

urlpatterns = [

    url(r'^register/', views.RegisterView.as_view(),name='register'),

    url(r'login/$',views.LoginView.as_view(),name='login'),

    url(r'logout/',views.LogoutView.as_view(),name='login'),

    url(r'userinfo/',views.UserInfoView.as_view(),name='userinfo'),

]
