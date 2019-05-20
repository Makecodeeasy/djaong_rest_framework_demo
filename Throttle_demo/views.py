from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Auth_demo.models import User
from Throttle_demo.throttle import UserListThrottle


class UserListView(APIView):
    throttle_classes = [UserListThrottle, ]

    def get(self, request, *args, **kwargs):
        user_dict = dict()
        users = User.objects.all()
        for user in users:
            user_id = user.id
            username = user.username
            user_dict[user_id] = username
        return Response(user_dict, status=status.HTTP_200_OK)

