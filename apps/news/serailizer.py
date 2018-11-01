from rest_framework import serializers
from .models import NewsConten,NewsTag,NewsPub,NewsHotAddModle
from apps.authPro.serailizer import NewsUserSerailizer

class NewsContentSerailizer(serializers.ModelSerializer):
    auth = NewsUserSerailizer()
    class Meta:
        model = NewsConten
        fields = ('id','content','create_time','auth')


class NewsTagSerailizer(serializers.ModelSerializer):

    class Meta:
        model = NewsTag
        fields = ('id','name','create_time',)

class NewsPubSerailizer(serializers.ModelSerializer):
    auth = NewsUserSerailizer()
    tag = NewsTagSerailizer()

    class Meta:
        model = NewsPub
        fields = ('id','title','desc','pub_time','thumbnail','auth','tag')

class NewsHotSerailizer(serializers.ModelSerializer):
    news = NewsPubSerailizer()

    class Meta:
        model = NewsHotAddModle
        fields = ('id','news','priority','create_time')