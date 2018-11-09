from django.urls import path
from . import views,course_views,doc_views,staff_views

app_name = 'cms'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('new_tag_manage/',views.TagManageView.as_view(),name='tag_manage'),
    path('pub_news/',views.PubNews.as_view(),name='pubnews'),
    path('news_edit/',views.NewsEidtView.as_view(),name='news_edit'),
    path('upload_qiniu/',views.Upload_Qiniu.as_view(),name='upload_qiniu'),
    path('upload-server/',views.Upload_server.as_view(),name='upload_server'),
    path('news_manage/',views.NewsManage.as_view(),name='news_manage'),
    path('news/hot/',views.NewsHotView.as_view(),name='news_hot'),
    path('news/hot/add/',views.NewsHotAddView.as_view(),name='news_hot_add'),
]

#banner管理url
urlpatterns += [
    path('news/banner/list/',views.news_banner_list,name = 'news_banner_list'),
    path('news/banner/',views.NewsBannerView.as_view(),name = 'news_banner'),
    path('news/banner/upload_file/',views.banner_upload_file,name = 'upload_file'),
]

#course管理url
urlpatterns += [
    path('course/pub/',course_views.CourseView.as_view(),name = 'course')
]

# DOC
urlpatterns += [
    path('doc/upload/',doc_views.DocUploadView.as_view(),name = 'upload'),
    path('doc/upload-file/',doc_views.UploadFileView.as_view(),name = 'uploadfile')
]

# Staff
urlpatterns += [
    path('staff/add/',staff_views.StaffAddView.as_view(),name = 'staff_add'),
    path('staff/',staff_views.StaffView.as_view(),name = 'staff')
]