from django.db import models
from account.models import User


class Article(models.Model) :
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='', null=False, blank=False)
    content = models.CharField(max_length=500, default='', null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)





