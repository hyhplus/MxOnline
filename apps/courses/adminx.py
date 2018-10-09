# coding: utf-8
__author__ = 'Evan'

from .models import Course, Lesson, Video, CourseResource
import xadmin


class CourseAdmin(object):
    """
    # 显示的列   list_display
    # 搜索字段   search_fields
    # 过滤      list_filter
    """
    list_display = [
        'name', 'desc', 'detail',
        'degree', 'learn_times',
        'students'
    ]

    search_fields = ['name', 'desc', 'detail', 'degree', 'students']

    list_filter = [
        'name', 'desc', 'detail',
        'degree', 'learn_times',
        'students'
    ]


class LessonAdmin(object):
    """
    # 显示的列   list_display
    # 搜索字段   search_fields
    # 过滤      list_filter
    """
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']

    # __name代表使用外键中name字段
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    """
    # 显示的列   list_display
    # 搜索字段   search_fields
    # 过滤      list_filter
    """
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    """
    # 显示的列   list_display
    # 搜索字段   search_fields
    # 过滤      list_filter
    """
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']

    # __name代表使用外键中name字段
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

