from rest_framework import serializers
from .models import NewsConten,NewsTag,NewsPub
from apps.authPro.serailizer import NewsUserSerailizer

class NewsContentSerailizer(serializers.ModelSerializer):
    auth = NewsUserSerailizer()
    class Meta:
        model = NewsConten
        fields = ('id','content','create_time','auth')


class NewsTagSerailizer(serializers.ModelSerializer):

    class Meta:
        model = NewsTag
        fields = ('name',)

class NewsPubSerailizer(serializers.ModelSerializer):
    auth = NewsUserSerailizer()
    tag = NewsTagSerailizer()

    class Meta:
        model = NewsPub
        fields = ('id','title','desc','pub_time','thumbnail','auth','tag')