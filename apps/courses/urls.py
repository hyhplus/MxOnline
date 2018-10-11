# coding: utf-8
__author__ = 'Evan'

from django.urls import path, re_path

from courses.views import CourseListView, CourseDetailView

# 必须加上app_name
app_name = "courses"

urlpatterns = [
    # 课程列表url
    path('list/', CourseListView.as_view(), name="list"),

    # 课程详情页
    re_path('course/(?P<course_id>\d+)/', CourseDetailView.as_view(),
            name='course_detail'),

]