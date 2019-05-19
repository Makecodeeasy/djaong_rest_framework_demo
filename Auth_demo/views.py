import time
import base64

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, \
    check_password  # 导入几个方法，用来加密password 和生成token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from Auth_demo.authentication import UserAuthentication  #  导入自定义用户认证类
from Auth_demo.models import User, UserToken


def make_token(username, timestamp):
    a_str = username + str(timestamp)
    return base64.b64encode(a_str.encode("utf-8")).decode("utf-8")


class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        return_data = {"code": 1001,
                       "msg": None}

        username = request.data.get("username")
        password = request.data.get("password")
        if username and password:
            encrypted_password = make_password(password)
            # 保存创建的用户到数据库
            user_type = request.data.get("user_type") or 1

            User.objects.create(username=username,
                                password=encrypted_password,
                                user_type=user_type)
            return_data["code"] = 1000
            return_data["msg"] = "创建用户成功, username={}".format(username)
            return_status = status.HTTP_201_CREATED
        else:
            return_data["msg"] = {"创建用户:{} 失败".format(username)}
            return_status = status.HTTP_400_BAD_REQUEST

        return Response(return_data, status=return_status)


class LoginView(APIView):
    """
    用户登录
    """

    def post(self, request, *args, **kwargs):
        return_data = {
            "code": 1000,
            "msg": None,
        }
        request_data = request.data
        username = request_data.get("username", "")
        password = request_data.get("password", "")
        # 检查username和password是否合法
        user = authenticate(username=username, password=password)
        if user:
            user_obj = User.objects.filter(username=username).first()
            timestamp = time.time()
            token = make_token(username, timestamp)
            # 保存token到UserToken表中，如果记录不存在，则create， 如果存在则update
            UserToken.objects.update_or_create(user=user_obj, defaults={"token": token})
            return_data["code"] = 1000
            return_data["msg"] = "认证成功"
            return_data["token"] = token
            ret_status = status.HTTP_200_OK
        else:
            return_data["code"] = 1001
            return_data["msg"] = "用户名或密码错误"
            ret_status = status.HTTP_400_BAD_REQUEST

        return Response(return_data, status=ret_status)


class OrderView(APIView):
    authentication_classes = [UserAuthentication, ]  # 申明使用的认证类

    def get(self, request, *args, **kwargs):
        all_order = [{"order_id": 1,
                      "goods": "apple",
                      "amount": 10,
                      "total_price": 25},
                     {"order_id": 2,
                      "goods": "banana",
                      "amount": 12,
                      "total_price": 18},
                     ]
        return Response(all_order, status=status.HTTP_200_OK)


