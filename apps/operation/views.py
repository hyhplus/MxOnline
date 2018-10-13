from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from courses.models import Course
from operation.models import UserFavorite
from organization.models import CourseOrg, Teacher


class AddFavView(View):
    """
    用户收藏与取消收藏
    """
    def post(self, request):
        # 表明你收藏的不管是课程，讲师，还是机构。他们的id
        # 默认值取0是因为空串转int报错
        id = request.POST.get('fav_id', 0)

        # 取到你收藏的类别，从前台提交的ajax请求中取
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录，即使没登录会有一个匿名的user
        if not request.user.is_authenticated:

            return HttpResponse('{"status": "fail", "msg": "用户未登录"}',
                                content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(id),
                                                    fav_type=int(fav_type),)
        if exist_records:
            # 已收藏，则取消收藏
            exist_records.delete()

            # 分别对课程，机构，讲师的取消收藏操作{`-1`}
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status": "success", "msg": "收藏"}',
                                content_type='application/json')

        else:
            user_fav = UserFavorite()

            # 过滤掉未取到fav_id type的默认情况
            if int(fav_type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save()

                # 分别对课程，机构，讲师的收藏操作{`+1`}
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status": "success", "msg": "已收藏"}',
                                    content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏失败"}',
                                    content_type='application/json')


class MyFavOrgView(LoginRequiredMixin, View):
    """
    个人中心-我收藏的课程机构
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        org_list = []
        fav_org_filter = UserFavorite.objects.filter(user=request.user, fav_type=2)

        for fav_org in fav_org_filter:
            # 取出fav_id,也就是机构的id
            org_id = fav_org.fav_id
            # 从而获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'user_center/usercenter-fav-org.html',
                      {
                          'org_list': org_list,
                      })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    个人中心-我收藏的授课讲师
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)

        # 上面fav_teachers只是存放了id,我们需要通过id找到讲师对象
        for fav_teacher in fav_teachers:
            # 取出fav_id,也就是讲师的id
            teacher_id = fav_teacher.fav_id
            # 从而获取这个机构对象
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'user_center/usercenter-fav-teacher.html',
                      {
                          'teacher_list': teacher_list,
                      })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    个人中心-我收藏的课程
    """
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)

        for fav_course in fav_courses:
            # 取出fav_id,也就是课程的id
            course_id = fav_course.fav_id
            # 从而获取这个课程对象
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'user_center/usercenter-fav-course.html',
                      {
                          'course_list': course_list,
                      })