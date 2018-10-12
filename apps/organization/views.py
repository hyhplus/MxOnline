from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse

from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserFavorite
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm


# Create your views here.
class OrgView(View):
    """
    处理课程机构列表的`view`
    """
    def get(self, request):
        # 查找到所有的课程机构
        all_org = CourseOrg.objects.all()

        all_city = CityDict.objects.all()

        # 取出筛选的城市，默认值为空
        city_id = request.GET.get('city', '')
        # 如果选择了某个城市，也就是前端传过来了值
        if city_id:
            # 外键`city`在数据中叫`city_id`
            # 我们就在机构中做进一步筛选
            all_org = all_org.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            # 我们就在机构中作进一步筛选类别
            all_org = all_org.filter(category=category)

        # 热门机构
        hot_org = all_org.order_by('-click_nums')[:3]

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在`name`字段进行操作，做`like`语句操作
            all_org = all_org.filter(Q(name__icontains=search_keywords) |
                                     Q(desc__icontains=search_keywords) |
                                     Q(address__icontains=search_keywords))
        # 注意保持一定的顺序
        # 进行排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_org = all_org.order_by('-students')
        elif sort == 'courses':
            all_org = all_org.order_by('-course_nums')

        # 这里写在最后才统计
        # 统计机构数
        org_nums = all_org.count()

        # 对课程机构进行分页
        # 尝试获取前台`get`请求传递过来的`page`参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 这里指从`all_org`中取五个出来，每页显示五个
        p = Paginator(all_org, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org/org-list.html',
                      {
                          'all_org': orgs,
                          'all_city': all_city,
                          'org_nums': org_nums,
                          'city_id': city_id,
                          'category': category,
                          'hot_org':hot_org,
                          'sort': sort,
                          'search_keywords': search_keywords,
                      })


class AddUserAskView(View):
    """
    用户添加我要学习
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)

        if userask_form.is_valid():
            # 这里是modelform和form的区别
            # 它有model的属性
            # 当commit为true进行真正保存
            # 这样就不需要把一个一个字段取出来然后存到model的对象中之后save
            userask_form.save(commit=True)

            # 保存成功，返回json字符串，后面content_type是告诉浏览器的
            # 注意: 这里只能单引号'' 包含双引号""  '{"",""}'
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            # 注意: 这里只能单引号'' 包含双引号""  '{"",""}'
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


# return HttpResponse("{'status': 'fail', 'msg': {0}}".format(userask_form.errors),
#                     content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        # 根据id取值到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 通过课程机构找到课程，内建的变量，找到指定这个字段的外键引用
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.course_set.all()[:2]

        return render(request, 'org/org-detail-homepage.html',
                      {
                            'all_courses': all_courses,
                            'all_teacher': all_teacher,
                            'course_org': course_org,
                      })


class OrgCourseView(View):
    """
    访问课程列表的`view`
    """
    def get(self, request, org_id):
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()

        return render(request, 'org/org-detail-homepage.html',
                      {
                          'all_courses': all_courses,
                          'course_org': course_org,
                      })


class OrgDescView(View):
    """
    机构描述详情页的`view`
    """
    def get(self, request, org_id):
        # 向前端传值，表现目前在home页面
        current_page = 'desc'

        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        # 向前端传值说明用户是否收藏
        has_fav = False

        # 必须是用户已登录我们才需要判断
        if request.user.is_authenticated:

            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id,
                                           fav_type=2):
                has_fav = True

        return render(request, 'org/org-detail-desc.html',
                      {
                        'course_org': course_org,
                        'current_page': current_page,
                        'has_fav': has_fav,
                      })


class OrgTeacherView(View):
    """
    机构讲师列表页的`view`
    """
    def get(self, request, org_id):
        # 向前端传值，表明目前在home页
        current_page = 'teacher'

        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_teachers = course_org.teacher_set.all()

        # 向前端传值说明用户是否收藏
        has_fav = False

        # 必须是用户已登录我们才需要判断
        if request.user.is_authenticated:

            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_org.id,
                                           fav_type=2):
                has_fav = True

        return render(request, 'org/org-detail-teachers.html',
                      {
                           'all_teachers':all_teachers,
                            'course_org': course_org,
                            "current_page":current_page,
                            "has_fav":has_fav,
                      })


class TeacherListView(View):
    """
    课程讲师列表页的`view`
    """
    def get(self, request):
        all_teacher = Teacher.objects.all()
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teacher = all_teacher.order_by('-click_nums')

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) |
                                             Q(work_company__icontains=search_keywords))
        # 排行榜讲师
        rank_teacher = Teacher.objects.all().order_by('-fav_nums')[:5]
        teacher_nums = all_teacher.count()

        # 分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, 4, request=request)
        teachers = p.page(page)

        return render(request, 'org/teachers-list.html',
                      {
                          'all_teacher': teachers,
                          'teacher_nums': teacher_nums,
                          'sort': sort,
                          'rank_teachers': rank_teacher,
                          'search_keywords': search_keywords,
                      })


class TeacherDetailView(View):
    """
    讲师详情页面的`view`
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher.click_nums += 1
        teacher.save()

        # all_course = teacher.course_set.all()
        #
        # rank_teacher = Teacher.objects.all().order_by('-fav_nums')[:5]
        # has_fav_teacher = False
        #
        # if UserFavorite.objects.filter(user=request.user,
        #                                fav_type=3,
        #                                fav_id=teacher_id):
        #     has_fav_teacher = True
        #
        # has_fav_org = False
        # if UserFavorite.objects.filter(user=request.user,
        #                                fav_type=2, fav_id=teacher.org.id):
        #     has_fav_org = True
        #
        # return render(request, 'org/teachers-list.html',
        #               {
        #                   'teacher': teacher,
        #                   'all_course': all_course,
        #                   'rank_teacher': rank_teacher,
        #                   'has_fav_teacher': has_fav_teacher,
        #                   'has_fav_org': has_fav_org,
        #               })

        all_course = Course.objects.filter(teacher=teacher)
        # 教师收藏和机构收藏
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3,
                                       fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user,
                                       fav_type=2,
                                       fav_id=teacher.org.id):
            has_org_faved = True
        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request,'org/teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'sorted_teacher':sorted_teacher,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved,
        })