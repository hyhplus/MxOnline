from django.http import HttpResponse
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