from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


# Create your models here.
class Course(models.Model):
    """
    课程信息
    """
    DEGREE_CHOICES = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级')
    )

    name = models.CharField(verbose_name='课程名', max_length=50)
    desc = models.CharField(verbose_name='课程描述', max_length=300)
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(verbose_name='难度', choices=DEGREE_CHOICES,
                              max_length=2)
    learn_times = models.IntegerField(verbose_name='学习时长(分钟数)',
                                      default=0)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0)
    image = models.ImageField(upload_to='courses/%Y/%m',
                              verbose_name='封面图',
                              max_length=100)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now)

    course_org = models.ForeignKey(CourseOrg, verbose_name='所属机构',
                                   null=True, blank=True,
                                   on_delete=models.CASCADE)
    # 添加外键：讲师
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                verbose_name="讲师",
                                null=True, blank=True)
    # 添加课程类别
    category = models.CharField(verbose_name='课程类别', max_length=20,
                                default='Python开发')
    tag = models.CharField(verbose_name='课程标签', max_length=15,
                           default='')
    # 添加其他字段
    you_need_know = models.CharField(verbose_name='课程须知', max_length=300,
                                     default='一颗勤学的心是本课程必要的前提')
    teacher_tell = models.CharField(verbose_name='老师告诉你', max_length=300,
                                    default='什么都可以学到，按时交作业，不然叫家长')
    is_banner = models.BooleanField(verbose_name='是否轮播', default=False)

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        # 获取课程章节数的方法
        return self.lesson_set.all().count()

    # 获取学习这门课程的用户
    def get_learn_users(self):
        # 谁的里面添加了它做外键，他都可以取出来
        return self.usercourse_set.all()[:5]

    def get_teacher_nums(self):
        return  self.lesson_set.all().count()


class Lesson(models.Model):
    """
    章节
    """
    course = models.ForeignKey(Course, verbose_name='课程',
                               on_delete=models.CASCADE)
    name = models.CharField(verbose_name='章节名', max_length=100)
    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    """
    每章视频
    """
    lesson = models.ForeignKey(Lesson, verbose_name='章节',
                               on_delete=models.CASCADE)
    name = models.CharField(verbose_name='视频名', max_length=100)
    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now)
    url = models.CharField(verbose_name='访问地址', max_length=200,
                           default='/media/text.mp4')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    """
    课程资源
    """
    course = models.ForeignKey(Course, verbose_name='课程',
                               on_delete=models.CASCADE)
    name = models.CharField(verbose_name='课程资源名', max_length=100)
    download = models.FileField(upload_to='courses/resource/%Y/%m',
                                verbose_name='资源文件',max_length=100)
    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name