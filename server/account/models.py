import bcrypt
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save

def hashed_password(password : bytes) :
    return bcrypt.hashpw(password, bcrypt.gensalt())

def decoded_password(hashed_password : bytes) :
    return hashed_password.decode('utf-8')


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

    @property
    def token(self):
      return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
      dt = datetime.now() + timedelta(days=60)

      token = jwt.encode({
        'id' : self.id,
        'email' : self.email,
        'exp' : dt.utcfromtimestamp(dt.timestamp())
      },  settings.SECRET_KEY, algorithm='HS256')

      return token

@receiver(pre_save, sender=User)
def user_encode_password_pre_save(sender, instance ,**kwargs):
    if not instance.id :
        input_hashed_password:bytes = hashed_password(instance.password.encode('utf-8'))
        input_decode_password:str = decoded_password(input_hashed_password)

        instance.password = input_decode_password
    
    
    elif bcrypt.checkpw(instance.password.encode('utf-8'), User.objects.get(id= instance.id).password.encode('utf-8')) == False:
        updated_hashed_password  = hashed_password(instance.password.encode('utf-8'))
        updated_decoded_password = decoded_password(updated_hashed_password)
        
        instance.password = updated_decoded_password
        
        