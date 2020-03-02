
from django.urls import path

from . import views

# 视图函数命名空间，告诉django这个urls模块是属于blog应用的，用来区分以后一些第三方应用中也叫index和detail的函数
app_name = 'blog'
urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    # 详情页
    path('posts/<int:pk>', views.detail, name='detail'),
    # 归档
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    # 目录
    path('category/<int:pk>', views.category, name='category'),
    # 标签
    path('tags/<int:pk>', views.tag, name='tag'),
    # 目录名
    path('category_name', views.category_name, name='category_name'),
]









"""
path函数实际上是一个规则，Django用这个规则去匹配用户实际输入的网址
如果匹配成功，就会调用其后面的视图函数做响应的处理。
如http://127.0.0.1:8000,当用户输入此网址后，Django首先会把协议http、
域名127.0.0.1和端口号8000去掉，此时只剩下一个空字符串，而''的模式
正是匹配一个空字符串，于是二者匹配，Django便会调用其对应的views.index函数
"""