from rest_framework import serializers
from .models import NewsConten
from apps.authPro.serailizer import NewsUserSerailizer

class NewsContentSerailizer(serializers.ModelSerializer):
    auth = NewsUserSerailizer()
    class Meta:
        model = NewsConten
        fields = ('id','content','create_time','auth')