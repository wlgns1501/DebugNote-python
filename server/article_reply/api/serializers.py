from django.utils import timezone
from rest_framework import serializers
<<<<<<< HEAD
from article_reply.models import Reply
from account.api.serializers import UserDtoSerialzer
=======
from account.api.serializers import UserDtoSerializer
>>>>>>> 64a0b6e07592e3bded869da50d58027b29cdb640
from article_reply.api.service import Article_Reply_Service


class ReplySerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField(write_only=True)
    comment_id = serializers.IntegerField(write_only=True)
<<<<<<< HEAD
    user = UserDtoSerialzer(read_only=True)
=======
    user = UserDtoSerializer(read_only=True)
>>>>>>> 64a0b6e07592e3bded869da50d58027b29cdb640
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data) :
        content = validated_data['content']
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
        fields = ['id', 'content', 'created_at', 'user_id', 'comment_id', 'user']


class ReplyDetailSerializer(serializers.ModelSerializer) :
    content = serializers.CharField(max_length = 100)
    user_id = serializers.IntegerField(read_only=True)
    comment_id = serializers.IntegerField(read_only = True)
<<<<<<< HEAD
    user = UserDtoSerialzer(read_only=True)
=======
    user = UserDtoSerializer(read_only=True)
>>>>>>> 64a0b6e07592e3bded869da50d58027b29cdb640
    created_at = serializers.DateTimeField(read_only= True)
    updated_at =  serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data) :
        if not validated_data['content']:
            return serializers.ValidationError(
                '내용을 입력하지 않았습니다.'
            )
        
        instance.content = validated_data.get('content', instance.content)
        instance.updated_at = timezone.now()


        instance.save()
        return instance


    class Meta :
        model = Reply
        fields = ['id', 'content', 'user_id', 'comment_id' ,'user', 'created_at', 'updated_at']