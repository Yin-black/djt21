from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from .models import NewsPub,NewsTag
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import NewContent
from apps.authPro.formcheck import FormMixin
from .models import NewsConten
from utils import json_status
# Create your views here.
class NewsView(View):
    def get(self,request):
        newspubs = NewsPub.objects.defer('content').filter(is_delete=True).all().order_by('-id')   #倒序排列，最新发布的提前显示,同时conten字段不查询以提高速度
        tag = NewsTag.objects.filter(is_delete=True).all()
        return render(request,'news/index.html',context={"newspubs":newspubs,"newtags":tag})

class SearchView(View):
    def get(self,request):
        return render(request,'news/search.html')


class NewsDtailView(View):
    def get(self,request,tag_id):
        news = NewsPub.objects.get(is_delete=True,id = tag_id)
        return render(request,'news/news_detail.html',context={"news":news})

@method_decorator(csrf_exempt,name="dispatch")
class AddNewsContentView(View,FormMixin):
    def get(self,request):
        news_id = request.GET.get('news_id')

    def post(self,request):

        form = NewContent(request.POST)

        if form.is_valid():
            new_id = form.cleaned_data.get('news_id')
            print(new_id)
            news = NewsPub.objects.filter(id = new_id,is_delete=True)
            print(news)
            if news:
                content = form.cleaned_data.get('content')
                news_content = NewsConten(content=content,auth = request.user,news= news[0])
                news_content.save()
                return json_status.result(message='发表成功')
            else:
                return  json_status.params_error(message='新闻不存在！')
        else:
            return json_status.params_error(message=self.get_error(form))
