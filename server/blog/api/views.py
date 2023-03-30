import json
from django.shortcuts import render
from django.db import transaction
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from ..models import Article, Article_Like, Comment
from rest_framework.permissions import IsAuthenticated
from account.authentication import JWTAuthentication
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import CursorPagination

class ArticlePagination(CursorPagination):
    page_size = 10
    ordering = 'createdAt'

class ArticleView(APIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = ArticlePagination

    @swagger_auto_schema(tags=['아티클 리스트'])
    def get(self, request) :
        try:
            articles = Article.objects.select_related('user').all().order_by('-createdAt')
        except Article.DoesNotExist : 
            return Response({'data': [], 'success' : True}, status=status.HTTP_200_OK)

        serializer = ArticleSerializer(articles, many=True)
        
        return Response({'data': serializer.data, 'success' : True}, status=status.HTTP_200_OK)


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
    def post(self, request) :
        authentication_classes = [JWTAuthentication]

        payload = JWTAuthentication.authenticate(self, request)
        user_id = payload[1]['id']
        
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

    def get_object(self, article_id: int, user_id:int) :
        try:
            return Article.objects.get(id=article_id, user_id= user_id)
        except Article.DoesNotExist:
            return Response({"success" : False, "data" : "다른 사람의 글을 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['아티클 상세페이지'])
    def get(self, request, article_id:int):
        # article = self.get_object(article_id)
        
        try:
            article = Article.objects.get(id = article_id)
        except Article.DoesNotExist:
            return Response({"success" : False, "data" : None}, status=status.HTTP_404_NOT_FOUND)


        # if not article: 
        #     return Response({"success" : False }, status=status.HTTP_400_BAD_REQUEST)
        
        
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
        user_id = user[1]['id']

        article = self.get_object(article_id, user_id)
        
        if not article :
            return Response({"success" : False, "data" : "다른 사람의 글을 삭제할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            with transaction.atomic() :
                article.delete()

            return Response({"success" : True}, status=status.HTTP_200_OK)

        except : 
            return Response({"success" : False}, status=status.HTTP_400_BAD_REQUEST)    

        
class CommentPagination(CursorPagination):
    page_size = 5
    ordering = 'createdAt'


class CommentView(APIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = CommentPagination


    @swagger_auto_schema(tags=['댓글 리스트'])
    def get(self, request, article_id : int):

        try : 
            comments = Comment.objects.filter(article_id=article_id).order_by('-createdAt')
        except Comment.DoesNotExist:
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
    def post(self, request, article_id):
        authentication_classes = [JWTAuthentication]

        payload = JWTAuthentication.authenticate(self, request)
        user_id = payload[1]['id']

        body = json.loads(request.body)
        body['article_id'] = article_id
        body['user_id'] = user_id

        serializer = self.serializer_class(data=body)

        if serializer.is_valid() :
            serializer.save()
            return Response({'data': serializer.data, 'success' : True}, status=status.HTTP_201_CREATED)
        
        else : 
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()


    def get_object(self, comment_id:int, user_id:int) :
        try :
            return Comment.objects.get(id = comment_id, user_id = user_id)
        except Comment.DoesNotExist:
            return Response({"success" : False, "data" : "다른 사람의 글을 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['댓글 상세페이지'])
    def get(self, request, comment_id : int, article_id:int) :
        try:
            comment = Comment.objects.get(id = comment_id, article_id = article_id)
        except Comment.DoesNotExist:
            return Response({"success" : False, "data" : None}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentDetailSerializer(comment)
        return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    @method_decorator(name = '댓글 수정하기', decorator=swagger_auto_schema(
        tags=['댓글 달기'], 
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'content' : openapi.Schema(type=openapi.TYPE_STRING, description='내용')
        }))
    )
    def patch(self, request, comment_id:int, article_id:int) :
        authentication_classes = [JWTAuthentication]

        payload = JWTAuthentication.authenticate(self, request)
        user_id = payload[1]['id']

        comment = self.get_object(comment_id, user_id)

        body = json.loads(request.body)

        with transaction.atomic() :
            serializer = self.serializer_class(comment, data=body)

        if serializer.is_valid():
            serializer.save()

            return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)
        
        else :
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ArticleLikeView(APIView):
    serializer_class = ArticleLikeSerializer
    queryset = Article_Like.objects.all()
    authentication_classes = [JWTAuthentication]


    @transaction.Atomic
    async def post(self, request, article_id : int) :
        payload = JWTAuthentication.authenticate(self, request)
        user_id = payload[1]['id']

        with transaction.atomic():
            serializer = await self.serializer_class({article_id, user_id})


        if serializer.is_valid():
            serializer.save()
        
            return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)

        else :
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
