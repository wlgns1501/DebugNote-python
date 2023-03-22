from rest_framework import serializers
from .models import User


class BaseUserSeiralizer(serializers.Serializer):
    email = serializers.CharField(help_text='email', required=True)
    password = serializers.CharField(help_text='password', required=True)
    
    class Meta:
        model = User
        fields = ["id", "email", "createdAt"]
