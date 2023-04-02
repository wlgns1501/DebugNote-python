from rest_framework.test import APITestCase, APIClient

from rest_framework.reverse import reverse
from account.models import User
from rest_framework import status
# Create your tests here.

class UserTestCase(APITestCase):
    def test_signup(self) :
        url = 'http://127.0.0.1:8000/auth/signup'
        data = {
            'email' : 'test@test.com',
            'password' : 'test',
            'nickname' : 'test'
        }
        
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
