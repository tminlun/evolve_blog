from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm
from .models import EmailVerifyRecord
from utils.email_send import send_register_email
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
            send_register_email(email, 'register')
            return render(request, 'login.html',{'msg':'邮箱已发送,请激活'})  # 注册完跳到登录页面
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
            return render(request, 'password_reset.html', {
                'modify_form': modify_form,
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
        return render(request, 'home.html',{
        })



