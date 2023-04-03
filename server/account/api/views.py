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
from account import jwt_middleware
from .serializers import SignInSerializer, SignUpSeiralizer, UserSerializer
from ..models import User
from django.db import transaction
from django.utils.decorators import method_decorator
from account.jwt_middleware import JwtMiddleWare

class SignUpView(APIView):
    serializer_class = SignUpSeiralizer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=['유저 생성'], request_body = SignUpSeiralizer)
    def post(self, request):
        body = json.loads(request.body)


        with transaction.atomic() :
            serializer = self.serializer_class(data=body)
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
    middleware_classes = []

    @swagger_auto_schema(tags=['로그인'], request_body = SignInSerializer)
    def post(self, request) :
        
        body = json.loads(request.body)
    
        serializer = self.serializer_class(data=body)

        if serializer.is_valid() :
            response = JsonResponse({'data' : serializer.data, 'status' : status.HTTP_200_OK })
            response.set_cookie("access_token", serializer.data['token'], expires= datetime.now() + timedelta(days=2) )
            return response

        else :
            return Response({'data' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class SignOutView(APIView):
      
      @method_decorator(JwtMiddleWare)
      @swagger_auto_schema(tags=['로그아웃'])
      def post(self, request) :

        response = JsonResponse({"success" : True})
        response.delete_cookie('access_token')

        return response

class UserDetailView(APIView):
    serailizer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self, user_id:int) :
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @transaction.atomic
    @method_decorator(JwtMiddleWare)
    @swagger_auto_schema(tags=['개인 정보 수정'], request_body=UserSerializer)
    def patch(self, request, user_id:int):
        payload = JWTAuthentication.authenticate(self, request)
        payload_user_id = payload[1]['id']

        if payload_user_id != user_id :
            return Response({"success" : False, "data" : None, "message" : '다른 유저의 정보를 수정 할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        
        body = json.loads(request.body)
        user = self.get_object(user_id)
        
        if not user :
            return Response({"success" : False, "data" : None}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            serializer = self.serailizer_class(user, data=body)

        if serializer.is_valid():
            serializer.save()
            
            response = JsonResponse({'data' : serializer.data, 'status' : status.HTTP_200_OK })
            response.set_cookie("access_token", serializer.data['token'], expires= datetime.now() + timedelta(days=2) )
            return response

        else :
            return Response({'data' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    @method_decorator(JwtMiddleWare)
    @swagger_auto_schema(tags=['탈퇴'])
    def delete(self, request, user_id: int) :
        payload = JWTAuthentication.authenticate(self, request)
        payload_user_id = payload[1]['id']

        if payload_user_id != user_id :
            return Response({"success" : False, "data" : None, "message" : '다른 유저를 삭제할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


        user = self.get_object(user_id)

        if not user :
            return Response({"success" : False, "data" : None, 'message' : "해당 유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        try :
            with transaction.atomic():
                user.delete()
                return Response({"success" : True}, status=status.HTTP_200_OK)
        except :
            return Response({"success" : False}, status=status.HTTP_400_BAD_REQUEST)    





