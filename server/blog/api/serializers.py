from django.utils import timezone
from rest_framework import serializers
from blog.models import *
from account.api.serializers import UserSerializer
from article_like.api.serializers import ArticleLikeSerializer
from article_comment.api.serializers import *
from blog.api.service import ArticleRepository

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    user_id = serializers.IntegerField(write_only = True)
    created_at = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    article_like = ArticleLikeSerializer(many=True, read_only=True)
    article_comment = CommentDetailSerializer(many=True, read_only=True)
    
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

        article = ArticleRepository.create_article(validated_data)

        return article

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'user_id', 'user', 'article_like', 'article_comment']


class ArticleDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    article_like = ArticleLikeSerializer(read_only=True, many=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.updated_at= timezone.now()
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        instance.save()

        # return article
    class Meta :
        model = Article
        fields = ['id', 'title', 'content', 'created_at' , 'updated_at', 'user_id', 'user', 'article_like']
