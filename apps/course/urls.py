from django.shortcuts import render
from django.urls import path
from . import views
app_name = 'course'

urlpatterns = [
    path('course/',views.Courseview.as_view(),name='course'),
    path('course-token/',views.course_token,name='course_token'),
    path('course/detail/<int:id>/',views.CourseDetalView.as_view(),name='coursedetail'),
]