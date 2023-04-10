import json
from django.shortcuts import render
from django.db import transaction, connection
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.authentication import JWTAuthentication
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import CursorPagination
from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models.functions import Coalesce
        

class CommentPagination(CursorPagination):
    page_size = 5
    ordering = 'created_at'


class CommentView(APIView):
    serializer_class = CommentSerializer
    queryset = Article_Comment.objects.all()
    pagination_class = CommentPagination


    @swagger_auto_schema(tags=['댓글 리스트'])
    def get(self, request, article_id:int):

        try : 
            comments = Article_Comment.objects.filter(article_id=article_id).order_by('-created_at')
        except Article_Comment.DoesNotExist:
            return Response({'data': [], 'success' : True}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(comments, many=True)      

        return Response({'data': serializer.data, 'success' : True}, status=status.HTTP_200_OK)

    @transaction.atomic
    @method_decorator(name = '댓글 달기', decorator=swagger_auto_schema(
        tags=['댓글 달기'], 
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'content' : openapi.Schema(type=openapi.TYPE_STRING, description='내용')
        }))
    )
    def post(self, request, article_id: int):
        authentication_classes = [JWTAuthentication]
        user = JWTAuthentication.authenticate(self, request)
        
        user_id = user[0].id

        body = json.loads(request.body)
        body['article_id'] = article_id
        body['user_id'] = user_id

        with transaction.atomic() :
            serializer = self.serializer_class(data=body)
            
        if serializer.is_valid() :
            serializer.save()
            return Response({'data': serializer.data, 'success' : True}, status=status.HTTP_201_CREATED)
        
        else : 
            print(serializer.error_messages)
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    serializer_class = CommentDetailSerializer
    queryset = Article_Comment.objects.all()


    def get_object(self, comment_id:int, user_id:int) :
        try :
            return Article_Comment.objects.get(id = comment_id, user_id = user_id)
        except Article_Comment.DoesNotExist:
            return Response({"success" : False, "data" : "다른 사람의 글을 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['댓글 상세페이지'])
    def get(self, request, comment_id : int, article_id:int) :
        try:
            comment = Article_Comment.objects.get(id = comment_id, article_id = article_id)
        except Article_Comment.DoesNotExist:
            return Response({"success" : False, "data" : None}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentDetailSerializer(comment)
        return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    @method_decorator(name = '댓글 수정하기', decorator=swagger_auto_schema(
        tags=['댓글 수정하기'], 
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'content' : openapi.Schema(type=openapi.TYPE_STRING, description='내용')
        }))
    )
    def patch(self, request, comment_id:int, article_id:int) :
        authentication_classes = [JWTAuthentication]

        user = JWTAuthentication.authenticate(self, request)
        user_id = user[0].id

        comment = self.get_object(comment_id, user_id)

        body = json.loads(request.body)

        with transaction.atomic() :
            serializer = self.serializer_class(comment, data=body)

        if serializer.is_valid():
            serializer.save()

            return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)
        
        else :
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(tags=['댓글 삭제'])
    def delete(self, request, comment_id : int, article_id : int):
        authentication_classes = [JWTAuthentication]

        user = JWTAuthentication.authenticate(self, request)
        user_id = user[0].id

        comment = self.get_object(comment_id, user_id)

        with transaction.atomic():
            comment.delete()
            return Response({"success" : True}, status=status.HTTP_200_OK)

