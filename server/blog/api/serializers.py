from django.utils import timezone
from rest_framework import serializers
from blog.models import Article
from account.api.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    user_id = serializers.IntegerField(write_only = True)
    createdAt = serializers.DateTimeField(read_only=True)
    user = UserSerializer(many=False, read_only=True)

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

        article = Article.objects.create(
            title = validated_data['title'],
            content = validated_data['content'],
            user_id = validated_data['user_id']
        )

        return article

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'createdAt', 'user_id', 'user']


class ArticleDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    createdAt = serializers.DateTimeField(read_only = True)
    updatedAt = serializers.DateTimeField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    user = UserSerializer(many=False, read_only=True)
    

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.updatedAt= timezone.now()
        instance.save()
        return instance
        

    def delete(self, instance):
        instance.delete()
        instance.save()


        # return article
    class Meta :
        model = Article
        fields = ['id', 'title', 'content', 'createdAt' , 'updatedAt', 'user', 'user_id']
    
        