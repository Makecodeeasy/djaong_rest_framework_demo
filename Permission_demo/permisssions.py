# -*- coding:utf-8 -*- 
# author: yanzhengbin@bianfeng.com

from rest_framework.permissions import BasePermission
from Auth_demo.models import User

# 权限控制字典，如果是生产环境，则放入到数据库为佳
perm = {1: ("GET", ), 2: ("GET", "POST"), 3: {"GET", "POST", "PUT", "DELETE"}}


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        username = request.data.get("admin_user")
        user_obj = User.objects.filter(username=username).first()
        user_type = user_obj.user_type

        allow_method = perm.get(user_type, tuple())
        request_method = request.method
        if request_method in allow_method:
            return True
        else:
            return False
