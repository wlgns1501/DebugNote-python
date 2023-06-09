from django.utils import timezone
from rest_framework import serializers
from blog.models import *
# from account.api.serializers import UserSerializer
from article_like.api.serializers import ArticleLikeSerializer
from article_comment.api.serializers import *
from blog.api.service import Article_Service
from account.api.serializers import UserDtoSerializer


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    user_id = serializers.IntegerField(write_only = True)
    created_at = serializers.DateTimeField(read_only=True)
    user = UserDtoSerializer(read_only=True)
    likes = serializers.JSONField(read_only=True)
    comments = serializers.IntegerField(read_only =True)
    isLiked = serializers.BooleanField(read_only=True)
    
    def create(self, validated_data) :
        title = validated_data['title']
        content = validated_data['content']
        user_id = validated_data['user_id']

        if title is None :
            return serializers.ValidationError(
                '제목을 입력하지 않았습니다.'
            )

        if content is None :
            return serializers.ValidationError(
                '본문을 입력하지 않았습니다.'
            )
        
        if user_id is None :
            return serializers.ValidationError(
                '유저 Id를 입력하지 않았습니다.'
            )

        article = Article_Service.create_article(validated_data)

        return article

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'user_id', 'user', 'likes', 'comments', 'isLiked']


class ArticleDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only=True)
    user = UserDtoSerializer(read_only=True)
    article_like = ArticleLikeSerializer(read_only=True, many=True)
    article_comment = CommentSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):

        if instance.title != validated_data['title'] :
            instance.title = validated_data['title']

        if instance.content != validated_data['content'] :
            instance.content = validated_data['content']

        instance.updated_at= timezone.now()
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        instance.save()

        # return article
    class Meta :
        model = Article
        fields = ['id', 'title', 'content', 'created_at' , 'updated_at', 'user', 'article_like', 'article_comment']
