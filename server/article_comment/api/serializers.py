from django.utils import timezone
from rest_framework import serializers
from blog.models import *
from account.api.serializers import UserDtoSerializer
from article_comment.models import Article_Comment
from article_comment.api.service import Article_Comment_Service
<<<<<<< HEAD
from article_reply.api.serializers import ReplySerializer

=======
# from blog.api.serializers import ArticleDetailSerializer
from article_reply.api.serializers import ReplySerializer
>>>>>>> 64a0b6e07592e3bded869da50d58027b29cdb640

class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    article_id = serializers.IntegerField()
    user = UserDtoSerializer(read_only=True)


    def create(self, validated_data):
        content = validated_data['content']
        article_id = validated_data['article_id']
        user_id = validated_data['user_id']
        
        if not content :
            return serializers.ValidationError(
                '댓글을 입력하지 않았습니다.'
            )

        comment = Article_Comment_Service.create(validated_data)

        return comment
        

    class Meta:
        model= Article_Comment
        fields = ['id', 'content', 'user', 'article_id' , 'user_id', 'created_at', 'updated_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    article_id = serializers.IntegerField(write_only=True)
    article_reply = ReplySerializer(read_only=True, many=True)
    # user = serializers.StringRelatedField(read_only=True, many=False)
<<<<<<< HEAD
    article_reply = ReplySerializer(read_only=True, many=True)
    user = UserDtoSerialzer(read_only=True)
=======
    user = UserDtoSerializer(read_only=True)
>>>>>>> 64a0b6e07592e3bded869da50d58027b29cdb640



    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.updated_at= timezone.now()

        instance.save()
        return instance

    class Meta:
        model= Article_Comment
<<<<<<< HEAD
        fields = ['id', 'content', 'user', 'article_id' ,'article_reply' , 'user_id', 'created_at', 'updated_at']
=======
        fields = ['id', 'content', 'user', 'article_id' , 'user_id', 'article_reply' ,'created_at', 'updated_at']
>>>>>>> 64a0b6e07592e3bded869da50d58027b29cdb640
