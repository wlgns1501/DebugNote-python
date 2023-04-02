from django.db import models
from account.models import User
from blog.models import Article

# Create your models here.
class Article_Comment(models.Model) :
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100, default='', null=False, blank=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_comment')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'article_comment'