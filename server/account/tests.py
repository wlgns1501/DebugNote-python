import json
import os
import bcrypt
import jwt
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.reverse import reverse
from django.utils import timezone
from account.models import User
from rest_framework import status
from account.factory.user_factory import UserFactory
from account.api.views import SignUpView
from rest_framework import serializers
from dataclasses import dataclass


@dataclass
class JWT_TYPE : 
    id : int
    email : str
    exp : str

def hashed_password(password : bytes) :
    return bcrypt.hashpw(password, bcrypt.gensalt())

def decoded_password(hashed_password : bytes) :
    return hashed_password.decode('utf-8')

def decode_jwt(jwt_token : str) -> JWT_TYPE :
    return jwt.decode(jwt_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

class SignUpTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('signup')
        self.user_factory = UserFactory
        self.user = {
            'email' : 'test@test.com',
            'password' : 'testtest',
            'nickname' : 'test'
        }

    def test_signup_with_validate_check_email(self):
        data = {
            'email' : 'test',
            'password' : 'testtest',
            'nickname' : 'test'
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                            "email": [
                                "유효한 이메일 주소를 입력하십시오."
                            ]
                        },'이메일 형식 체크 테스트🚀')

    def test_signup_with_null_check_email(self):
        data = {
            'email' : None,
            'password' : 'testtest',
            'nickname' : 'test'
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertIsNone(data['email'], 'email이 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'status 코드 400인지 확인')
        self.assertEqual(response.data, {
                                "email": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        }, '이메일 null 체크 테스트🚀')

    def test_signup_with_null_check_nickname(self):
        data = {
            'email' : 'test@test.com',
            'password' : 'testtest',
            'nickname' : None
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertIsNone(data['nickname'], 'nickname이 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                                "nickname": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        },'닉네임 null 체크 테스트🚀')
        
    def test_signup_with_null_check_nickname(self):
        data = {
            'email' : 'test@test.com',
            'password' : None,
            'nickname' : 'test'
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertIsNone(data['password'], 'password가 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, '비밀번호 null 체크 테스트🚀')
        self.assertEqual(response.data, {
                                "password": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        }, '비밀번호 null 체크 테스트🚀')
    
    def test_signup_with_duplicated_email(self):
        existed_user = self.user_factory.create(email='user@example.com')
        self.user['email'] = existed_user.email

        response = self.client.post(self.url, data=self.user, format='json')        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '중복된 이메일 입니다.', '이메일 중복 테스트🚀')

    def test_signup_with_duplicated_nickname(self):
        existed_user = self.user_factory.create(nickname='string')
        self.user['nickname'] = existed_user.nickname

        response = self.client.post(self.url, data=self.user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '중복된 닉네임 입니다.', '닉네임 중복 테스트🚀')
        
    def test_signup(self) :
        data = {
            "email" : 'test@test.com',
            "nickname" : 'test',
            "password" : 'testtest'
        }

        response = self.client.post(self.url, data=data, format='json')
        user = User.objects.get(email=data['email'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, '회원가입 테스트🚀')
        self.assertEqual(data['email'], user.email)
        self.assertEqual(data['nickname'], user.nickname)
        self.assertTrue(bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')))

class SignInTestAPIViewTestCase(APITestCase):
    def setUp(self) : 
        self.factory = APIRequestFactory()
        self.url = reverse('signin')
        self.user = UserFactory.create(password='testtest')
    
    def test_signin_with_null_check_email(self):
        data = {
            'email' : None,
            'password' : 'testtest',
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertIsNone(data['email'], 'email이 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                                "email": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        }, '로그인 이메일 null 체크 테스트🚀')
        
    def test_signin_with_null_check_nickname(self):
        data = {
            'email' : 'test@test.com',
            'password' : None
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertIsNone(data['password'], 'password가 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                                "password": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        }, '로그인 비밀번호 null 체크 테스트🚀')

    def test_is_user(self) :
        data = {
            'email' : 'test11@test.com',
            'password' : self.user.password
        }

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=data['email'])
        
    def test_signin(self) :
        data = {
            'email' : self.user.email,
            'password' : 'testtest'
        }
        
        response = self.client.post(self.url, data=data, format='json')
        res = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.cookies['access_token'].value)


class SignOutTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('signout')
        self.user = UserFactory.create(password='testtest')
        self.response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

    def test_signout(self):
        response = self.client.post(self.url)

        self.assertEqual(response.cookies['access_token'].value, '')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['success'], True)


class UpateUserInfoAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('user')
        self.user_factory = UserFactory
        self.user = UserFactory.create(password='testtest')
        self.response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

    def test_update_user_info_with_validate_check_email(self):
        data = {
            'email' : 'test',
            'password' : 'testtest',
            'nickname' : 'test'
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                            "email": [
                                "유효한 이메일 주소를 입력하십시오."
                            ]
                        },'이메일 형식 체크 테스트🚀')

    def test_update_user_info_with_null_check_email(self):
        data = {
            'email' : None,
            'password' : 'testtest',
            'nickname' : 'test'
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertIsNone(data['email'], 'email이 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'status 코드 400인지 확인')
        self.assertEqual(response.data, {
                                "email": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        }, '이메일 null 체크 테스트🚀')

    def test_update_user_info_with_null_check_nickname(self):
        data = {
            'email' : 'test@test.com',
            'password' : 'testtest',
            'nickname' : None
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertIsNone(data['nickname'], 'nickname이 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                                "nickname": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        },'닉네임 null 체크 테스트🚀')
        
    def test_update_user_info_with_null_check_nickname(self):
        data = {
            'email' : 'test@test.com',
            'password' : None,
            'nickname' : 'test'
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertIsNone(data['password'], 'password가 None인지 확인')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, '비밀번호 null 체크 테스트🚀')
        self.assertEqual(response.data, {
                                "password": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        }, '비밀번호 null 체크 테스트🚀')
    
    def test_update_user_info_with_duplicated_email(self):
        existed_user = self.user_factory.create(email='user@example.com')
        self.user.email = existed_user.email
        data = {
            'email' : self.user.email,
            'password' : 'testtest',
            'nickname' : self.user.nickname
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '중복된 이메일 입니다.', '이메일 중복 테스트🚀')

    def test_update_user_info_with_duplicated_nickname(self):
        existed_user = self.user_factory.create(nickname='string')
        self.user.nickname = existed_user.nickname
        data = {
            'email' : self.user.email,
            'password' : 'testtest',
            'nickname' : self.user.nickname
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], '중복된 닉네임 입니다.', '닉네임 중복 테스트🚀')
      
    def test_update_user_info(self):
        data = {
            'email' : 'wlgns1501@gmail.com',
            'password' : 'gkstlsyjh116!',
            'nickname' : 'jihun'
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.nickname, data['nickname'])

        access_token = response.cookies['access_token'].value

        payload = decode_jwt(access_token)

        self.assertEqual(user.id, payload['id'])
        self.assertEqual(user.email, payload['email'])

class DeleteUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('user')
        self.user = UserFactory.create(password='testtest')
        self.response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

    # def test_find_user(self) :
    #     payload = self.response.cookies['access_token'].value
    #     user_id = payload[0].id

    #     user = User.objects.get(id=user_id)



    def test_delete_user(self):
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.cookies['access_token'].value

        self.assertEqual(access_token, '')


