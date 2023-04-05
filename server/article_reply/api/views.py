import json
from django.db import transaction
from django.shortcuts import render
from rest_framework.views import APIView
from article_reply.models import Reply
from article_reply.api.serializers import ReplySerializer
from article_reply.api.service import Article_Reply_Service
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from account.authentication import JWTAuthentication



class ReplyView(APIView) :
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    article_reply_service = Article_Reply_Service


    @swagger_auto_schema(tags=['대댓글 리스트'])
    def get(self, request, article_id : int, comment_id: int) :
        replies = self.article_reply_service.get_all(article_id, comment_id)
        
        if replies is None :
            return Response({'data': [], 'success' : True}, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(replies, many=True)
    
        return Response({'data' : serializer.data, 'success' : True}, status=status.HTTP_200_OK)

    @transaction.atomic
    @method_decorator(name = '대댓글 달기', decorator=swagger_auto_schema(
        tags=['대댓글 달기'], 
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'content' : openapi.Schema(type=openapi.TYPE_STRING, description='내용')
        }))
    )
    def post(self, request, article_id:  int, comment_id:int) :
        authentication_classes = [JWTAuthentication]

        user = JWTAuthentication.authenticate(self, request)
        user_id = user.id

        body = json.loads(request.body)
        body['article_id'] = article_id
        body['user_id'] = user_id

        with transaction.atomic() :
            serializer = self.serializer_class(data=body)

        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'success' : True}, status=status.HTTP_201_CREATED)
        
        else :
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ReplyDetailView(APIView) :
    def get() :
        return None