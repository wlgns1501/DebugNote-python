from dataclasses import dataclass
import os
from typing import Dict, Union
import jwt
from account.models import User
from rest_framework.exceptions import AuthenticationFailed, ParseError

@dataclass
class JWT_TYPE : 
    id : int
    email : str
    exp : str


class JwtMiddleWare(object):

    def __init__(self, response) :
        self.response =  response

    
    def __call__(self, request):
        response = self.response(request)

        jwt_token = request.COOKIES.get('access_token')

        if jwt_token is None :
            raise AuthenticationFailed('로그인이 필요한 기능입니다.')


        try :
            payload : JWT_TYPE = self.decode_jwt(jwt_token)
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        email = payload.email

        if email is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.get_user_by_email(email)
        if user is None:
            raise AuthenticationFailed('회원가입을 한 유저가 아닙니다.')

        request.user = user

        return request
    
