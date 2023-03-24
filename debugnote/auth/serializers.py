from rest_framework import serializers
from .models import User


class BaseUserSeiralizer(serializers.Serializer):
    email = serializers.CharField(help_text='email', required=True)
    password = serializers.CharField(help_text='password', required=True)
    

    def create(self, validated_data):
        return User(**validated_data)

    def save(self):
        email = self.validated_data['email'];
        password = self.validated_data['password']

    class Meta:
        model = User
        fields = ["id", "email", "createdAt"]
