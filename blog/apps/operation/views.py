# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import CourseComments, UserFavorite
from article.models import Blog
from users.models import UserProfile
# Create your views here.


def Success(msg):
    """ajax成功"""
    data = {}
    data['status'] = 'success'
    data['msg'] = msg
    return JsonResponse(data)


def Fail(msg):
    """ajax失败"""
    data = {}
    data['status'] = 'fail'
    data['msg'] = msg
    return JsonResponse(data)


class AddCommentView(View):
    """评论功能"""
    def post(self, request):
        blog_id = int(request.POST.get('blog_id', 0))
        comments = request.POST.get('comments', '')
        user = request.user

        if not user.is_authenticated:
            return Fail('用户未登录')

        #实例化
        blog_comment = CourseComments()
        if blog_id > 0 and comments != '':
            blog_comment.blog = Blog.objects.get(pk=blog_id)
            blog_comment.user = user
            blog_comment.comment = comments
            blog_comment.save()
            return Success('评论成功')
        else:
            return Fail('评论失败')


class ReplyCommentView(View):
    """回复功能"""

    def post(self,request):

        root_id = int(request.POST.get('root_comment_id', 0))#顶级评论的id
        reply_id = int(request.POST.get('reply_comment_id', 0))#上一级回复的id
        reply_user_id = int(request.POST.get('reply_user_id', 0))#上一级回复user的id
        blog_pk = int(request.POST.get('blog_pk', 0))  # 课程id

        root_comment_text = request.POST.get('comment', '')#回复顶级评论的内容
        ptn_text = request.POST.get('ptn', '')#回复回复评论的内容

        try:
            root_id = CourseComments.objects.get(pk=root_id)#获取"一个"评论对象（顶级评论）
            reply_id = CourseComments.objects.get(pk=reply_id)
            reply_user_id = UserProfile.objects.get(pk=reply_user_id) #回复给谁
        except:
            return Fail('回复失败')

        #回复内容传递给数据库
        course_comment = CourseComments()
        course_comment.user = request.user #回复的作者
        course_comment.blog = Blog.objects.get(pk=blog_pk)
        course_comment.root = root_id
        course_comment.parent = reply_id
        course_comment.reply_to = reply_user_id
        if ptn_text == '':#如果回复评论的内容为空，则把回复顶级内容赋值给评论内容
            if root_comment_text == '':#如果回复顶级内容为空，抛出错误
                return Fail('回复不能为空')
            course_comment.comment = root_comment_text
        else:
            if ptn_text == '':#如果回复回复评论内容为空，抛出错误
                return Fail('回复不能为空')
            course_comment.comment = ptn_text
        course_comment.save()
        return Success('评论成功') #坑，保存数据库后，记得返回ajax成功信息使得刷新页面


class AddFavView(View):
    """用户点击收藏"""
    def post(self,request):
        #获取值
        fav_id = int(request.POST.get('fav_id', 0))
        user = request.user
        fav_blog = Blog.objects.get(pk=fav_id)

        if not user.is_authenticated:
            return Fail('用户未登录')

        #查询是否有收藏
        fav_record = UserFavorite.objects.filter(user=user, fav_blog=fav_blog)
        #如果有收藏，那么用户在点击此方法的时候视为取消收藏
        if fav_record:
            fav_record.delete()
            if fav_blog.fav_nums > 0:
                fav_blog.fav_nums -= 1
            elif fav_blog.fav_nums <= 0:
                fav_blog.fav_nums = 0
            fav_blog.save()
            return JsonResponse({'status': 'success', 'msg': '收藏', 'fav_nums': fav_blog.fav_nums})
        else:
            user_fav = UserFavorite()
            if fav_id > 0:
                user_fav.user = request.user
                user_fav.fav_blog = fav_blog
                user_fav.save()
                fav_blog.fav_nums += 1
                fav_blog.save()
                return JsonResponse({'status':'success','msg':'已收藏','fav_nums': fav_blog.fav_nums})
            else:
                return Fail('收藏出错')
