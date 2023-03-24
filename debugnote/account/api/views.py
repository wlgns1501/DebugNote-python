import json
import math
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import User

from .serializers import SignInSerializer, SignUpSeiralizer
from rest_framework.views import APIView
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
import bcrypt


class SignUpView(APIView):
    serializer_class = SignUpSeiralizer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=['유저 생성'], request_body = SignUpSeiralizer)
    def post(self, request):
        body = json.loads(request.body)

        hashed_password = bcrypt.hashpw(body['password'].encode('utf-8'), bcrypt.gensalt())

        decode_password = hashed_password.decode('utf-8')

        body['password'] = decode_password
        
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
        
       


class SignInView(APIView) :
    serializer_class = SignInSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=['로그인'], request_body = SignInSerializer)
    def signin(self, request) :
        body = json.loads(request.body)

        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)