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
    queryset = User.objects.all()


    def get(self, request):
        users = User.objects.all()
        print(users)

        serializer = self.serializer_class(users, many=True)
        print(serializer.data)
        return Response(
            {
                "status": "success",
                "users": serializer.data,
            }
        )

    @swagger_auto_schema(tags=['유저 생성'], request_body = BaseUserSeiralizer)
    def post(self, request):
        
        serializer = self.serializer_class(data=json.loads(request.body))
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "user" : serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else :
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
       