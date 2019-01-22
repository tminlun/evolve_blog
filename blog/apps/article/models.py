from django.db import models
from datetime import datetime
from users.models import UserProfile
# Create your models here.


class BlogType(models.Model):
    """博客类型"""
    name = models.CharField(max_length=20, verbose_name="类型")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    """博客"""
    name = models.CharField(max_length=20, verbose_name="标题")
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name="博客类型")
    describe = models.CharField(max_length=100, verbose_name="描述",null=True,blank=True)
    detail = models.CharField(max_length=300,verbose_name="内容")
    image = models.ImageField(upload_to="blog/%Y%m",null=True,blank=True,verbose_name="图片")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="作者")
    related = models.CharField(max_length=20,blank=True, verbose_name="相关博客")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    # fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    # like_nums = models.IntegerField(default=0,verbose_name='喜欢人数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.name


    def details(self):
        if len(str(self.detail)) > 65:
            return '{}...'.format(str(self.detail))[0:65]
        else:
            return self.detail

#博客资源
class CourseResource(models.Model):
    """博客资源"""
    course = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="博客")
    name = models.CharField(max_length=100, verbose_name="资源名")
    download = models.FileField(upload_to="blog/resource/%Y%m",verbose_name="资源文件")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "博客资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
