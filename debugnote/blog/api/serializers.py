from rest_framework import serializers

from blog.models import Article



class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=500)
    user_id = serializers.IntegerField()

    def create(self, validated_data) :
        article = Article.objects.create(
            title = validated_data['title'],
            content = validated_data['content'],
            user = validated_data['user_id']
        )

        return article
