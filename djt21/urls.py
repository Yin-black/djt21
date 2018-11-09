"""djt21 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.news.urls')),
    path('auth/',include('apps.authPro.urls')),
    path('doc/',include('apps.doc.urls')),
    path('course/',include('apps.course.urls')),
    path('cms/',include('apps.cms.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)     #可以通过浏览器直接访问media文件夹
