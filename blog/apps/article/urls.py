# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/1/17 0017 17:53'

from django.urls import path
from .views import AticleListView, AticleDetailView
from operation.views import AddCommentView, ReplyCommentView, AddFavView, AddLikeView

app_name = "article"

urlpatterns = [

    path('article-list/',AticleListView.as_view(), name="article-list"), #文章列表
    path('article-detail/<int:blog_id>/',AticleDetailView.as_view(), name="article-detail"), #文章列表
    path('add_comment/',AddCommentView.as_view(), name="add_comment"), #评论功能
    path('reply_comment/', ReplyCommentView.as_view(), name="reply_comment"),#回复
    path('add_fav/', AddFavView.as_view(), name="add_fav"),#收藏
    path('add_like/', AddLikeView.as_view(), name="add_like"),#收藏
]
