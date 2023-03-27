from rest_framework import serializers
from blog.models import Article



class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    user_id = serializers.IntegerField()
    createdAt = serializers.DateField(read_only=True)
    user = serializers.StringRelatedField(many=False, read_only=True)

    def create(self, validated_data) :
        article = Article.objects.create(
            title = validated_data['title'],
            content = validated_data['content'],
            user_id = validated_data['user_id']
        )

        return article

    # def __str__(self):
    #     return self.title

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'createdAt', 'user_id', 'user']


class ArticleDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    updatedAt = serializers.DateTimeField(read_only=True)


    # def get(self, validated_data):
        


    class Meta :
        model = Article
        fields = ['id', 'title', 'content', 'updatedAt', 'user_id']
    
        