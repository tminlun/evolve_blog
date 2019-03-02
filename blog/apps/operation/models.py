from django.db import models
from datetime import datetime
from article.models import Blog
from users.models import UserProfile

# Create your models here.


class UserAsk(models.Model):
    """用户留言"""
    name = models.CharField(default='佚名',max_length=20, verbose_name="姓名")
    email_nums = models.EmailField(default='',max_length=32,verbose_name="留言的邮箱")
    message = models.TextField(max_length=200,verbose_name="留言内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="留言的时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 用户评论
class CourseComments(models.Model):
    """用户评论"""
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="评论的用户")
    blog = models.ForeignKey(Blog,related_name='comment_blog',on_delete=models.CASCADE,verbose_name="评论的博客")
    comment = models.TextField(verbose_name="评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    root = models.ForeignKey('self',related_name="root_comment",on_delete=models.CASCADE,null=True,blank=True,verbose_name="顶级评论")
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,verbose_name="上一级评论")#上一级评论在此模型

    reply_to = models.ForeignKey(UserProfile,related_name="reply_users",on_delete=models.CASCADE,null=True,blank=True,verbose_name="回复给谁")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]

    def __str__(self):
        return "{0}添加：{1}".format(self.user, self.comment)


class UserFavorite(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="收藏的用户")
    fav_blog = models.ForeignKey(Blog, on_delete=models.CASCADE,verbose_name="收藏的博客")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏的时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}收藏了{1}'.format(self.user,self.fav_blog)


class FavoriteCount(models.Model):
    """
        用户收藏数量
    """
    fav_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="收藏的博客")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数量")

    class Meta:
        verbose_name = "收藏数量"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fav_nums


class UserLike(models.Model):
    """
    用户点赞
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="点赞的用户")
    like_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="点赞的博客")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="点赞的时间")

    class Meta:
        verbose_name = "用户点赞"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}点赞了{1}'.format(self.user, self.like_blog)


class LikeCount(models.Model):
    """
        用户点赞数量
    """
    like_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="点赞的博客")
    like_nums = models.IntegerField(default=0,verbose_name="点赞数量")

    class Meta:
        verbose_name = "点赞数量"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.like_nums


class Photo(models.Model):
    """图片描述"""
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE, verbose_name="作者")
    photo = models.ImageField(upload_to="photo/%Y%m", null=True,blank=True, verbose_name="图片")
    describe = models.CharField(max_length=100,null=True,blank=True, verbose_name="描述")
    photo_type = models.CharField(max_length=20,verbose_name="图片类型",blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="时间")

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}添加了图片".format(self.author)

