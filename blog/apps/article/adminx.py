# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/1/12 0012 14:15'

import xadmin
from .models import BlogType,Blog,CourseResource


class BlogTypeAdmin(object):
    # 显示的列
    list_display = ('name', 'add_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name']
    # 过滤
    list_filter = ['name', 'add_time']


class BlogAdmin(object):
    # 显示的列
    list_display = ('name', 'blog_type','describe','detail','image','author','related','click_nums','fav_nums','like_nums','add_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'blog_type','describe','detail','image','author','related']
    # 过滤
    list_filter = ['name', 'blog_type','describe','detail','image','author','related','click_nums','fav_nums','like_nums','add_time']


class CourseResourceAdmin(object):
    # 显示的列
    list_display = ('name', 'course', 'download', 'add_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'course', 'download',]
    # 过滤
    list_filter = ['name', 'course', 'download', 'add_time']


xadmin.site.register(BlogType, BlogTypeAdmin)
xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
