from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.db.models import Q
from .models import Blog, BlogType
from operation.models import CourseComments, UserFavorite
# Create your views here.


class AticleListView(View):
    """博客列表"""
    def get(self,request):
        all_blog = Blog.objects.all()
        all_blog_type = BlogType.objects.all()

        # 全局搜索
        search_keywords = request.GET.get('keywords', '')  # 获取用户输入的值
        if search_keywords:  # 如果获取的了
            # 进行Q查询,包含（__icontains：加了i则不区分大小写）,查询完毕返回值（all_course）
            all_blog = all_blog.filter(Q(name__icontains=search_keywords) | Q(detail__icontains=search_keywords)
                                       | Q(describe__icontains=search_keywords)
                                       )

        #排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_blog = all_blog.order_by('-click_nums')
        elif sort == 'ascending':#升序
            all_blog = all_blog.order_by('-add_time')
        elif sort == 'descending':#降序
            all_blog = all_blog.order_by('add_time')

        #分页筛选
        blog_type_id = request.GET.get('blog_type', '')
        if blog_type_id:
            all_blog = all_blog.filter(blog_type_id=int(blog_type_id))

        # 分页功能
        try:
            page = request.GET.get('page', 1)  # 获取n（page=n）,默认显示第一页
        except PageNotAnInteger:
            page = 1  # 出现异常显示第一页
        p = Paginator(all_blog, 5, request=request)  # 进行分页，每5个作为一页
        blogs = p.page(page)  # 获取当前页面
        return render(request, 'article-list.html', {
            'all_blog': blogs,
            'all_blog_type': all_blog_type,
            'sort': sort,
            'blog_type_id': blog_type_id,#分类筛选
        })


class AticleDetailView(View):
    """博客细节"""
    def get(self, request, blog_id):
        blog_detail = get_object_or_404(Blog, pk=int(blog_id))
        all_blog_type = BlogType.objects.all()

        previous_blog = Blog.objects.filter(add_time__gt=blog_detail.add_time).last()
        next_blog = Blog.objects.filter(add_time__lt=blog_detail.add_time).first()

        all_comment = CourseComments.objects.filter(blog=blog_detail, root=None) #让回复内容不显示（root可以得到全部回复）
        #如果浏览器没有cookie记录，阅读数加1
        cookie = "%s_pk" % blog_detail.pk
        if not request.COOKIES.get(cookie):
            blog_detail.click_nums += 1
            blog_detail.save()

        # 相关课程推荐
        tag = request.GET.get('tag', '')
        blog_tags = Blog.objects.filter(related=tag)[:5]

        #收藏
        has_blog_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_blog=blog_detail):
                has_blog_fav = True
        response = render(request, 'article-detail.html', {
            'blog_detail': blog_detail,
            'all_blog_type': all_blog_type,
            'blog_tags': blog_tags,#相关博客
            'previous_blog': previous_blog,
            'next_blog': next_blog,
            'all_comment': all_comment,
            'has_blog_fav': has_blog_fav,
        })
        response.set_cookie(cookie, 'true')
        return response


