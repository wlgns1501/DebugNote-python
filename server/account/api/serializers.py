from psycopg2.errors import UniqueViolation
from django.db.utils import IntegrityError
from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
import bcrypt
from django.core.exceptions import ValidationError

from account.api.service import User_Service

class SignUpSeiralizer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length= 100)
    nickname = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    def create(self, validated_data):
        email = validated_data['email'],
        password = validated_data['password'],
        nickname = validated_data['nickname']

        try :
            user:User = User.objects.create(
                email = validated_data['email'],
                password = validated_data['password'],
                nickname = validated_data['nickname']
            )
            return user
        except IntegrityError as e :
            if 'account_user_email_key' in e.args[0] :
                raise serializers.ValidationError('중복된 이메일 입니다.')
            elif 'account_user_nickname_key' in e.args[0]:
                raise serializers.ValidationError('중복된 닉네임 입니다.')

    class Meta:
        model = User
        fields = ["id", "email", "nickname", "password"]


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        email:str = data.get('email', None)
        password:str = data.get('password', None)
        
        if email is None : 
            raise serializers.ValidationError(
                '이메일을 입력하지 않았습니다.'
            )

        if password is None:
            raise serializers.ValidationError(
                'password를 입력하지 않았습니다.'
            )
        try:
            user = User_Service.get_user_by_email(email=email)
        except User.DoesNotExist:
            user = None

        # 저장되어 있는 비밀번호
        user_password: str = user.password

        # 입력한 비밀번호
        input_password = password.encode('utf-8')
        check = bcrypt.checkpw(input_password, user_password.encode('utf-8'))

        if not check:
            raise serializers.ValidationError(
                '비밀 번호가 일치하지 않습니다.'
            )
        
        # access_token = User_Service.generate_jwt_token(user.id, user.email)
        # print(access_token)
        # user.token = access_token

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])


        
        return {
            'email' : user.email,
            'username' : user.nickname,
            'last_login' : user.last_login,
            'token' : user.token
        }

    class Meta :
        model = User
        fields = ["id", "email", "nickname" ,"password", "token", "last_login"]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 100)
    password = serializers.CharField(max_length = 100, write_only=True)
    nickname = serializers.CharField(max_length = 100)
    token = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        if instance.email != validated_data['email'] :
            instance.email = validated_data['email']
        
        if not bcrypt.checkpw(validated_data['password'].encode('utf-8'), instance.password.encode('utf-8')):
            instance.password = validated_data['password']

        if instance.nickname != validated_data['nickname'] :
            instance.nickname = validated_data['nickname']

        try :
            instance.save()
        except IntegrityError as e :
            if 'account_user_email_key' in e.args[0] :
                raise serializers.ValidationError('중복된 이메일 입니다.')
            elif 'account_user_nickname_key' in e.args[0]:
                raise serializers.ValidationError('중복된 닉네임 입니다.')

        return instance
    class Meta:
        model = User
        fields = ['id', 'email', 'password','token' ,'nickname']


class UserDtoSerializer(serializers.ModelSerializer) :
    email = serializers.EmailField(max_length = 100)
    nickname = serializers.CharField(max_length = 100)


    class Meta:
        model = User
        fields = ['id', 'email','nickname']

