from django.db import models
from account.models import User
from blog.models import Article

# Create your models here.

class Article_Like(models.Model) :
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_like')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_like')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'article_like'