from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, Http404
import os, hmac, hashlib, time
from django.conf import settings
from .models import Course,CourseCategory,Teacher

class Courseview(View):
    def get(self,request):
        courese = Course.objects.filter(is_delete=True)


        return render(request,'course/course.html',context={'courses':courese})

class CourseDetalView(View):
    """
    课程详情
    """
    def get(self,request,id):
        try:
            courese = Course.objects.get(is_delete=True,id=id)
            return render(request, 'course/course_detail.html', context={'course': courese})
        except Course.DoesNotExist:
            raise Http404

def course_token(request):
    # 获取视频路径
    video_url = request.GET.get('video_url')
    # video_url = 'http://ih2vvidjmihrie7nvje.exp.bcevod.com/mda-ih6x46pcj8w9vbs1/mda-ih6x46pcj8w9vbs1.m3u8'
    # 过期时间
    expiration_time = int(time.time()) + 3600
    # 百度云 UserId / UserKey
    user_id = settings.BAIDU_USER_ID
    user_key = settings.BAIDU_USER_KEY

    # extension ===> .mu38
    extension = os.path.splitext(video_url)[1]
    # mda-ih6x46pcj8w9vbs1
    media_id = video_url.split('/')[-1].replace(extension, '')

    # key 和 message 转化为 bytes
    key = user_key.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    # 加密盐 加密数据  加密方式
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, user_id, expiration_time)
    print(token)
    return JsonResponse({"token": token})
