from django.shortcuts import render
from .serializers import ArticleSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from ..models import Article
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class ArticleView(APIView):
    serializer_class = ArticleSerializer
    authentication_classes = [BasicAuthentication]
    

    def post(self, request) :
        token = request.COOKIES.get('access_token')
        print(token)
        return Response({"message" : "success"})



