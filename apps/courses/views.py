from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, PageNotAnInteger
from .models import Course


class CourseListView(View):
    """
    课程列表的｀view`
    """
    def get(self, request):
        all_course = Course.objects.all()

        # 热门课程推荐
        hot_courses = Course.objects.all().order_by("-students")[:3]

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # `OR`操作使用Q
            all_course = all_course.filter(Q(name__icontains=search_keywords) |
                                           Q(desc__icontains=search_keywords) |
                                           Q(detail__icontains=search_keywords))

        # 进行排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')

        # 对课程进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_course中取6个出来，每页显示6个
        p = Paginator(all_course, 6, request=request)
        courses = p.page(page)


        return render(request, 'course/course-list.html',
                      {
                         'all_course': courses,
                         'sort': sort,
                         'hot_courses': hot_courses,
                         'search_keywords': search_keywords,
                      })


class CourseDetailView(View):
    """
    课程详情页的`view`
    """
    pass
