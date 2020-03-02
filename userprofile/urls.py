

from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]