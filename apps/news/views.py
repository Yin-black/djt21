from django.shortcuts import render
from django.http import Http404
from django.views import View
from .models import NewsPub,NewsTag,NewsHotAddModle,NewsBanner
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import NewContent
from apps.authPro.formcheck import FormMixin
from .models import NewsConten
from utils import json_status
from .serailizer import NewsContentSerailizer,NewsPubSerailizer,NewsTagSerailizer,NewsHotSerailizer
from utils.decortors import ajax_login_required
from djt21 import settings
from django.db.models import Q
from apps.course.models import Course
# encoding=utf8

# Create your views here.
class NewsView(View):
    def get(self,request):
        newspubs = NewsPub.objects.defer('content').filter(is_delete=True).all().order_by('-id')   #倒序排列，最新发布的提前显示,同时conten字段不查询以提高速度
        tag = NewsTag.objects.filter(is_delete=True).all()
        h_news = NewsHotAddModle.objects.filter(is_delete=True)
        banners = NewsBanner.objects.filter(is_delete=True)
        courses = Course.objects.filter(is_delete=True).first()

        return render(request,'news/index.html',context={"newspubs":newspubs,
                                                         "newtags":tag,
                                                         'banners':banners,
                                                         'h_news':h_news,
                                                         'coureses':courses})


class NewsDtailView(View):
    def get(self,request,tag_id):
        try:
            news = NewsPub.objects.get(is_delete=True,id = tag_id)
            return render(request,'news/news_detail.html',context={"news":news})
        except NewsPub.DoesNotExist:
            raise Http404

@method_decorator([csrf_exempt,ajax_login_required],name="dispatch")
class AddNewsContentView(View,FormMixin):
    """
    添加评论
    """
    def get(self,request):
        pass

    def post(self,request):

        form = NewContent(request.POST)

        if form.is_valid():
            new_id = form.cleaned_data.get('news_id')
            print(new_id)
            news = NewsPub.objects.filter(id = new_id,is_delete=True).first()
            # print(news)
            if news:
                content = form.cleaned_data.get('content')
                news_content = NewsConten.objects.create(content=content,auth = request.user,news= news)

                # contents = NewsConten.objects.filter(id = news_content.id)
                # print(type(contents))

                new_se = NewsContentSerailizer(news_content)
                return json_status.result(message='添加成功',data=new_se.data)
            else:
                return  json_status.params_error(message='新闻不存在！')
        else:
            return json_status.params_error(message=self.get_error(form))


class GetNewsContentView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = NewsPub.objects.filter(id = news_id,is_delete=True).first()
        if news:
            new_contents = news.newsconten_set.all()   #通过新闻反向查询评论
            print(type(new_contents))

            contents =NewsContentSerailizer(new_contents,many=True)   #序列化结果
            return json_status.result(data=contents.data)
        else:
            return json_status.params_error(message='没有这条新闻！')


def newslis_view(request):
    """
    新闻列表。每点击"加载更多"按钮加载ONE_PAGE_NEWS_COUNT条新闻
    """

    page = int(request.GET.get('page',1))
    print(page)
    tag_id = int(request.GET.get('tag_id',0))

    start_page = settings.ONE_PAGE_NEWS_COUNT * (page-1)
    end_page = start_page + settings.ONE_PAGE_NEWS_COUNT

    print("=================")
    print(page,tag_id)
    print("=================")
    if tag_id:
        nlist = NewsPub.objects.select_related('tag','auth').defer('content').filter(is_delete=True,tag_id=tag_id)[start_page:end_page]

        seralizer = NewsPubSerailizer(nlist,many=True)
        return json_status.result(data={"newses":seralizer.data})
    else:
        nlist = NewsPub.objects.select_related('tag', 'auth').defer('content').filter(is_delete=True)[
                start_page:end_page]

        seralizer = NewsPubSerailizer(nlist, many=True)
        return json_status.result(data={"newses": seralizer.data})

#     /news/hot/list/
def news_hot_list(request):
    """
    热点新闻列表
    """
    hot_news = NewsHotAddModle.objects.all()
    if hot_news:
        serailizer = NewsHotSerailizer(hot_news,many=True)
        return json_status.result(data=serailizer.data)
    return json_status.params_error(message='没有设置优先级的新闻！')

# /news/tag/list/
def news_tag_list(request):
    """
    新闻标签列表
    """
    tags = NewsTag.objects.all()
    # print(tags[0])
    serializer = NewsTagSerailizer(tags,many=True)
    # print(serializer.data)
    return json_status.result(data={'tags':serializer.data})

def news_with_tag(request):
    """
    根据新闻标签显示新闻标题
    """
    tag_id = int(request.GET.get('tag_id',0))
    if tag_id:
        newstag = NewsPub.objects.filter(tag_id= tag_id,is_delete=True)
    elif not tag_id:
        newstag = NewsPub.objects.all()

    # print(tag_id)
    # print("++++++")
    # print(newstag)
    serializer = NewsPubSerailizer(newstag,many=True)

    return json_status.result(data={'newses':serializer.data})

def search(request):
    try:
        q = request.GET.get("q", '')
        courses = Course.objects.filter(is_delete=True).first()
        if q:
            result_newses = NewsPub.objects.select_related('tag', 'auth').filter(Q(title__icontains=q)|Q(auth__username__icontains=q)|Q(tag__name__icontains=q)|Q(content__icontains=q)|Q(desc__icontains=q))

            context = {
                "result_newses": result_newses,
                "q": q,
            }
        else:
            #所有热门新闻都查出来
            h_newses = NewsHotAddModle.objects.select_related('news', 'news__tag', 'news__auth').filter(is_delete=True)
            context = {
                "h_newses": h_newses,
            }
        context.update({'coureses':courses})
        return render(request, 'news/search.html', context=context)
    except:
        raise Http404