# coding: utf-8
__author__ = 'Evan'

import json
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, PageNotAnInteger

from .forms import UploadImageForm, ModifyPwdForm, UserInfoForm
from users.models import UserProfile, EmailVerifyRecord
from operation.models import UserCourse, UserMessage
from utils.email_send import send_register_email


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息的`view`
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'user_center/usercenter-info.html', {})

    def post(self, request):
        # 这里不像用户咨询是一个新的，需要指明instance
        # 不然无法修改，而是新增用户
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success}',
                                content_type='application/json')
        else:

            return HttpResponse(json.dumps(user_info_form.errors),
                                content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户上传图片的`view`，用于修改头像
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        # 这时候用户上传的文件就已经被保存到image_form了
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_form.save()

            # # 取出cleaned data中的值,一个dict
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    在个人中心修改用户密码
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modifyPwd_form = ModifyPwdForm(request.POST)
        if modifyPwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}',
                                    content_type='application/json')
            # 如果密码一致
            user =request.user
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        # 验证失败说明密码位数不够
        else:
            return HttpResponse('{"status":"fail", "msg":"填写错误请检查"}',
                                content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码的`view`
    """
    def get(self,request):
        # 取出需要发送的邮件
        email = request.GET.get("email", "")

        # 不能是已注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱的`view`
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(
                            email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    用户个人中心-我的课程的`view`
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'user_center/usercenter-mycourse.html',
                      {
                          'user_courses': user_courses,
                      })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人中心消息页面，清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id,
                                                        has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对消息进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_message中取出4个，每页显示4个
        p = Paginator(all_message, 4)
        messages = p.page(page)

        return render(request, 'user_center/usercenter-message.html',
                      {
                          'messages': messages,
                      })
