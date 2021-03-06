# coding: utf-8
__author__ = 'Evan'

from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile


class LoginForm(forms.Form):
    """
    登录表单验证
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """
    注册表单验证 & 验证码
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)

    # 应用验证码
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    """
    忘记密码表单验证
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ActiveForm(forms.Form):
    """
    激活时验证码实现
    激活时不对邮箱密码做验证
    应用验证码 自定义错误输出key必须与异常一致
    """
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    """
    重置密码表单验证
    这里设置密码和再次确认密码
    """
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)



class UploadImageForm(forms.ModelForm):
    """
    用于文件上传，修改头像
    """
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """
    用于个人中心修改个人信息
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']