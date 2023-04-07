from article_reply.models import Reply
from rest_framework import serializers
from account.api.serializers import UserSerializer
from article_reply.api.service import Article_Reply_Service

class ReplySerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField(write_only=True)
    comment_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)



    def create(self, validated_data) :
        content = validated_data['content']
        article_id = validated_data['article_id']
        user_id = validated_data['user_id']
        comment_id = validated_data['comment_id']

        if content is None :
            return serializers.ValidationError(
                '대댓글을 입력하지 않았습니다.'
            )

        reply = Reply.objects.create(
            content = content,
            user_id = user_id,
            comment_id = comment_id
        )

        return reply

    class Meta:
        model = Reply
        fields = ['id', 'content', 'created_at', 'updated_at', 'user_id', 'comment_id', 'user']
