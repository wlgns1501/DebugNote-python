from rest_framework import serializers
from ..models import User
from django.contrib.auth import authenticate
from django.utils import timezone


class SignUpSeiralizer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            password = validated_data['password'],
            nickname = validated_data['nickname']
        )
        return user

    class Meta:
        model = User
        fields = ["id", "email", "nickname", "password", "token"]


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    nickname = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)



    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None : 
            raise serializers.ValidationError(
                '이메일을 입력하지 않았습니다.'
            )

        if password is None:
            raise serializers.ValidationError(
                'password를 입력하지 않았습니다.'
            )
        
        user = authenticate(username = email, password = password)
        print(user)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )


        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])


        return {
            'email' : user.email,
            'username' : user.nickname,
            'last_login' : user.last_login
        }
    


    class Meta :
        model = User
        fields = ["id", "email", "nickname", "password", "token"]






