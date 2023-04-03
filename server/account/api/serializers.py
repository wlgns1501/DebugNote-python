from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
import bcrypt

from account.api.service import User_Service


def hashed_password(password : bytes) :
    return bcrypt.hashpw(password, bcrypt.gensalt())

def decoded_password(hashed_password : bytes) :
    return hashed_password.decode('utf-8')

class SignUpSeiralizer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    def create(self, validated_data):
        input_hashed_password:bytes = hashed_password(validated_data['password'].encode('utf-8'))
        input_decode_password:str = decoded_password(input_hashed_password)


        user:User = User.objects.create(
            email = validated_data['email'],
            password = input_decode_password,
            nickname = validated_data['nickname']
        )
        return user

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
        
        # if not user.is_active:
        #     raise serializers.ValidationError(
        #         'This user has been deactivated.'
        #     )

        # user = User.objects.get(email=email)
        # print(user)

      

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
    email = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 100, write_only=True)
    nickname = serializers.CharField(max_length = 100)
    # token = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        new_password : bytes = validated_data.get('password').encode('utf-8')
        hashed_new_password = hashed_password(new_password)
        decoded_new_password = decoded_password(hashed_new_password)

        instance.email = validated_data.get('email', instance.email)
        instance.password = decoded_new_password
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()

        return instance
    class Meta:
        model = User
        fields = ['id', 'email', 'password' ,'nickname']