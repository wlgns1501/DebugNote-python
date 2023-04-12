from datetime import datetime, timedelta
import json
import math
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
import bcrypt
from account.authentication import JWTAuthentication
from .serializers import SignInSerializer, SignUpSeiralizer, UserSerializer
from ..models import User
from django.db import transaction
from drf_yasg import openapi
from django.utils.decorators import method_decorator

class SignUpView(APIView):
    serializer_class = SignUpSeiralizer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=['유저 생성'], request_body = SignUpSeiralizer)
    def post(self, request):
        body = json.loads(request.body)
        

        with transaction.atomic() :
            serializer = self.serializer_class(data=body)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save()
            
            return Response(
                {"user" : serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else :
            return Response(
                { "message": serializer.errors },
                status=status.HTTP_400_BAD_REQUEST,
            )
   
                
class SignInView(APIView) :
    serializer_class = SignInSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=['로그인'], request_body = SignInSerializer)
    def post(self, request) :
        
        body = json.loads(request.body)
    
        serializer = self.serializer_class(data=body)
        
        if serializer.is_valid(raise_exception=True) :
            response = JsonResponse({'data' : serializer.data, 'status' : status.HTTP_200_OK })
            response.set_cookie("access_token", serializer.data['token'], expires= datetime.now() + timedelta(days=2) )
            return response

        else :
            return Response({'data' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class SignOutView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(tags=['로그아웃'])
    def post(self, request) :

        response = JsonResponse({"success" : True})
        response.delete_cookie('access_token')

        return response

class UserDetailView(APIView):
    serailizer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()

    def get_object(self, user_id:int) :
        return User.objects.get(id=user_id)
      

    @transaction.atomic
    @method_decorator(decorator=swagger_auto_schema(
            tags=['개인정보 수정하기'], 
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT, 
                properties={
                    'email' : openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                    'nickname' : openapi.Schema(type=openapi.TYPE_STRING, description='nickname'),
                    'password' : openapi.Schema(type=openapi.TYPE_STRING, description='password'),
    })))
    def patch(self, request):
        user = JWTAuthentication.authenticate(self, request)
        user_id = user[0].id

        body = json.loads(request.body)
        user = self.get_object(user_id)

        with transaction.atomic():
            serializer = self.serailizer_class(user, data=body)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = JsonResponse({'data' : serializer.data, 'status' : status.HTTP_200_OK })
            response.set_cookie("access_token", serializer.data['token'], expires= datetime.now() + timedelta(days=2) )
            return response

        else :
            return Response({'data' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    @swagger_auto_schema(tags=['탈퇴'])
    def delete(self, request) :
        user = JWTAuthentication.authenticate(self, request)
        user_id = user[0].id

        user = self.get_object(user_id)

        if not user :
            return Response({'message' : "해당 유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        try :
            with transaction.atomic():
                user.delete()
                
                response = JsonResponse({"success" : True}, status=status.HTTP_200_OK)
                response.delete_cookie('access_token')
                return response
        except :
            return Response({"success" : False}, status=status.HTTP_400_BAD_REQUEST)    