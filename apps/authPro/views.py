from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse,HttpResponse
from django.views import View
from .formls import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .formcheck import FormMixin
from utils import captcha_check,mcache,json_status
from io import BytesIO
from .models import User


# Create your views here.

@method_decorator(csrf_exempt,name='dispatch')  #关闭跨域攻击
class LoginView(View,FormMixin):
    """
    登陆
    """
    def get(self,request):
        return render(request,'authPro/login.html')

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user= authenticate(username = telephone,password = password)
            if user:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                # return JsonResponse({'code':2,'msg':'登陆成功'})
                return json_status.result(message='登陆成功！')
            else:
                 # return JsonResponse({'code':1,'msg':'手机或密码不正确！'})
                return json_status.params_error(message="手机或密码不正确！")
        else:
            # return JsonResponse({'code':1,'msg':self.get_error(form)})
            return json_status.params_error(message=self.get_error(form))

@method_decorator(csrf_exempt,name='dispatch')  #关闭跨域攻击
class RegisterView(View,FormMixin):
    """
    注册
    """
    def get(self,request):
        return  render(request,'authPro/register.html')

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid() and form.check_data():
                telephone = form.cleaned_data.get('telephone')
                password = form.cleaned_data.get('password')
                username = form.cleaned_data.get('username')

                # print("-----------")
                # print(telephone,username,password)
                # print("-----------")

                #存入数据库
                user = User.objects.create_user(telephone=telephone,username=username,password=password)
                login(request,user)
                # print(user)
                # print(dir(user))
                # return JsonResponse({"code":2,"msg":"注册成功"})
                return json_status.result(message="注册成功！")
        else:
             # return JsonResponse({"code":1,"msg":self.get_error(form)})
             return json_status.params_error(message=self.get_error(form))

def logout_view(request):
    """
    退出登陆
    """
    logout(request)
    return redirect(reverse('authPro:login'))

def captcha_view(request):
    """
    随机图片
    """
    text,img = captcha_check.Captcha.gene_code()  #返回一个字符串和一个image对象
    out = BytesIO()
    img.save(out,'png')
    out.seek(0)
    resp = HttpResponse(content_type='image/png')
    #图片验证码写入缓存
    mcache.set_key(text.lower(),text.lower())

    resp.write(out.read())
    return resp

@method_decorator(csrf_exempt,name='dispatch')  #关闭跨域攻击
def send_sms_captcha_view(request):

    captch = captcha_check.Captcha.gene_text()
    telephone =request.GET.get('telephone')
    print(telephone,captch)
    # mesg = sms_send.send_sms(telephone,captch)

    # 短信验证码写入缓存
    mcache.set_key(captch.lower(),captch.lower())
    # return JsonResponse(str(mesg,encoding='utf-8'),safe=False)
    # return  JsonResponse({"code":2,"msg":"ok"})
    return json_status.result(message="ok")