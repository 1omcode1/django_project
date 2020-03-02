# 视图函数

import markdown
import re
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Tag
from django.views.generic import ListView

'''
from django.http import HttpResponse
def index(request):
    return HttpResonse('欢迎访问我的博客首页')
'''

'''
def index(request):
    return render(request,'blog/index.html',context={
        'title':'我的博客首页',
        'welcome':'欢迎访问我的博客'
    })
'''


def paginator_fiction(request, paginator):
    # paginator = Paginator(post_list, 2)
    try:
        num = request.GET.get('index', '1')
        page_num = paginator.page(num)
    except PageNotAnInteger:
        page_num = paginator.page(1)
    except EmptyPage:
        page_num = paginator.page(paginator.num_pages)

    post_list = page_num.object_list
    return page_num


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 4)
    page_num = paginator_fiction(request, paginator)

    post_list = page_num.object_list
    return render(request, 'blog/index.html', context={
        'paginator': paginator,
        'page': page_num,
        'post_list': post_list,
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])

    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})


# 完善归档功能
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')

    # 分页功能
    paginator = Paginator(post_list, 2)
    page_num = paginator_fiction(request, paginator)
    post_list = page_num.object_list
    # return render(request, 'blog/index.html', context={'post_list': post_list})
    return render(request, 'blog/index.html', context={
        'paginator': paginator,
        'page': page_num,
        'post_list': post_list,
    })


# 完善分类功能
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    # 分页功能
    paginator = Paginator(post_list, 3)
    page_num = paginator_fiction(request, paginator)
    post_list = page_num.object_list

    # return render(request, 'blog/index.html', context={'post_list': post_list})
    return render(request, 'blog/index.html', context={
        'paginator': paginator,
        'page': page_num,
        'post_list': post_list,
    })


# 完善标签页面
def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')

    # 分页功能
    paginator = Paginator(post_list, 4)
    page_num = paginator_fiction(request, paginator)
    post_list = page_num.object_list

    # return render(request, 'blog/index.html', context={'post_list': post_list})
    return render(request, 'blog/index.html', context={
        'paginator': paginator,
        'page': page_num,
        'post_list': post_list,
    })


# 首页目录标题功能设置
def category_name(request):
    category_name_list = Category.objects.all()
    return render(request, 'blog/category.html', context={
        'category_list': category_name_list
    })


'''
参数request是Django为我们封装好的http请求，它是类HttpRequest的一个实例，
然后我们便直接返回了一个HTTP响应给用户，这个响应也是Django帮我们封装好的，
也是HttpResponse的一个实例，只是我们给它传了一个自定义的字符串参数。

但是，我们的博客不可能只显示这么一句话，它可能会显示很长很长的内容。比如我们
发布的博客文章列表，或者一大段的博客文章。我们不能每次都把这些大段大段的内
容传给HttpResponse。因此，Django对这个问题给我们提供一个很好的解决方案，叫
做模板系统。Django要我们把大段的文本写到一个文件里，然后Django自己会去读取
这个文件，再把读取到的内容传给HttpResponse。让我们用模板系统来改造一下上面
的例子；

则调用Django提供的render函数，这个函数根据我们传入的参数构造HttpResponse.
我们首先把http请求传进去，然后render根据第二个参数的值找到这个模板并读取模板中
的内容。之后render根据我们传入的context参数的值把模板中的变量替换为我们传递的
变量的值，{{ title }}和{{ welcome }}中的变量则被我们替换成了上面显示的字符串，
也就是渲染了模板。然后输出会被返回到View生成HTTPresponse被发送到中间件，然后经过丰富
或者调整再返回到浏览器，呈现给用户。
'''
# Create your views here.


#  类视图写法
'''
class IndexView(ListView, PaginationMixin):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
'''

'''
class ArchiveView(IndexView):

    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(created_time__month=month).order_by('-created_time')

'''

'''
class CategoryView(IndexView):

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate).order_by('-created_time')
'''

'''
class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t).order_by('-created_time')

'''
