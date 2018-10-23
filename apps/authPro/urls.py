from django.shortcuts import render
from django.urls import path
from . import views
app_name = 'authPro'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('graph_captcach/',views.captcha_view,name='captcach'),
    path('send_sms/',views.send_sms_captcha_view,name='sendsms'),
]