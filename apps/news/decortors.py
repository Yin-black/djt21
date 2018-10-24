from functools import wraps
from utils import json_status
from django.shortcuts import redirect,reverse


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