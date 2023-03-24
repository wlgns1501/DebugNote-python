from django.db import models

# Create your models here.
class User(models.Model):
    email: models.CharField(max_length=200)
    password: models.CharField(max_length=100)
    createdAt: models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
