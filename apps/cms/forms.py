from django import forms


class PubNewsForm(forms.Form):
    title = forms.CharField(max_length=100,min_length=2,error_messages={"max_lenght":"标题不能超过100","min_length":"标题不能小于2","required":"标题不能为空"})
    desc = forms.CharField(max_length=200,min_length=2,error_messages={"max_lenght":"描述不能超过200","min_length":"描述不能小于2","required":"描述不能为空"})
    tag_id = forms.IntegerField(error_messages={"required":"标签不能为空！"})
    thumbnail_url = forms.URLField()
    content = forms.CharField(max_length=100000,min_length=2,error_messages={"max_lenght":"内容不能超过100000","min_length":"描述不能小于2","required":"内容不能为空"})

class NewsHotAddForm(forms.Form):
    news_id = forms.IntegerField(required='新闻ID不能为空！')
    priority = forms.IntegerField(required='优先级不能为空！')


class NewsEditForm(PubNewsForm):
    news_id = forms.CharField(error_messages={'required':'新闻ID不能为空！'})

class NewsBannerForm(forms.Form):
    image_url = forms.URLField(error_messages={"required": "图片地址不能为空", "invalid": "请输入合法的图片网址"})
    priority = forms.IntegerField(error_messages={"required": "优先级不能为空"})
    link_to = forms.URLField(error_messages={"required": "跳转地址不能为空", "invalid": "请输入合法的跳转网址"})