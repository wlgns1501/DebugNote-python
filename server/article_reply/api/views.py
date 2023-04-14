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
from article_reply.api.serializers import ReplyDetailSerializer

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
        user_id = user[0].id

        body = json.loads(request.body)
        body['article_id'] = article_id
        body['user_id'] = user_id
        body['comment_id'] = comment_id

        with transaction.atomic() :
            serializer = self.serializer_class(data=body)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data' : serializer.data, 'success' : True}, status=status.HTTP_201_CREATED)
        
        else :
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ReplyDetailView(APIView) :
    serializer_class = ReplyDetailSerializer
    queryset = Reply.objects.all()

    def get_one(self, comment_id:int, reply_id:int, user_id : int) :
        try:
            return  Article_Reply_Service.get_by_user(comment_id,reply_id, user_id)
        except Reply.DoesNotExist:
            return None
    
    @swagger_auto_schema(tags=['대댓글 상세페이지'])
    def get(self, request, article_id: int ,comment_id: int ,reply_id:int) :
        try:
            article = Article_Reply_Service.get(comment_id,reply_id)
        except Reply.DoesNotExist:
            return Response({"success" : False, 'data' : '대댓글이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(article)

        return Response({'data' : serializer.data, 'success' : True}, status=status.HTTP_200_OK)

    @transaction.atomic
    @method_decorator(name = '대댓글 수정', decorator=swagger_auto_schema(
        tags=['대댓글 수정'], 
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'content' : openapi.Schema(type=openapi.TYPE_STRING, description='내용')
        }))
    )
    def patch(self, request, article_id : int, comment_id : int, reply_id : int) :
        authentication_classes = [JWTAuthentication]

        user = JWTAuthentication.authenticate(self, request)
        user_id = user[0].id

        reply = self.get_one(comment_id, reply_id, user_id)

        if reply is None :
            return Response({"success" : False, "data" : "다른 사람의 글을 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        body = json.loads(request.body)

        with transaction.atomic():
            serializer = self.serializer_class(reply, data=body)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data' : serializer.data, 'success' : True}, status=status.HTTP_200_OK)

        else :
            return Response({"success" : False, 'data' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(tags=['대댓글 삭제'])
    def delete(self,request, article_id : int, comment_id: int, reply_id:int) :
        authentication_classes = [JWTAuthentication]

        user = JWTAuthentication.authenticate(self, request)
        user_id = user[0].id

        reply = self.get_one(comment_id, reply_id, user_id)

        if reply is None:
            return Response({"success" : False, "data" : "다른 사람의 글을 삭제할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            reply.delete()
            return Response({"success" : True}, status=status.HTTP_200_OK)
        