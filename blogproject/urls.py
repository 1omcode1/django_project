"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('comments.urls')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
]
'''
这里导入了一个include函数，然后利用这个函数把blog应用下的urls.py文件包含了进来。此外
include前还有一个''(函数)，这是一个空字符串。这里也可以写其他字符串，django这个字符串
和后面include的urls.py文件中的url拼接。比如说如果我们这里把''改成'blog/',而我们在blog/urls.py
中是''，即一个空字符串。那么Django最终匹配的就是blog/加上一个空字符串，即blog/。
'''
