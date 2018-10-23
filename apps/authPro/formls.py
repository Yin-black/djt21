from django import forms
from utils import mcache

class LoginForm(forms.Form):
    """
    登陆表单
    """
    telephone = forms.CharField(max_length=11,min_length=11,error_messages={'max_length':"手机长度不超过11位","min_length":"手机长度不能小于11位"},required=True)
    password = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':"密码长度不超过20位","min_length":"密码长度不能小于6位"},required=True)
    remember = forms.BooleanField(required=False)

class RegisterForm(forms.Form):
    """
    注册表单
    """
    telephone = forms.CharField(max_length=11,min_length=11,error_messages={'max_length':"手机长度不超过11位","min_length":"手机长度不能小于11位"})
    sms_captcha = forms.CharField(max_length=4, min_length=4,
                                  error_messages={'max_length': "短信验证码长度为4位", "min_length": "短信验证码长度为4位"})
    username = forms.CharField(max_length=50, min_length=6,
                               error_messages={'max_length': "用户名长度不超过20位", "min_length": "用户名长度不小于6位",
                                               "required": '密码不能为空'})
    password = forms.CharField(max_length=20,min_length=6,
                               error_messages={'max_length':"密码长度不超过20位","min_length":"密码长度不能小于6位","required":'密码不能为空'})
    password_repeat = forms.CharField(max_length=20, min_length=6,
                               error_messages={'max_length': "密码长度不超过20位", "min_length": "密码长度不能小于6位",
                                               "required": '确认密码不能为空'})
    captcha_graph = forms.CharField(max_length=4, min_length=4,
                                  error_messages={'max_length': "图片验证码长度为4位", "min_length": "图片验证码长度为4位"},
                                  required=True)

    def check_data(self):
        """
        表单数据验证
        :return:
        """
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        print("-----------")
        print(password)
        print("-----------")

        #检验两次密码是否正确
        if password != password_repeat:
            return self.add_error('password','两次密码不一致！')


        graph_captcha = self.cleaned_data.get('captcha_graph')
        #获取表单的图形验证码
        graph_captcha_cache = mcache.get_key(graph_captcha.lower())
        #获取缓存的图形验证码

        print("-----------")
        print(graph_captcha)
        print(graph_captcha_cache)
        print("-----------")
        if not graph_captcha_cache and graph_captcha_cache!=graph_captcha.lower(): #检验图形验证码是否正确
            return self.add_error('captcha_graph','图形验证码输入错误！')

        sms_captcha = self.cleaned_data.get('sms_captcha')
        #获取表单的短信验证码
        sms_captcha_cache = mcache.get_key(sms_captcha.lower())
        #获取缓存短信验证码

        print("-----------")
        print(sms_captcha)
        print(sms_captcha_cache)
        print("-----------")
        if not sms_captcha_cache and sms_captcha.lower() != sms_captcha_cache:    #检验短信验证码是否正确
            return self.add_error('sms_captcha','短信验证码输入错误')
        return True