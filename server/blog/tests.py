import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from blog.factory.article_factory import ArticleFactory
from rest_framework import status
from account.factory.user_factory import UserFactory
from blog.models import Article


class GetArticleListTestAPIViewTestCase(APITestCase):
    def setUp(self) :
        self.url = reverse('article')
        self.factory = APIRequestFactory()
        self.article_facotry = ArticleFactory
        

    def test_get_no_articles_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['articles'], [])
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_articles_list(self):
        self.articles = ArticleFactory.create_batch(10)
        response = self.client.get(self.url)
        
        json_data = json.loads(json.dumps(response.data['articles']))
        
        self.assertNotEqual(json_data, [])
        self.assertEqual(len(json_data), response.data['count'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateArticleTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('article')
        self.user = UserFactory.create(password='testtest')
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        self.data = {
            'title' : 'test title',
            'content' : 'test test  test test'
        }

    def test_create_article_with_null_check_title(self) :
        self.data['title'] = None

        response = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                            "title": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        })

    def test_create_article_with_null_check_content(self) :
        self.data['content'] = None

        response = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
                            "content": [
                                    '이 필드는 null일 수 없습니다.'
                                ]
                        })
        
    def test_create_article(self) :
        response = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        article = response.data['data']

        self.assertEqual(self.data['title'], article['title'])
        self.assertEqual(self.data['content'], article['content'])

        user = json.loads(json.dumps(response.data['data']['user']))

        self.assertEqual(self.user.id, user['id'])
        self.assertEqual(self.user.email, user['email'])
        self.assertEqual(self.user.nickname, user['nickname'])

class GetArticleTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('articleDetail', args=[1])
        self.article_factory = ArticleFactory
    
    def test_get_no_article(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(response.data['data'])

    def test_get_article(self):
        self.article_factory.create(id=1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data'])


class PatchArticleTestAPIViewTestCase(APITestCase):
    def setUp(self) :
        self.url = reverse('articleDetail', args=[21])
        self.user_factory= UserFactory
        self.user = UserFactory.create(password='testtest')
        self.aritlce_factory = ArticleFactory
        self.article = ArticleFactory.create(id = 21, user_id = self.user.id)
    
    def test_check_article_mine(self):
        user = self.user_factory.create(password='aaaa')
        login_response = self.client.post('/auth/signin', {'email' : user.email, 'password' :'aaaa'}, format='json')

        data = {
            'title' : 'title title2',
            'content' : 'content 2222'
        }

        response = self.client.patch(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['data'], '다른 사람의 글을 수정할 수 없습니다.')
    
    def test_patch_aritcle(self) :
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

        data = {
            'title' : 'title title2',
            'content' : 'content 2222'
        }

        response = self.client.patch(self.url, data=data, format='json')
        

        json_data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_data['data']['title'], data['title'])
        self.assertEqual(json_data['data']['content'], data['content'])
        self.assertEqual(json_data['data']['user']['id'], self.user.id)


class DeleteArticleTestAPIViewTestCase(APITestCase):
    def setUp(self) :
        self.url = reverse('articleDetail', args=[21])
        self.user_factory= UserFactory
        self.user = UserFactory.create(password='testtest')
        self.aritlce_factory = ArticleFactory
        self.article = ArticleFactory.create(id = 21, user_id = self.user.id)

    def test_check_article_mine(self):
        user = self.user_factory.create(password='aaaa')
        login_response = self.client.post('/auth/signin', {'email' : user.email, 'password' :'aaaa'}, format='json')

        data = {
            'title' : 'title title2',
            'content' : 'content 2222'
        }

        response = self.client.patch(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['data'], '다른 사람의 글을 수정할 수 없습니다.')
    
    def test_delete_article(self):
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')

        response = self.client.delete(self.url)

        json_data = response.json()

        with self.assertRaises(Article.DoesNotExist):
           Article.objects.get(id=21)

        self.assertEqual(json_data['success'], True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


