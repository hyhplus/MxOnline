from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import View

from .forms import LoginForm

# 基于类 实现需要继承的View

class RegisterView(View):
    """
    注册功能实现的view
    """
    # get方法直接返回页面
    def get(self, request):
        return render(request, 'users/register.html', {})


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

            # 成功返回user对象，失败返回null
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器, 完成登录
                login(request, user)

                # 跳转到首页，user request会被带回到首页
                return render(request, 'index.html')

            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})

        else:
            return render(
                request, "login.html", {
                    "login_form": login_form})