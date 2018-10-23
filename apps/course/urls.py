from django.shortcuts import render
from django.urls import path
from . import views
app_name = 'course'

urlpatterns = [
    path('course/',views.Courseview.as_view(),name='course'),
]