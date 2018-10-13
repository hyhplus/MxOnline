from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class UserProfile(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )

    nick_name = models.CharField(verbose_name='昵称', max_length=50,
                                 default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', max_length=6,
                              choices=GENDER_CHOICES, default='female')
    address = models.CharField(verbose_name='地址', max_length=100,
                               default='')
    mobile = models.CharField(verbose_name='手机号码', max_length=11,
                              null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m',
                              default='image/default.png',
                              max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        """
        username继承自AbstractUser
        """
        return self.username

    def unread_nums(self):
        """
        页面顶部的小喇叭
        获取用户未读消息的数量
        这里导入`UserMessage`, 不能放在外面，否则会报错
        """
        from operation.models import UserMessage
        return UserMessage.objects.filter(has_read=False, user=self.id).count()


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    SEND_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱')
    )

    code = models.CharField(verbose_name='验证码', max_length=20)
    email = models.EmailField(verbose_name='邮箱', max_length=50)
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20)

    # 注意：这里的now没有(),因为now()是创建字段的时间，而不是实例化的时间
    send_time = models.DateTimeField(default=datetime.now)
    # send_time_test = models.DateTimeField(default=datetime.now())

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """
    首页轮播图
    """
    title = models.CharField(verbose_name='标题', max_length=100)
    image = models.ImageField(upload_to='banner/%Y/%m',
                              verbose_name='轮播图',
                              max_length=100)
    url = models.URLField(verbose_name='访问地址', max_length=200)
    index = models.IntegerField(verbose_name='序号', default=100)
    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name