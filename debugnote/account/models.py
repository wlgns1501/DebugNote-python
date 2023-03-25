from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, nickname, name, password=None):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
            name = name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, nickname, name, password=None):
        user = self.create_user(
            email,
            password = password,
            nickname = nickname,
            name = name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True )
    password = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email', 'password']


    # def __str__(self):
    #   return self.email
    
    def getPassword(email):
        user = User.objects.get(email=email)
        return user.password

    def get_user_by_email(email:str):
        user = User.objects.get(email=email)
        print(user)
        return user

    @property
    def token(self):
      return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
      dt = datetime.now() + timedelta(days=60)

      token = jwt.encode({
        'id' : self.id,
        'exp' : dt.utcfromtimestamp(dt.timestamp())
      },  settings.SECRET_KEY, algorithm='HS256')

      return token
