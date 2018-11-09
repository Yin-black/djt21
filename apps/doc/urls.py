from django.shortcuts import render
from django.urls import path
from . import views
app_name = 'doc'

urlpatterns = [
    path('download/',views.DocDownLoadView.as_view(),name='docdownload'),
    path('doc_download/',views.doc_download,name='download'),
]