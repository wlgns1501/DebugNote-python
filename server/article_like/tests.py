from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.reverse import reverse
from rest_framework import status
from article_like.factory.article_like_factory import ArticleLikeFactory
from blog.factory.article_factory import ArticleFactory
from account.factory.user_factory import UserFactory

class LikeAritlceTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('article_like', args=[1])
        self.user = UserFactory.create(password='testtest')
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

    def test_get_no_article(self):
        
        response = self.client.post(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json_data['data'], '게시물이 존재하지 않습니다.')
        self.assertEqual(json_data['success'], False)

    def test_like_article_and_unlike_article(self):
        article = ArticleFactory.create(id=1)

        response = self.client.post(self.url)

        json_data = response.json()
        self.assertEqual(json_data['success'], True)
        self.assertEqual(json_data['data']['is_liked'], True)
        self.assertEqual(json_data['data']['liked_article_id'], 1)

        response = self.client.post(self.url)

        json_data = response.json()
        self.assertEqual(json_data['success'], True)
        self.assertEqual(json_data['data']['is_liked'], False)
        self.assertEqual(json_data['data']['liked_article_id'], 0)


    