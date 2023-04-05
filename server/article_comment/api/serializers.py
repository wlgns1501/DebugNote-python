from django.utils import timezone
from rest_framework import serializers
from blog.models import *
from account.api.serializers import UserSerializer
from article_comment.models import Article_Comment

# from blog.api.serializers import ArticleDetailSerializer


class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    article_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)


    def create(self, validated_data):
        content = validated_data['content']
        article_id = validated_data['article_id']
        user_id = validated_data['user_id']

        print(validated_data)

        if not content :
            return serializers.ValidationError(
                '댓글을 입력하지 않았습니다.'
            )

        comment = Article_Comment.objects.create(
            content = validated_data['content'],
            article_id = validated_data['article_id'],
            user_id = validated_data['user_id']
        )

        
        return comment

    class Meta:
        model= Article_Comment
        fields = ['id', 'content', 'user', 'article_id' , 'user_id', 'created_at', 'updated_at', 'article']


class CommentDetailSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    article_id = serializers.IntegerField(write_only=True)
    # user = serializers.StringRelatedField(read_only=True, many=False)
    user = UserSerializer(read_only=True)



    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.updated_at= timezone.now()

        instance.save()
        return instance

    class Meta:
        model= Article_Comment
        fields = ['id', 'content', 'user', 'article_id' , 'user_id', 'created_at', 'updated_at']