from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.urls import reverse
from django.views.generic.base import View
from django.db.models import Q

from .forms import LoginForm, RegisterForm, ForgetForm
from .forms import ActiveForm, ModifyPwdForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


# 基于类 实现需要继承的`View`
class CustomBackend(ModelBackend):
    """
    邮箱和用户名都可以登录
    继承`ModelBackend`类，因为有`authenticate()`方法
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    """
    注册功能实现的`view`
    """
    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)

            # 用户已存在判断
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'users/register.html',
                              {'register_form': register_form, 'msg': '用户已存在'})

            pass_word = request.POST.get('password', '')

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False

            user_profile.password = make_password(pass_word)

            user_profile.save()

            # 发送激活邮箱
            send_register_email(user_name, 'register')

            return render(request, 'login.html')

        else:
            return render(request, 'users/register.html',
                          {'register_form': register_form})


class LoginView(View):
    """
    登录逻辑实现类
    """
    # 直接调用get方法免去判断
    def get(self, request):
        # render是渲染html返回用户
        # render三大变量：request, 模板名称，一个字典写明传给前端的值
        return render(request, 'login.html', {})

    def post(self, request):
        # 类实例化需要一个字典参数dict。 request.POST就是一个QueryDict所以直接传入
        # POST 中的 username, password 会对应到 LoginForm 中
        login_form = LoginForm(request.POST)

        # is_valid判断是否通过表单验证
        if login_form.is_valid():
            # 取不到为空，username, password为前端页面name的值
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')

            # 成功返回user对象，失败返回None
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器, 完成登录

                if user.is_active:
                    login(request, user)

                    # 跳转到首页，user request会被带回到首页
                    # return render(request, 'index.html')
                    # 增加重定向回原网页。
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    # 跳转到首页 user request会被带回到首页
                    return HttpResponseRedirect(reverse('index'))
                else:
                    # 用户未激活跳转登录，提示未激活
                    return render(request, 'login.html',
                                  {'msg': '用户名未激活! 请前往邮箱进行激活！'})

            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})

        else:
            return render(
                request, "login.html", {
                    "login_form": login_form})


class ActiveUserView(View):
    """
    发送邮箱的激活链接从而激活用户
    """
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        # 验证码错误
        else:
            return render(request, 'users/active_fail.html')

        # 激活成功跳转到登录页面
        return render(request, 'login.html')


class ForgetPwdView(View):
    """
    用户忘记密码的`view`
    """
    # get方法直接返回页面
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "users/forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)

        # `form`验证合法情况下取出`email`
        if forget_form.is_valid():
            email = request.POST.get('email', '')

            # 发送找回密码邮件, 类型为`forget`
            send_register_email(email, 'forget')

            # 发送完毕返回登录页面并显示发送邮箱成功
            return render(request, 'login.html', {'msg': '重置密码邮箱已发送，请注意查收'})
        else:
            # 验证表单失败，刷新页面并提示验证错误信息
            return render(request, 'users/forgetpwd.html', {
                            'forget_form': forget_form
                         })


class ResetView(View):
    """
    重置密码的`view` 接收邮件显示此页面, 处理get逻辑
    """
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 将`email`传回来
                return render(request, 'users/password_reset.html', {'email': email})
        else:
            return render(
                request, "users/forgetpwd.html", {
                    "msg": "您的重置密码链接无效,请重新请求", "active_form": active_form})


class ModifyPwdView(View):
    """
    修改密码的`view`, 处理post提交逻辑
    """
    def post(self, request):
        modifyPwd_form = ModifyPwdForm(request.POST)
        if modifyPwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            # 如果两次密码不一致，返回错误信息
            if pwd1 != pwd2:
                return render(request, 'users/password_reset.html',
                              {"email": email, "msg": "密码不一致"})
            # 如果密码一致
            user = UserProfile.objects.get(email=email)
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return render(request, "login.html", {"msg": "密码修改成功，请登录"})

        # 验证失败说明密码位数不够
        else:
            email = request.POST.get("email", "")
            return render(request, "users/password_reset.html",
                          {"email": email, "modifyPwd_form": modifyPwd_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))