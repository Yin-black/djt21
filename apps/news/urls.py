from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('',views.NewsView.as_view(),name='index'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('news/detail/<int:tag_id>/',views.NewsDtailView.as_view(),name='dtail'),
    path('news/add_content/',views.AddNewsContentView.as_view(),name='content'),
    path('news/list/',views.newslis_view,name='news_list'),
    path('news/content/',views.GetNewsContentView.as_view(),name='getcontent'),
]