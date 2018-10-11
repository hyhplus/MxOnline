# coding: utf-8
__author__ = 'Evan'

from django.urls import path, re_path

from organization.views import OrgView, AddUserAskView
from organization.views import OrgHomeView, OrgCourseView
from organization.views import OrgDescView, OrgTeacherView
from organization.views import TeacherListView, TeacherDetailView
from operation.views import AddFavView

# 解决Django2.0.1: app_name报错问题
# 必须加上app_name
app_name = 'organization'

urlpatterns = [
    # 课程机构首页url
    path('org_list/', OrgView.as_view(), name='org_list'),

    # 添加我要学习的url
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),

    # home页面，取纯数字
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name='org_home'),

    # 访问课程的url
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='org_course'),

    # 访问机构详情的url
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='org_desc'),

    # 访问机构讲师的url
    re_path('teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='org_teacher'),

    # 机构收藏的url
    re_path('add_fav/', AddFavView.as_view(), name='add_fav'),

    # 讲师列表的url
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),

    # 访问讲师详情的url
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(),
            name='teacher_detail'),

]