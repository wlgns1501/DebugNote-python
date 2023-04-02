from django.utils import timezone
from rest_framework import serializers
from blog.models import *
from account.api.serializers import UserSerializer
from article_like.models import Article_Like


class ArticleLikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    article_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)

    def post(self, validated_data) :
        article_id = validated_data['article_id']
        user_id = validated_data['user_id']

        if not article_id:
            return serializers.ValidationError(
                '댓글을 입력하지 않았습니다.'
            )
        if not user_id : 
            return serializers.ValidationError(
                '댓글을 입력하지 않았습니다.'
            )
        
        liked_article = Article_Like.objects.create(
            user_id = user_id,
            article_id = article_id
        )

        return liked_article
    
    class Meta:
        model=Article_Like
        fields = ['id', 'user_id', 'article_id', 'created_at']


