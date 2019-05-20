
from Auth_demo.models import User, UserToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Permission_demo.permisssions import UserPermission
from django.contrib.auth.hashers import make_password


class UserView(APIView):
    """
    用户增删改查
    """
    permission_classes = [UserPermission, ]    # 权限控制
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user_type = request.data.get("user_type", 1)
        if username and password:
            encrypted_password = make_password(password)
            User.objects.create(username=username, password=encrypted_password, user_type=user_type)
            return Response("用户创建成功: username={}".format(username), status=status.HTTP_201_CREATED)
        else:
            return Response("用户创建失败: 用户名或密码不能为空", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username:
            user_obj = User.objects.filter(username=username).first()
            if user_obj:
                user_obj.delete()
                return Response("删除用户:{}成功".format(username), status=status.HTTP_200_OK)
            else:
                return Response("用户:{}未找到".format(username), status=status.HTTP_404_NOT_FOUND)

        return Response("用户名不能为空", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user_type = request.data.get("user_type")
        user_obj = User.objects.filter(username=username).first()

        if user_obj:
            if not user_type:
                user_type = user_obj.user_type
            encrypted_password = user_obj.password if not password else make_password(password)
            User.objects.filter(username=username).update(password=encrypted_password, user_type=user_type)
            # user_obj.update(password=encrypted_password, user_type=user_type)
            return Response("用户{}修改成功".format(username))
        return Response("用户:{}未找到".format(username), status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        user_dict = dict()
        users = User.objects.all()
        for user in users:
            user_id = user.id
            username = user.username
            user_dict[user_id] = username

        return Response(user_dict, status=status.HTTP_200_OK)



