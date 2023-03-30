from rest_framework import serializers

from article.models import Article


class ArticleSerializer(serializers.ModelSerializer) :
  title = serializers.CharField(max_length = 100)
  content = serializers.CharField(max_length=500)
  user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


  def create(self, validate_date):
    article = Article.objects.create(
      title = validate_date['title'],
      content = validate_date['content'],
      user = validate_date['user']
    )

    return article
  
  class Meta:
    model = Article
    fields = ['id','title', 'content', 'user']