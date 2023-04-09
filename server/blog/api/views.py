import json
from django.shortcuts import render
from django.db import transaction, connection
from blog.api.service import Article_Service
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


class ArticlePagination(CursorPagination):
    page_size = 10
    ordering = 'created_at'


class ArticleView(APIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    article_repository = Article_Service

    @swagger_auto_schema(tags=['아티클 리스트'])
    def get(self, request) :
        try :
            article_counts = self.article_repository.get_count()
        except Article.DoesNotExist : 
            return Response({'data': [], 'success' : True}, status=status.HTTP_200_OK)

        try:
            articles = self.article_repository.get_articles()
        except Article.DoesNotExist : 
            return Response({'data': [], 'success' : True}, status=status.HTTP_200_OK)

        serializer = ArticleSerializer(articles, many=True)
        
        return Response({'count' : article_counts, 'articles' :serializer.data , 'success' : True}, status=status.HTTP_200_OK)


    
    @transaction.atomic
    @method_decorator( decorator=swagger_auto_schema(
            tags=['아티클 생성'], 
            request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'title' : openapi.Schema(type=openapi.TYPE_STRING, description='제목'),
                'content' : openapi.Schema(type=openapi.TYPE_STRING, description='내용')
            })))
    def post(self, request) :
        authentication_classes = [JWTAuthentication]
        user = JWTAuthentication.authenticate(self, request)
        
        user_id = user.id
        
        body = json.loads(request.body)
        body['user_id'] = user_id

        with transaction.atomic():
            serializer = self.serializer_class(data=body)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success" : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
    
        else :
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    serializer_class = ArticleDetailSerializer
    article_repository = Article_Service

    def get_object(self, article_id: int, user_id:int) :
        try:
            return self.article_repository.get_article_mine(article_id, user_id)
        except Article.DoesNotExist:
            return Response({"success" : False, "data" : "다른 사람의 글을 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['아티클 상세페이지'])
    def get(self, request, article_id:int):
        try:
            article = self.article_repository.get_article(article_id)
        except Article.DoesNotExist:
            return Response({"success" : False, "data" : None}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArticleDetailSerializer(article)
        return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)
    

    @transaction.atomic
    @method_decorator(name = '아티클 생성', decorator=swagger_auto_schema(
            tags=['아티클 생성'], 
            request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'title' : openapi.Schema(type=openapi.TYPE_STRING, description='제목'),
                'content' : openapi.Schema(type=openapi.TYPE_STRING, description='내용')
            }))
    )
    def patch(self, request, article_id : int):
        authentication_classes = [JWTAuthentication]

        user = JWTAuthentication.authenticate(self, request)
        user_id = user[1]['id']

        article = self.get_object(article_id, user_id)
        
        
        body = json.loads(request.body)

        with transaction.atomic():
            serializer = self.serializer_class(article, data=body)
        

        if serializer.is_valid(raise_exception=True) :
            serializer.save()

            return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)
        
        else :
            return Response({"success" : False, "data" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    @swagger_auto_schema(tags=['아티클 삭제하기'])
    def delete(self, request, article_id:int) :
        authentication_classes = [JWTAuthentication]

        user = JWTAuthentication.authenticate(self, request)
        user_id = user.id

        article = self.get_object(article_id, user_id)
        
        if not article :
            return Response({"success" : False, "data" : "다른 사람의 글을 삭제할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            with transaction.atomic() :
                article.delete()

            return Response({"success" : True}, status=status.HTTP_200_OK)

        except : 
            return Response({"success" : False}, status=status.HTTP_400_BAD_REQUEST)    

        