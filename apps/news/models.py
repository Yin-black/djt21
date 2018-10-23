from django.db import models


# Create your models here.

class NewsTag(models.Model):
    """
    新闻标签
    """
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    # 是否删除标志
    #False 为假删，True 为真删
    is_delete = models.BooleanField(default=True)


class NewsPub(models.Model):
    """
    新闻
    """
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()

    pub_time =models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)

    #forign key
    tag= models.ForeignKey('NewsTag',on_delete=models.CASCADE)
    auth = models.ForeignKey('authPro.User',on_delete=models.CASCADE)


class NewsConten(models.Model):
    """
    新闻评论
    """

    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)

    auth = models.ForeignKey('authPro.User',on_delete=models.CASCADE)
    news = models.ForeignKey('NewsPub',on_delete=models.CASCADE)