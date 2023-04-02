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
import psycopg2
from django.db.models.functions import Coalesce

class ArticleLikeView(APIView):
    serializer_class = ArticleLikeSerializer
    queryset = Article_Like.objects.all()
    authentication_classes = [JWTAuthentication]


    @transaction.atomic
    @swagger_auto_schema(tags=['아티클 좋아요'])
    def post(self, request, article_id : int) :
        payload = JWTAuthentication.authenticate(self, request)
        user_id : int = payload[1]['id']

        try :
            article = Article.objects.get(id=article_id)

        except Article.DoesNotExist :
            return Response({'data': '게시물이 존재하지 않습니다.', 'success' : False}, status=status.HTTP_404_NOT_FOUND)

        try :
            with connection.cursor() as cursor:
                cursor.callproc("article_like", (article_id, user_id ))
                data = cursor.fetchone()
                cursor.close()
        except (Exception, psycopg2.DatabaseError) as error :
            return Response({"success" : False, "data" : error }, status=status.HTTP_400_BAD_REQUEST)
        

        print(data)
        return Response({"success" : True, "data" : {"is_liked" : data[0], "article_id" : data[1]} }, status=status.HTTP_200_OK)
