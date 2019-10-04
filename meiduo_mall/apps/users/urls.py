from django.conf.urls import url, include
from django.contrib import admin

from apps.users import views

urlpatterns = [

    url(r'^register/', views.RegisterView.as_view(),name='register'),

    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),

    url(r'^mobiles/(?P<mobile>1[345789]\d{9})/count/$', views.MobileCountView.as_view()),

    url(r'^login/$',views.LoginView.as_view(),name='login'),

    url(r'^logout/$',views.LogoutView.as_view(),name='logout'),

    url(r'^info/$',views.UserInfoView.as_view(),name='userinfo'),

    url(r'^emails/$',views.EmailView.as_view(),name='email'),


    url(r'^address/$',views.AddressView.as_view(),name='address'),


    url(r'^addresses/create/$',views.AddressAddView.as_view(),name='addressadd'),

    url(r'^password/$',views.ChangPwdAddView.as_view()),


    url(r'^browse_histories/$',views.BrowseHistoriesView.as_view()),

    url(r'^find_password/$',views.FindPasswordView.as_view()),

    url(r'^accounts/(?P<username>[a-zA-Z0-9_-]{5,20})/sms/token/$',views.PasswordOneView.as_view()),

    url(r'^find_password_sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.PasswordTwoView.as_view()),

    url(r'^users/(?P<user_id>\d+)/new_password/$',views.PasswordThreeView.as_view()),


    url(r'^accounts/(?P<mobile>[a-zA-Z0-9_-]{5,20})/password/token/$',views.SmsView.as_view(),),





]
