from django.db import connections
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.reverse import reverse
from account.factory.user_factory import UserFactory
from blog.factory.article_factory import ArticleFactory
from article_comment.factory.article_comment_factory import ArticleCommentFactory
from article_reply.factory.article_reply_facotry import ArticleReplyFactory
from article_reply.models import Reply
from article_comment.models import Article_Comment
from blog.models import Article

class GetRepliesListTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('reply', args=[1,1])
        self.article_reply_factory = ArticleReplyFactory

    def test_no_article_replies_list(self):
        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_data['data'], [])
        self.assertTrue(json_data['success'])
    
    def test_get_article_list(self):
        article_replies = ArticleReplyFactory.create_batch(10)

        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(json_data['data'], [])

      


class CreateArticleReplyTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create(password = 'testtest')
        self.article = ArticleFactory.create()
        self.article_comment = ArticleCommentFactory.create(id=1)
        # self.url = reverse('reply', args=[self.article.id, self.article_comment.id])
        self.url = reverse('reply', args=[1,1])
        self.data = {
            'content' : 'test reply'
        }

    def test_not_login(self) :
        response = self.client.post(self.url, data=self.data, format='json')
        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json_data['detail'], '로그인이 필요한 기능입니다.')

    def test_none_check_content(self) :
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        self.data['content'] = None

        response = self.client.post(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['content'], ['이 필드는 null일 수 없습니다.'])


    def test_create_reply(self):
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        response = self.client.post(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_data['data']['content'], self.data['content'])


class GetReplyTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('replyDetail', args=[1,1,1])
        self.article_factory = ArticleFactory
        self.article_reply_factory = ArticleReplyFactory
        self.article_comment_factory = ArticleCommentFactory

    def test_no_get_reply(self):
        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json_data['data'], '대댓글이 존재하지 않습니다.')

    def test_get_reply(self):
        article = self.article_factory.create(id=1)
        article_comment = self.article_comment_factory.create(id=1, article_id= 1)
        article_reply = self.article_reply_factory.create(id=1, comment_id=1)

        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(json_data['data'])

class PatchArticleReplyTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('replyDetail', args=[1,1,1])
        self.user = UserFactory.create(password='testtest')
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        self.article = ArticleFactory.create(id=1)
        self.article_comment = ArticleCommentFactory.create(id=1, article_id=1)
        self.data = {
            'content' : 'test patch reply'
        }

    def test_get_not_mine_reply(self):
        another_user = UserFactory.create()
        ArticleReplyFactory.create(id=1, comment_id= 1, user_id = another_user.id)

        response = self.client.patch(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['data'],'다른 사람의 글을 수정할 수 없습니다.' )

    def test_check_none_content(self):
        self.data['content'] = None

        ArticleReplyFactory.create(id=1, comment_id= 1, user_id = self.user.id)

        response = self.client.patch(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['content'], ['이 필드는 null일 수 없습니다.'])

    def test_patch_article_reply(self):
        ArticleReplyFactory.create(id=1, comment_id= 1, user_id = self.user.id)

        response = self.client.patch(self.url, data=self.data, format='json')

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_data['data']['content'], 'test patch reply')

class DeleteArticleReplyTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('replyDetail', args=[1,1,1])
        self.user = UserFactory.create(password='testtest')
        self.login_response = self.client.post('/auth/signin', {'email' :self.user.email, 'password' :'testtest'}, format='json')
        self.article = ArticleFactory.create(id=1)
        self.article_comment = ArticleCommentFactory.create(id=1, article_id=1)

    def test_get_not_mine_reply(self):
        another_user = UserFactory.create()
        ArticleReplyFactory.create(id=1, comment_id= 1, user_id = another_user.id)

        response = self.client.delete(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_data['data'],'다른 사람의 글을 삭제할 수 없습니다.' )


    def test_delete_reply(self):
        ArticleReplyFactory.create(id=1, comment_id=1, user_id=self.user.id)

        response = self.client.delete(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json_data['success'])