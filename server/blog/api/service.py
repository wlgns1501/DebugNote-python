from dataclasses import dataclass
from blog.models import Article
from django.db.models import Count, Case, When, Q
from django.db.models.functions import JSONObject
from article_like.models import Article_Like
from django.db import models

@dataclass
class DataDto:
    title : str
    content : str
    user_id : int

class Article_Service() :

    def get_count():
        return Article.objects.count()
    
    def get_articles(user_id : int or None) :
        return Article.objects.annotate(likes = JSONObject(count = Count('article_like', distinct=True), isliked= Case(When(Q(article_like__user = user_id)& ~Q(article_like__user=None), then=True), default=False , output_field=models.BooleanField()))).annotate(comments = Count('article_comment', distinct=True)).all().order_by('-created_at')

    def get_article(article_id: int):
        return Article.objects.get(id=article_id)
    
    def get_article_mine(article_id : int, user_id:int) :
        return Article.objects.get(id=article_id, user_id=user_id)
    
    def create_article(data : DataDto) :
        return Article.objects.create(
            title = data['title'],
            content = data['content'],
            user_id = data['user_id']
        )