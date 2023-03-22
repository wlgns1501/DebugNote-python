from django.db import models


# Create your models here.
class User(models.Model):
    id: models.IntegerField(primary_key=True, auto_created=True)
    email: models.CharField(unique=True, null=False, blank=False, max_length=200)
    password: models.CharField(null=False, blank=False, max_length=True)
    createdAt: models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_user"

    def __str__(self):
        return self.email


    # def get_user(self) :
