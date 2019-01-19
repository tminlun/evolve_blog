from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


#扩展user表（如果出现错误，看AbstractUser继承有没有错误）
class UserProfile(AbstractUser):
    '''用户扩展'''
    nick_name = models.CharField(max_length=15, default='',null=True,blank=True, verbose_name="昵称")
    birthday = models.DateField(null=True,blank=True,verbose_name="生日")#null:为null,blank:为""
    gander = models.CharField(max_length=10,default='man',choices=(('man','男'),('woman','女')),verbose_name="性别")
    address = models.CharField(max_length=100,default='',null=True,blank=True,verbose_name="住址")
    mobile = models.CharField(max_length=11,default='',null=True,blank=True,verbose_name="手机号码")
    image = models.ImageField(upload_to='users/%Y%m',default='',null=True,blank=True,max_length=100,verbose_name='头像')

    class Meta:
        verbose_name = '用户扩展'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.username) #AbstractUser自带username


#邮箱验证码
class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register','注册'),
        ('forget','找回密码')
    )
    code = models.CharField(max_length=20,verbose_name="验证码")
    email = models.EmailField(max_length=50,verbose_name="邮箱")
    send_type = models.CharField(choices=send_choices,max_length=10,verbose_name="验证码的类型")
    send_time = models.DateTimeField(default=datetime.now,verbose_name="发送时间")

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}{1}'.format(self.code,self.email)


#轮播图
class Banner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to="banner/%Y%m",max_length=100,default='banner/default.png')
    url = models.URLField('访问地址',max_length=200)#url是图片的路径
    index = models.IntegerField('顺序',default=100)# index控制轮播图的播放顺序
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
