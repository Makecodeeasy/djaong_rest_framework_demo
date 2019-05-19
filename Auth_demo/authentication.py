# -*- coding:utf-8 -*- 
# author: yanzhengbin@bianfeng.com


from rest_framework.authentication import BaseAuthentication, BasicAuthentication
from rest_framework import exceptions

from Auth_demo.models import User, UserToken


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request._request.GET.get("username")
        print(username)
        user_obj = User.objects.filter(username=username).first()
        if user_obj:
            # user_id = user_obj.id
            token = request._request.GET.get("token")
            print(token)
            token_obj = UserToken.objects.filter(user=user_obj, token=token).first()
            if token_obj:
                return user_obj, None
            else:
                raise exceptions.AuthenticationFailed('用户认证失败.')
        else:
            raise exceptions.AuthenticationFailed('用户认证失败.')

    def authenticate_header(self, request):
        pass

