import json
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.reverse import reverse
from django.utils import timezone
from account.models import User
from rest_framework import status
from account.factory.user_factory import UserFactory
from account.api.views import SignUpView
# Create your tests here.

class SignUpTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('signup')
        self.user_factory = UserFactory
 
    
    def test_signup_with_duplicated_email(self):
        print('이메일 중복 테스트🚀')
        existed_user = self.user_factory.create(email='user@example.com')
        data = {
            'email' : existed_user.email,
            "nickname" : 'test',
            "password" : 'testtest',
        }

        response = self.client.post(self.url, data=data, format='json')        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                            "status": "fail",
                            "message": {
                                "email": [
                                "user의 email은/는 이미 존재합니다."
                                ]
                            }
                        })

    def test_signup_with_duplicated_nickname(self):
        print('닉네임 중복 테스트🚀')
        existed_user = self.user_factory.create(nickname='string')
        data = {
            'email' : 'test@test.com',
            "nickname" : existed_user.nickname,
            "password" : 'testtest',
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                            "status": "fail",
                            "message": {
                                "nickname": [
                                "user의 nickname은/는 이미 존재합니다."
                                ]
                            }
                        })
        
    def test_signup(self) :
        print('로그인 테스트🚀')
        data = {
            "email" : 'test@test.com',
            "nickname" : 'test',
            "password" : 'testtest'
        }

        # existed_user = User.objects.get(email=data['email'])

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, '회원가입 테스트')




