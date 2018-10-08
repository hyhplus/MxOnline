from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    """
    user base information
    """
    gender_choices = (
        ('male', '男'),
        ('female', '女')
    )

    nick_name = models.CharField(verbose_name='昵称', max_length=50, default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)