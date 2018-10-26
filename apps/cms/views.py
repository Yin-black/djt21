import os
from django.core.paginator import Paginator
from django.shortcuts import render,reverse
from django import views
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from apps.news.models import NewsTag,NewsPub
from utils import json_status
from django.http import QueryDict, JsonResponse
import json
from qiniu import Auth
from djt21 import settings
from . import forms
from apps.authPro.formcheck import FormMixin


# Create your views here.
@staff_member_required(login_url='/auth/login/')
def index(request):
    return render(request,'cms/index.html')


@method_decorator([csrf_exempt,staff_member_required(login_url='/auth/login/')],name='dispatch')
class TagManageView(views.View):
    """
    新闻标签管理
    """

    def get(self,request):
        new_tags = NewsTag.objects.filter(is_delete=True).all()
        return render(request,'cms/news/news_tag_manage.html',context={"news_tags":new_tags})

    def post(self,request):
        """
        添加新闻标签
        :param request:
        :return:
        """
        tagVal = request.POST.get('name',None)

        if tagVal:
            news = NewsTag.objects.filter(name=tagVal).exists()   #如果存在返回True,否则False
            if not news:
                NewsTag.objects.create(name=tagVal)
                return json_status.result(message='添加成功！')
            else:
                return json_status.params_error(message='标签名已存在，请不要重复输入！')
        else:
            return json_status.params_error(message='值不能为空！')

    def put(self,request):
        """
        编辑新闻标签

        """
        tagVal = QueryDict(request.body)  #接受后台返回来的数据，并Dict
        # print("----------")
        # print(tagVal)
        # print(tagVal.get('tag_name'))
        # print("----------")
        newid = tagVal.get('tag_id')
        newtag = NewsTag.objects.filter(id=newid).all()
        if newtag:
            newtag.update(name = tagVal.get('tag_name'))
            return json_status.result(message="标签修改成功！")
        return json_status.params_error(message='标签修改失败！')

    def delete(self,request):

        tagid_dict = QueryDict(request.body)
        tagid = tagid_dict.get('tag_id')
        news = NewsTag.objects.filter(id=tagid)
        if tagid and news:
            news.update(is_delete = False)
            return json_status.result(message="删除成功！")
        return json_status.params_error(message='删除失败！请联系管理员。')

@method_decorator([csrf_exempt,staff_member_required(login_url='/auth/login/')],name='dispatch')
class PubNews(views.View,FormMixin):
    """
    发布新闻
    """

    def get(self,request):
        new_tags = NewsTag.objects.filter(is_delete=True).all()
        return render(request, 'cms/news/pub_news.html',context={"news_tags":new_tags})

    def post(self,request):
        form = forms.PubNewsForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail_url = form.cleaned_data.get('thumbnail_url')
            content = form.cleaned_data.get("content")

            tag_id = form.cleaned_data.get('tag_id')
            newstag = NewsTag.objects.filter(id = tag_id).all()
            if newstag:
                new = NewsPub(title=title,desc=desc,thumbnail=thumbnail_url,content=content,tag=newstag[0],auth=request.user)
                new.save()
                # print(newstag)
                return json_status.result(message='发布成功！')
            else:
                return json_status.params_error(message='新闻标签不存在！')
        else:
            return json_status.params_error(message=self.get_error(form))

@method_decorator([csrf_exempt,staff_member_required(login_url='/auth/login/')],name='dispatch')
class Upload_Qiniu(views.View):
    """
    上传到七牛空间
    """
    def get(self,request):
        # -*- coding: utf-8 -*-
        # flake8: noqa

        # 需要填写你的 Access Key 和 Secret Key
        access_key = settings.ACCESS_KEY
        secret_key = settings.SECRET_KEY
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = settings.BUCKET_NAME
        # 上传到七牛后保存的文件名
        # key = ''
        # 生成上传 Token，可以指定过期时间等
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        # policy = {
        #     # 'callbackUrl':'https://requestb.in/1c7q2d31',
        #     # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        #     # 'persistentOps':'imageView2/1/w/200/h/200'
        # }
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name,expires=3600)
        print(token)
        return JsonResponse({"uptoken":token})

    def post(self,request):
        pass


@method_decorator([csrf_exempt,staff_member_required(login_url='/auth/login/')],name='dispatch')
class Upload_server(views.View):
    """
    上传到服务器
    """
    def post(self,request):
        filepath = settings.MEDIA_ROOT
        f = request.FILES.get('upload_file')
        filename = os.path.join(filepath,f.name)

        with open(filename,'wb') as file:
            for chunk in f.chunks():
                file.write(chunk)
        fileurl = request.build_absolute_uri(settings.MEDIA_URL+f.name)   #生成一个可访问的url地址

        return json_status.result(message="sucess",data={"file_url":fileurl})

@method_decorator([csrf_exempt,staff_member_required(login_url='/auth/login/')],name='dispatch')
class NewsManage(views.View):
    """
    新闻管理
    """

    def get(self,request):

        current_page = int(request.GET.get("p",1))  #获取前台传的当前页面号

        per_page_news = 2     #每页显示的新闻列表数量
        newslist=NewsPub.objects.filter(is_delete=True).all()
        paginator = Paginator(newslist, per_page_news)
        context = self.get_page_data(paginator,current_page)
        # print("=====================")
        # print(current_page)
        # print(context)
        # print("=====================")
        return render(request,'cms/news/news_manage.html',context = context)

    def post(self,request):
        pass


    def get_page_data(self,paginator,current_page=1):
        """
        处理页面很多的时候，页码显示的样式
        """
        around_count = 2  #控制当前页面前后显示的页码数
        left_flag = False   #True表示左边要显示"..."
        right_flag = False  #True表示右边要显示"..."
        p = paginator.page(current_page)

        left_start_index = current_page - around_count
        left_end_index  = current_page

        right_start_index = current_page
        right_end_index = right_start_index +around_count+1

        # 左边页码范围
        if current_page <= around_count +around_count:
            left_flag = False
            left_range = range(1,left_end_index)
        else:
            left_flag = True
            left_range = range(left_start_index,left_end_index)

        #右边页码范围
        if current_page <= paginator.num_pages - around_count - around_count:
            right_flag = True
            right_range = range(right_start_index, right_end_index)
        else:
            right_flag = False
            right_range = range(current_page, paginator.num_pages+1)
        # print("***************")
        # print(current_page)
        # print("***************")

        context = {
            'paginator': paginator,
            'p_news': p,
            'left_start_index':left_start_index,
            'left_end_index': left_end_index,
            'right_start_index':right_start_index,
            'right_end_index':right_end_index,
            'left_flag':left_flag,
            'right_flag':right_flag,
            'left_range':left_range,
            'right_range':right_range,
            'current_page':current_page,
        }
        return context

