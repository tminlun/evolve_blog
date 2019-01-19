# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/1/12 0012 17:02'


import xadmin
from .models import UserAsk,CourseComments,UserFavorite,UserLike


class UserAskAdmin(object):
    # 显示的列
    list_display = ('name', 'email_nums', 'message', 'add_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'email_nums', 'message', ]
    # 过滤
    list_filter = ['name', 'email_nums', 'message', 'add_time']


class CourseCommentsAdmin(object):
    # 显示的列
    list_display = ('user', 'blog', 'comment', 'root', 'parent', 'reply_to', 'add_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['user', 'blog', 'comment', 'root', 'parent', 'reply_to']
    # 过滤
    list_filter = ['user', 'blog', 'comment', 'root', 'parent', 'reply_to', 'add_time']


class UserFavoriteAdmin(object):
    # 显示的列
    list_display = ('user', 'fav_blog', 'add_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['user', 'fav_blog']
    # 过滤
    list_filter = ['user', 'fav_blog', 'add_time']


class UserLikeAdmin(object):
    # 显示的列
    list_display = ('user', 'like_blog', 'add_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['user', 'like_blog']
    # 过滤
    list_filter = ['user', 'like_blog', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserLike, UserLikeAdmin)
