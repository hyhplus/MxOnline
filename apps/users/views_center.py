# coding: utf-8
from django.contrib.auth.hashers import make_password

from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email

__author__ = 'Evan'

from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View

from .forms import UploadImageForm, ModifyPwdForm


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息的`view`
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):

        return render(request, 'user_center/usercenter-info.html',
                      {

                      })


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
        modiypwd_form = ModifyPwdForm(request.POST)
        if modiypwd_form.is_valid():
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
        # 验证失败说明密码位数不够。
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
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')

