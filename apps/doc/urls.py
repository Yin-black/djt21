from django.shortcuts import render
from django.urls import path
from . import views
app_name = 'doc'

urlpatterns = [
    path('download/',views.DocDownloadView.as_view(),name='docdownload'),
]