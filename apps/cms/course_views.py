from django.shortcuts import render,reverse
from django import views
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET, require_POST
from apps.news.models import NewsTag,NewsPub,NewsHotAddModle,NewsBanner
from utils import json_status
from django.http import QueryDict, JsonResponse
from qiniu import Auth
from djt21 import settings
from . import forms
from apps.authPro.formcheck import FormMixin
from django.utils.timezone import timedelta, datetime, make_aware
from urllib.parse import urlencode
from apps.news.serailizer import NewsBannerSerializer
from apps.course.models import Teacher,CourseCategory,Course
from apps.course.forms import CoursePubForm

@method_decorator([csrf_exempt,staff_member_required(login_url='/auth/login/')],name='dispatch')
class CourseView(views.View,FormMixin):
    """
    谭程发布后台主页
    """
    def get(self, request):
        teachers = Teacher.objects.filter(is_delete=True).all()
        categories = CourseCategory.objects.filter(is_delete=True).all()
        context = {
            "teachers": teachers,
            "categories": categories,
        }
        return render(request, 'cms/couser/couser_pub.html', context=context)

    def post(self, request):
        form = CoursePubForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            video_url = form.cleaned_data.get("video_url")
            cover_url = form.cleaned_data.get("cover_url")
            teacher_id = form.cleaned_data.get("teacher_id")
            # name=teacher_name
            teacher = Teacher.objects.filter(id=teacher_id).first()
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get("profile")
            outline = form.cleaned_data.get("outline")
            category_id = form.cleaned_data.get('category_id')
            # category 分类
            category = CourseCategory.objects.filter(id=category_id).first()
            course = Course.objects.create(title=title, video_url=video_url, cover_url=cover_url, teacher=teacher,
                                           duration=duration, profile=profile, outline=outline, category=category)
            return json_status.result(data={"course_id": course.id})
        print(form.errors)
        return json_status.params_error(message=self.get_error(form))