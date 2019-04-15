"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import url
from django.views.generic import TemplateView
from users.views import HomeView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView,ResetView,ModifyPwdView, MyOperationView
from users.views import ProfileView,AjaxAvatarUploadView,MarkProgCount
from article.views import TimerShaftView
from django.conf import settings #上传图片
from django.conf.urls.static import static #上传图片


urlpatterns = [
    path('xadmin/', xadmin.site.urls,name="xadmin"),
    path('',HomeView.as_view(),name="home"), #首页
    # 登录
    # $：避免同名url
    # path('login/',LoginView.as_view(),name="login"),
    url(r'^login/$', LoginView.as_view(),name="login"),
    path('signup/',RegisterView.as_view(),name="signup"), #注册
    path('logout/',LogoutView.as_view(),name="logout"), #注销
    path('captcha/',include('captcha.urls')), #验证码
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),#注册激活
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),#忘记密码页面
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"), #找回密码激活
    path('modify_pwd/',ModifyPwdView.as_view(), name="modify_pwd"), #重设密码
    path('article/',include('article.urls',namespace='article')), #文章
    path('timer_shaft/',TimerShaftView.as_view(), name="timer_shaft"), #时间轴
    path('ueditor/', include('DjangoUeditor.urls')), #富文本
    path('myoperation/', MyOperationView.as_view(), name="myoperation"), #收藏列表
    # 展示头像
    path('profile/',ProfileView.as_view(), name='profile'),
    # 处理头像
    path('profile/ajax/avatar/',AjaxAvatarUploadView.as_view(), name='ajax_avatar_upload'),
    # 进度条
    path('filecount/',MarkProgCount.as_view(), name='filecount'),
    # 第三方登录
    path('', include('social_django.urls', namespace='social'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
