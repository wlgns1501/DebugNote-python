from account.models import User
from django.db import models


# Create your models here.
class Article(models.Model) :
  id = models.AutoField(primary_key=True)
  title = models.CharField(default='', null=False, blank=False, max_length=200)
  content = models.CharField(default='', null=False, blank=False, max_length=500)
  user = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)


  REQUIRED_FIELDS = ['title', 'content', 'user']

  def __str__(self):
    return self.title

