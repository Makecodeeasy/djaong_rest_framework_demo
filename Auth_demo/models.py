from django.db import models
from django.contrib.auth.models import AbstractUser   # 引入django的user表抽象类


class User(AbstractUser):
    """
    自定义的User表，继承了抽象类。可以基于该表做用户认证
    """
    user_type_choices = [
        (1, "普通用户"),
        (2, "VIP"),
        (3, "SVIP")
    ]
    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")
    # password = models.CharField(max_length=128)  # 可以不用定义，继承抽象类即可
    user_type = models.IntegerField(choices=user_type_choices, default=1, verbose_name="用户类型")


class UserToken(models.Model):
    user = models.OneToOneField(to="User", on_delete=True, verbose_name="用户")
    token = models.CharField(max_length=128, null=False, verbose_name="用户token")






