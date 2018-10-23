from django import forms


class NewContent(forms.Form):
    news_id = forms.IntegerField()
    content = forms.CharField(max_length=10000,min_length=1,error_messages={'max_length':'评论字数不能超过10000','min_length':'评论字数不能少于1','required':'评论不能为空！'})
