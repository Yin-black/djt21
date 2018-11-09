from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from functools import wraps
from utils import json_status
from django.shortcuts import redirect,reverse


# Ajax访问的用户登陆验证装饰器
def ajax_login_required(view_func):
    @wraps(view_func)     #保证函数的原义性
    def decor(request,*args,**kargs):
        if request.user.is_authenticated:
            return view_func(request,*args,**kargs)
        else:
            if request.is_ajax():
                return json_status.un_auth_error(message="请先登陆！")
            else:
                return redirect(reverse("authPro:login"))
    return  decor

# 权限装饰器
def user_permission_required(model_name):
    def wrapper(view_func):
        @wraps(view_func)
        def func(request, *args, **kwargs):
            # 根据对应的模型找到 对应的content_type
            content_type = ContentType.objects.get_for_model(model_name)
            # 找到权限
            permissions = Permission.objects.filter(content_type=content_type)
            # 拼接权限 app名字.权限名字 ==> news.change_news
            code_name = [content_type.app_label + '.' + permission.codename for permission in permissions]
            # 判断是否具有权限
            res = request.user.has_perms(code_name)
            if res:
                return view_func(request, *args, **kwargs)
            return json_status.un_auth_error(message='权限不足')
        return func
    return wrapper

# 判断用户权限装饰器(自写)
def usrer_authticate(mode_name):
    def warper(view_func):
        @wraps(view_func)
        def func(request,*args,**kargs):
            # 根据模型名查content_type
            content_type=ContentType.objects.get_for_model(mode_name)
            # 根据content_type来查询权限，return权限列表
            permissions = Permission.objects.filter(content_type=content_type)
            # 拼接模型权限名称  return module_name.permission
            permiss_lable = [content_type.app_label+'.'+ permission.codename for permission in permissions ]
            #查询当前用户是否具有这些权限
            result = request.user.has_perms(permiss_lable)

            if result:
                return view_func(request,*args,**kargs)
            return json_status.un_auth_error(message='您权限不足，请联系管理员！')
        return func
    return warper

# 超级用户装饰器
def user_super_required(view_func):
    @wraps(view_func)
    def func(request,*args,**kwargs):
        if request.user.is_superuser:
            return view_func(request,*args,**kwargs)
        return json_status.un_auth_error(message='必须为超级用户！')
    return func