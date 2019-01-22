# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import CourseComments, UserFavorite,FavoriteCount,UserLike,LikeCount
from article.models import Blog
from users.models import UserProfile
# Create your views here.


def Success(msg):
    """ajax成功"""
    data = {}
    data['status'] = 'success'
    data['msg'] = msg
    return JsonResponse(data)


def ConditionSuccess(condition_nums):
    """点赞，收藏成功"""
    data = {}
    data['status'] = 'success'
    data['condition_nums'] = condition_nums
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
        root_comment_text = request.POST.get('comment', '')  # 回复顶级评论的内容
        ptn_text = request.POST.get('ptn', '')  # 回复回复评论的内容

        try:
            root_id = CourseComments.objects.get(pk=root_id)#获取"一个"评论对象（顶级评论）
            reply_id = CourseComments.objects.get(pk=reply_id)
            reply_user_id = UserProfile.objects.get(pk=reply_user_id) #回复给谁
        except Exception as e:
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
        user = request.user
        fav_id = int(request.POST.get('fav_id', 0))
        is_fav = request.POST.get('is_fav', '')

        try:
            fav_blog = Blog.objects.get(pk=fav_id)
        except ObjectDoesNotExist:
            return Fail('获取不到对象')

        if not user.is_authenticated:
            return Fail('用户未登录')

        if is_fav == 'true':
            #如果没有active,要收藏
            user_fav, created = UserFavorite.objects.get_or_create(fav_blog=fav_blog, user=user)
            if created:
                #没有收藏
                fav_count, created = FavoriteCount.objects.get_or_create(fav_blog=fav_blog)
                #收藏数+1
                fav_count.fav_nums += 1
                fav_count.save()
                return ConditionSuccess(fav_count.fav_nums)
            else:
                #已经收藏
                return Fail('已收藏，无需再收藏')
        else:
            #有active，取消收藏
            if UserFavorite.objects.filter(fav_blog=fav_blog, user=user):
                #已收藏
                UserFavorite.objects.get(fav_blog=fav_blog,user=user).delete()
                fav_count, created = FavoriteCount.objects.get_or_create(fav_blog=fav_blog)
                if not created:
                    #有收藏数
                    fav_count.fav_nums -= 1
                    fav_count.save()
                    return ConditionSuccess(fav_count.fav_nums)
                else:
                    #没有收藏数
                    return Fail('没有收藏，不能减一')
            else:
                #没有收藏
                return Fail('您未收藏')


class AddLikeView(View):
    """用户点赞功能"""
    def post(self,request):
        # 获取值
        user = request.user
        like_id = int(request.POST.get('like_id', 0))
        is_like = request.POST.get('is_like', '')

        try:
            like_blog = Blog.objects.get(pk=like_id)
        except ObjectDoesNotExist:
            return Fail('获取不到对象')

        if not user.is_authenticated:
            return Fail('用户未登录')

        if is_like == 'true':
            # 如果没有active,要收藏
            user_fav, created = UserLike.objects.get_or_create(like_blog=like_blog, user=user)
            if created:
                # 没有收藏
                like_count, created = LikeCount.objects.get_or_create(like_blog=like_blog)
                # 收藏数+1
                like_count.like_nums += 1
                like_count.save()
                return ConditionSuccess(like_count.like_nums)
            else:
                # 已经收藏
                return Fail('已点赞，无需再点赞')
        else:
            # 有active，取消收藏
            if UserLike.objects.filter(like_blog=like_blog, user=user):
                # 已收藏
                UserLike.objects.get(like_blog=like_blog, user=user).delete()
                like_count, created = LikeCount.objects.get_or_create(like_blog=like_blog)
                if not created:
                    # 有收藏数
                    like_count.like_nums -= 1
                    like_count.save()
                    return ConditionSuccess(like_count.like_nums)
                else:
                    # 没有收藏数
                    return Fail('没有点赞，不能减一')
            else:
                # 没有收藏
                return Fail('您未点赞')
