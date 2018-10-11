# coding: utf-8
__author__ = 'Evan'

import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """
    `我要学习`版块表单验证
    进阶版本的`modelform`: 它可以向model一样save
    继承之余还可以新增字段
    """
    # 是由哪个model转换的
    class Meta:
        model = UserAsk
        # 我需要验证的字段
        fields = ['name','mobile','course_name']

    # 手机号码的正则表达式验证
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)

        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
