import os
import json
import uuid
from PIL import Image
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,AvatarUploadForm
from .models import EmailVerifyRecord
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserFavorite, FavoriteCount
from article.models import Blog
# Create your views here.


class CustomBackend(ModelBackend):
    """使得邮箱和用户名都可以登陆"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password): #如果密码解析的了
                return user
        except Exception:
            return None #获取邮箱出错返回None


def Fail(msg):
    """失败"""
    data = {}
    data['status'] = 'fail'
    data['msg'] = msg
    return JsonResponse(data)


def Success(msg):
    """成功"""
    data = {}
    data['status'] = 'success'
    data['msg'] = msg
    return JsonResponse(data)


class LoginView(View):
    """登录"""
    def get(self,request):
        current_url = request.GET.get('from', '')
        login_form = LoginForm()
        return render(request, 'login.html', {
            "login_form": login_form,
            "current_url": current_url,
        })

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #获取值
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password) #对数据库进行检查
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect(request.POST.get('next', reverse('home')))
                else:
                    return render(request, 'login.html',{'msg': '用户暂未激活，请前往QQ邮箱激活'})
            else:
                return render(request, 'login.html',{'login_form':login_form,'msg':'账号或者密码错误'})
        else:
            return render(request, 'login.html', {
                "login_form": login_form, #错误
            })


class LogoutView(View):
    """注销"""
    def get(self,request):
        logout(request)
        return redirect(request.GET.get('from', reverse('home')))


class RegisterView(View):
    """注册"""
    def get(self,request):
        register_form = RegisterForm()
        click_url = request.GET.get('from', '')
        return render(request,'sign_in.html',{
            'register_form': register_form,
            'click_url': click_url,
        })

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            #获取值
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password_again = request.POST.get('password_again', '')
            #验证值
            if UserProfile.objects.filter(username=username):
                return render(request, 'sign_in.html',{
                    'register_form': register_form,
                    'msg': '已经有此用户'
                })
            if UserProfile.objects.filter(email=email):# 邮箱：email
                return render(request, 'sign_in.html',{
                    'register_form': register_form,
                    'msg': '已经有此邮箱'
                })
            if password_again != password:
                return render(request, 'sign_in.html', {
                    'register_form': register_form,
                    'msg': '两次输入不一致'
                })
            #实例化用户
            user = UserProfile()
            user.username = username
            user.email = email
            user.password = make_password(password_again) #记得加密
            user.is_active = False
            user.save()
            #发送邮箱
            try:
                send_register_email(email, 'register')
            except Exception:
                return render(request, 'sign_in.html', {'msg': '邮箱出错'})
            return render(request, 'login.html',{'msg':'激活码已发送到QQ邮箱,请前往激活'})  # 注册完跳到登录页面
        else:
            return render(request, 'sign_in.html', {
                'register_form': register_form, #抛出forms错误
            })


class ForgetPwdView(View):
    """找回密码页面"""
    def get(self,request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html',{
            'forgetpwd_form': forgetpwd_form
        })

    def post(self,request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.get(email=email):
                send_register_email(email, 'forget')
                return render(request, 'active_fail.html', {
                    'msg': '邮箱已发送，请前往QQ邮箱进行修改密码'
                })
            else:
                return render(request, 'forgetpwd.html', {
                    'msg': '没有此邮箱的用户',
                    'forgetpwd_form': forgetpwd_form,
                })


class ModifyPwdView(View):
    """找回密码页面"""
    def get(self,request):
        modify_form = ModifyPwdForm()
        email = request.POST.get('email', '')
        return render(request, 'password_reset.html',{
            'email': email, #email只在用户激活邮箱时获取一次
            'modify_form': modify_form,
        })

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if password2 != password1:
                return render(request, 'password_reset.html',{'msg': '两次输入不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password2)
            user.save()
            return redirect('login')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {
                'modify_form': modify_form,
                'email':email,
            })


class ActiveUserView(View):
    """注册账号激活"""
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                EmailVerifyRecord.objects.filter(email=email, send_type='register').delete() #让一个邮箱可以注册多个账号
                return redirect('login')
        else:
            return render(request, 'active_fail.html',{
                'msg': '链接失效,返回注册页面',
            })


class ResetView(View):
    """找回密码激活"""
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request,'password_reset.html',{
                    'email': email
                })
        else:
            return render(request, 'active_fail.html',{
                'msg': '找回密码链接失效'
            })


class HomeView(View):
    """首页"""
    def get(self,request):
        return render(request, 'home.html',{})


class MyOperationView(LoginRequiredMixin, View):
    """
    收藏列表
    """
    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user)
        # 分页功能
        try:
            page = request.GET.get('page', 1)  # 获取n（page=n）,默认显示第一页
        except PageNotAnInteger:
            page = 1  # 出现异常显示第一页
        p = Paginator(user_favs,1, request=request)  # 进行分页，每5个作为一页
        favs = p.page(page)  # 获取当前页面
        return render(request, 'myoperation.html',{
            'user_favs': favs,
        })


# 图片上传
class ProfileView(LoginRequiredMixin, View):
    """  展示修改头像页面 """
    def get(self,request):
        user = request.user
        previous_url = request.GET.get('from')
        if user.is_authenticated:
            # 登录才可以访问此网页
            return render(request, 'profile.html', {'user': user,'previous_url':previous_url})
        # 没登录不做操作


class AjaxAvatarUploadView(LoginRequiredMixin, View):
    """
    保存
    """
    def post(self, request):
        user = request.user
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['avatar_file'] # 获取上传图片
            data = request.POST['avatar_data'] # 获取ajax返回图片坐标

            if img.size/1024 > 700:
                return JsonResponse({"message": "图片尺寸应小于900 X 1200 像素, 请重新上传。", })

            current_avatar = user.image  # 旧照片路径
            cropped_avatar = crop_image(current_avatar, img, data, user.id)  # 先新照片其压缩或裁剪，返回图片路径

            # 存储图片路径
            user.image = cropped_avatar
            user.save()

            # 向前台返回一个json，result值是图片路径
            data = {"result": user.image.url, "code": 200}
            return JsonResponse(data)
        else:
            return JsonResponse({"msg": "请重新上传。只能上传图片"})


def crop_image(current_avatar, file, data, uid):
    """
    处理头像
        :param current_avatar: 旧的照片
        :param file: 新图片
        :param data: 获取ajax返回图片坐标
        :param uid: 用户id
        :return:
    """
    # 新头像的后缀名（png）
    ext = file.name.split('.')[-1]

    #  uuid.uuid4()：随机数，hex[:10]：前10位数字转换为16进制
    #  {}.{}：{随机数字（新头像）}.{jpg}
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # 相对头像路径：（用户id / avatar / 头像名）,上传的头像会上传到这个路径
    cropped_avatar = os.path.join(str(uid), "avatar", file_name)
    # 绝对头像路径（media / id / 头像名）
    file_path = os.path.join("media", str(uid), "avatar", file_name)

    # 获取Ajax发送的裁剪参数data，先用json解析。
    #  {'x': 27.17776617378701, 'y': 2.26191634211227, 'height': 164.89762434053827, 'width': 164.89762434053827, 'rotate': 0}
    coords = json.loads(data)
    t_x = int(coords['x']) # 获取x值
    t_y = int(coords['y'])
    t_width = t_x + int(coords['width'])  # x + width
    t_height = t_y + int(coords['height'])
    t_rotate = coords['rotate']

    # 裁剪图片,压缩尺寸为400*400。
    img = Image.open(file)
    crop_im = img.crop((t_x, t_y, t_width, t_height)).resize((400, 400), Image.ANTIALIAS).rotate(t_rotate)

    # 保存图片
    '''
    dirname：（media / id / 头像名）
    功能：上一级目录
    如：
         print(os.path.dirname(media / id / 头像文件名))
         media / id
    '''
    # 保存到目录
    directory = os.path.dirname(file_path)  # 上一级目录
    # 判断括号里的目录，是否存在上一级目录
    if os.path.exists(directory):
        # 有，裁剪图片进行保存
        crop_im.save(file_path)
    else:
        # 如果没有目录（media / id / 头像名）
        os.makedirs(directory)  # 创建directory目录
        # 裁剪图片保存到，头像目录
        crop_im.save(file_path)

    # 上传新图片后，删除旧的图片
    # 判断是否使用默认头像，否则进行删除操作
    if not current_avatar == os.path.join("avatar", "default.jpg"):
        # 上传新图片，不使用默认头像
        current_avatar_path = os.path.join("media", str(uid), "avatar", os.path.basename(current_avatar.url))  # 老图片
        # 删除老照片
        os.remove(current_avatar_path)

    return cropped_avatar


#进度条
class MarkProgCount(View):
    def post(self,request):
        data = {}
        for i in range(101):
            cont_prog = int(i * 100 / 100)
            data['cont_prog'] = cont_prog
        # safe=False：传递如何值
        return JsonResponse(data, safe=False)