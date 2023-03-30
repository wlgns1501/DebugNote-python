import json
from django.shortcuts import render
from django.db import transaction
from .serializers import ArticleSerializer, ArticleDetailSerializer
from .serializers import ArticleSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from ..models import Article
from rest_framework.permissions import IsAuthenticated
from account.authentication import JWTAuthentication

# class ArticleViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


class ArticleView(APIView):
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Article.objects.all()

    @swagger_auto_schema(tags=['아티클 리스트'])
    def get(self, request) :
        articles = Article.objects.select_related('user').all()
        
        serializer = ArticleSerializer(articles, many=True)
        
        return Response({'data': serializer.data, 'success' : True}, status=status.HTTP_200_OK)


    @transaction.atomic
    @swagger_auto_schema(tags=['아티클 생성'], request_body=ArticleSerializer)
    def post(self, request) :
        user = JWTAuthentication.authenticate(self, request)
        body = json.loads(request.body)
        
        with transaction.atomic():
            serializer = self.serializer_class(data=body)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"success" : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
    
        else :
            return Response({"success" : True, 'data' : serializer.errors}, status=status.HTTP_201_CREATED)


class ArticleDetailView(APIView):
    serializer_class = ArticleDetailSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self, article_id: int, user_id:int) :
        try:
            return Article.objects.get(id=article_id, user_id= user_id)
        except Article.DoesNotExist:
            return None

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
    @swagger_auto_schema(tags=['아티클 수정하기'], request_body=ArticleDetailSerializer)
    def patch(self, request, article_id : int):
        user = JWTAuthentication.authenticate(self, request)
        user_id = user[1]['id']

        article = self.get_object(article_id, user_id)
        
        if not article :
            return Response({"success" : False, "data" : "다른 사람의 글을 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

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

        
