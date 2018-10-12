"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, LogoutView
from users.views import ForgetPwdView, ResetView, ModifyPwdView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    # 将admin换为x-admin
    path('x-admin/', xadmin.site.urls),

    # 首页    TemplateView.as_view 会将 template 转换为 view
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # 基于类的方式实现登录,这里是调用它的方法
    path('login/', LoginView.as_view(), name='login'),

    # 注册url
    path('register/', RegisterView.as_view(), name='register'),

    # 验证码url
    path("captcha/", include('captcha.urls')),

    # 邮件激活的url
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),

    # 忘记密码url
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),

    # 重置密码url: 用来接收 来自邮箱的重置链接
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),

    # 修改密码url; 用于password, reset页面提交表单
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 退出功能url
    path('logout/', LogoutView.as_view(), name='logout'),


    # 课程机构app的url配置
    path('org/', include('organization.urls', namespace='org')),

    # 处理上传图片显示url, 使用Django自带的serve
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    # 课程app的url配置
    path('course/', include('courses.urls', namespace='course')),


    # 用户app的url配置
    path('users/', include('users.urls', namespace='users')),

]
