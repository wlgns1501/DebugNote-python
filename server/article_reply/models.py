from django.db import models

from account.models import User
from article_comment.models import Article_Comment

# Create your models here.

class Reply(models.Model) :
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100, blank=False, null=False, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    comment = models.ForeignKey(Article_Comment, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_created=True, null=True)


    class Meta:
        db_table = 'article_reply'