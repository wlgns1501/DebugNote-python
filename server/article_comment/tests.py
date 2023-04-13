import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from blog.factory.article_factory import ArticleFactory
from rest_framework import status
from account.factory.user_factory import UserFactory
from blog.models import Article
from article_comment.factory.article_comment_factory import ArticleCommentFactory


class GetArticleCommentListTestAPIViewTestCase(APITestCase):
    def setUp(self):
        # self.article = ArticleFactory.create()
        self.article_comment_factory = ArticleCommentFactory
        self.url = reverse('comment', args=[1])

    def test_get_no_article_comments_list(self):
        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_data['data'], [])
        self.assertEqual(json_data['success'], True)

    def test_get_article_comments_list(self):
        article_comments = self.article_comment_factory.create_batch(10)

        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(json_data['data'], status.HTTP_200_OK)
    

class CreateArticleCommentListTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('comment', args=[1])
        self.user = UserFactory.create(password='testtest')
        self.article = ArticleFactory.create(id=1)
        self.data = {
            'content': 'test comment'
        }
        # self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

    def test_not_login(self):
        response = self.client.post(self.url, data=self.data, format='json')
        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_data['detail'], '로그인이 필요한 기능입니다.')

    def test_none_check_content(self):
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        self.data['content'] = None

        response = self.client.post(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['content'], ['이 필드는 null일 수 없습니다.'])
        

    def test_create_content(self):
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

        response = self.client.post(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_data['data']['content'], self.data['content'])
        self.assertEqual(json_data['data']['user']['email'], self.user.email)


class GetArticleCommentTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('commentDetail', args=[1, 1])
        
    def test_get_no_comment(self) :
        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(json_data['data'])

    def test_get_comment(self):
        ArticleFactory.create(id=1)
        ArticleCommentFactory.create(id = 1, article_id=1)

        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(json_data['data'])

class PatchArticleCommentTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('commentDetail', args=[1, 1])
        self.user = UserFactory.create(password='testtest')
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        self.article = ArticleFactory.create(id=1)
        # self.article_comment = ArticleCommentFactory.create(id=1, article_id=1, user_id=1)
        # self.article_not_mine_comment = ArticleCommentFactory.create(id=2, article_id=1, user_id=3)
        self.data = {
            'content' : 'test comment patch'
        }

    def test_get_not_mine_comment(self):
        another_user = UserFactory.create()
        ArticleCommentFactory.create(id=1, article_id=1, user_id = another_user.id)

        response = self.client.patch(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['data'],  '다른 사람의 글을 수정할 수 없습니다.')


    def test_null_check_content(self):
        self.data['content'] = None

        ArticleCommentFactory.create(id=1, article_id=1, user_id = self.user.id)

        response = self.client.patch(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['content'], ['이 필드는 null일 수 없습니다.'])

    def test_patch_comment(self):
        ArticleCommentFactory.create(id=1, article_id=1, user_id = self.user.id)

        response = self.client.patch(self.url, data=self.data, format='json')
        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_data['data']['content'], self.data['content'])
        self.assertEqual(json_data['data']['user']['email'], self.user.email)

class DeleteArticleCommentTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(password='testtest')
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        self.article = ArticleFactory.create()
        self.url = reverse('commentDetail', args=[self.article.id,2])

    def test_get_not_mine_comment(self):
        another_user = UserFactory.create()
        ArticleCommentFactory.create(article_id=self.article.id, user_id = another_user.id)

        response = self.client.delete(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['data'], '다른 사람의 글을 삭제할 수 없습니다.')

    def test_delete_comment(self):
        ArticleCommentFactory.create(article_id=self.article.id, user_id = self.user.id)

        response = self.client.delete(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json_data['success'])

