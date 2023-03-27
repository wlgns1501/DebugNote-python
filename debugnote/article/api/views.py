from django.shortcuts import render
from rest_framework.views import APIView
from article.models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import json
from rest_framework.authentication import BasicAuthentication

class ArticleView(APIView) :
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get(self):
        articles = Article.objects.all()
        print(articles)
        return Response({
            "status" : "success",
            "articles" : articles,
            },
            status=status.HTTP_200_OK
            )

    @swagger_auto_schema(tags=['아티클 생성'], request_body=ArticleSerializer)
    def post(self, request):
      body = json.loads(request.body)

      serializer = self.serializer_class(data=body)
      if serializer.is_valid():
         serializer.save()
         return Response({
            "status" : "success",
            "article" : serializer.data
         },status=status.HTTP_201_CREATED)
      else :
         return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )