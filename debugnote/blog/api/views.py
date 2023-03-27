import json
from django.shortcuts import render
from .serializers import ArticleSerializer, ArticleDetailSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from ..models import Article
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from account.authentication import JWTAuthentication

class ArticleView(APIView):
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Article.objects.all()

    @swagger_auto_schema(tags=['아티클 리스트'])
    def get(self, request) :
        articles = Article.objects.all().prefetch_related('user')
        serializer = ArticleSerializer(articles, many=True)
        
        return Response({'data': serializer.data, 'success' : True}, status=status.HTTP_200_OK)


    @swagger_auto_schema(tags=['아티클 생성'], request_body=ArticleSerializer)
    def post(self, request) :
        user = JWTAuthentication.authenticate(self, request)
        body = json.loads(request.body)
        
        serializer = self.serializer_class(data=body)
        if serializer.is_valid():
            serializer.save()

            return Response({"success" : True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
    
        else :
            return Response({"success" : True, 'data' : serializer.errors}, status=status.HTTP_201_CREATED)


class ArticleDetailView(APIView):
    serializer_class = ArticleDetailSerializer
    authentication_classes = [JWTAuthentication]

    def get_object(self, article_id) :
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return None

    @swagger_auto_schema(tags=['아티클 상세페이지'])
    def get(self, request, article_id):
        article = self.get_object(article_id)
        
        if not article: 
            return Response({"success" : False }, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = ArticleDetailSerializer(article)
        return Response({"success" : True, "data" : serializer.data}, status=status.HTTP_200_OK)
        

