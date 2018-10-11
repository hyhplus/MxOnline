# encoding: utf-8
from datetime import datetime

from django.db import models

from courses.models import Course
from users.models import UserProfile
from organization.models import CourseOrg


# Create your models here.
class UserAsk(models.Model):
    """
    用户咨询
    """
    name = models.CharField(verbose_name='姓名', max_length=20)
    mobile = models.CharField(verbose_name='手机', max_length=11)
    course_name = models.CharField(verbose_name='课程名', max_length=100)
    add_time = models.DateTimeField(verbose_name='咨询时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComments(models.Model):
    """
    用户对课程的评论
    会涉及两个外键：1.用户; 2.课程
    """
    course = models.ForeignKey(Course, verbose_name='课程',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='用户',
                             on_delete=models.CASCADE)
    comments = models.CharField(verbose_name='评论', max_length=250)
    add_time = models.DateTimeField(verbose_name='评论时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    """
    用户对课程，机构，讲师的收藏
    """
    TYPE_CHOICES = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '讲师')
    )

    user = models.ForeignKey(UserProfile, verbose_name='用户',
                             on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, verbose_name=u"课程")
    # teacher = models.ForeignKey()
    # org = models.ForeignKey()

    # 直接保存用户的id
    fav_id = models.IntegerField(default=0)

    # 表明收藏的是哪种类型
    fav_type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name='收藏类型')
    add_time = models.DateTimeField(verbose_name='收藏时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    """
    用户消息

    # 因为我们的消息有两种:发给全员和发给某一个用户。
    # 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息。
    # 机智版 为0发给所有用户，不为0就是发给用户的id
    """
    user = models.IntegerField(verbose_name='接收用户', default=0)
    message = models.CharField(verbose_name='消息内容', max_length=500)

    has_read = models.BooleanField(verbose_name='是否已读', default=False)
    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    """
    用户课程表
    会涉及到两个外键：1.用户; 2.课程
    """
    course = models.ForeignKey(Course, verbose_name='课程',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='用户',
                             on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

