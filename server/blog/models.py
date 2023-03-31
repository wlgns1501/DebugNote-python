from django.db import models
from account.models import User
import pgtrigger


class Article(models.Model) :
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='', null=False, blank=False)
    content = models.CharField(max_length=500, default='', null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model) :
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100, default='', null=False, blank=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)




# @pgtrigger.Func(
    # pgtrigger.(
    #     name = 'article_like_trigger',
    #     operation = pgtrigger.Insert
    #     when = pgtrigger.Before,
    #     func = 
    # )
# )
class Article_Like(models.Model) :
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_id')
    created_at = models.DateTimeField(auto_now=True)