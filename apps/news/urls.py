from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('',views.NewsView.as_view(),name='index'),
    path('search/',views.search,name='search'),
    path('news/detail/<int:tag_id>/',views.NewsDtailView.as_view(),name='dtail'),
    path('news/add_content/',views.AddNewsContentView.as_view(),name='content'),
    path('news/list/',views.newslis_view,name='news_list'),
    path('news/content/',views.GetNewsContentView.as_view(),name='getcontent'),
    path('news/hot/list/',views.news_hot_list,name='news_hot_list'),
    path('news/tag/list/',views.news_tag_list,name='news_tag_list'),
    path('news/news-with-tag/',views.news_with_tag,name='news_with_tag'),
]