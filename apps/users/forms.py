# coding: utf-8
__author__ = 'Evan'

from django import forms


class LoginForm(forms.Form):
    """
    登录表单验证
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)