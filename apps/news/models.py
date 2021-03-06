from django.db import models


# Create your models here.

class NewsTag(models.Model):
    """
    新闻标签
    """
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    # 是否删除标志
    #False 为此记录删除，True 为未除删除
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

    class Meta:
        ordering = ('-id',)

class NewsHotAddModle(models.Model):
    """
    热门新闻
    """
    news = models.OneToOneField('NewsPub',on_delete=models.CASCADE)
    priority = models.IntegerField()

    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)

class NewsBanner(models.Model):
    image_url = models.URLField()
    priority = models.IntegerField()
    link_to = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)

    class Meta:
        ordering = ['-priority']