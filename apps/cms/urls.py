from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('new_tag_manage/',views.TagManageView.as_view(),name='tag_manage'),
    path('pub_news/',views.PubNews.as_view(),name='pubnews'),
    path('upload_qiniu/',views.Upload_Qiniu.as_view(),name='upload_qiniu'),
    path('upload-server/',views.Upload_server.as_view(),name='upload_server'),
    path('news_manage/',views.NewsManage.as_view(),name='news_manage'),
]