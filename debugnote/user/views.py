import json
import math
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import BaseUserSeiralizer
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from .open_api_params import signup_params


class UserView(APIView):
    serializer_class = BaseUserSeiralizer
    qureyset = User.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        users = User.objects.all()
        total_users = users.count()

        serializer = self.serializer_class(users[start_num:end_num], many=True)
        return Response(
            {
                "status": "success",
                "total": total_users,
                "page": page_num,
                "last_page": math.ceil(total_users / limit_num),
                "users": serializer.data,
            }
        )

    @swagger_auto_schema(tags=['유저 생성'], request_body = BaseUserSeiralizer)
    def post(self, request):
        try :
            data = json.loads(request.body)
            user = User(email = data['email'], password= data['password'])
            user.save()
            print(user)
            return Response(
                {"status": "success", "user" : user},
                status=status.HTTP_201_CREATED,
            )
        except :
            return Response(
                {"status": "fail", "message": "error"},
                status=status.HTTP_400_BAD_REQUEST,
            )
