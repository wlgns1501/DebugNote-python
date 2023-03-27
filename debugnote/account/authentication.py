from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from account.models import User

# User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get('access_token')

        if jwt_token is None:
            return None
        
        try:
            payload = jwt.decode(jwt_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()


        email = payload.get('email')
        if email is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.get_user_by_email(email)
        if user is None:
            raise AuthenticationFailed('User not found')
        
        return user, payload
    
