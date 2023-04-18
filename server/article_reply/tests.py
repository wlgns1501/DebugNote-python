from rest_framework.test import APIRequestFactory, APITestCase
from blog.factory.article_factory import ArticleFactory
from article_comment.factory.article_comment_factory import ArticleCommentFactory
from account.factory.user_factory import UserFactory
from article_reply.factory.article_reply_facotry import ReplyFactory
from rest_framework.reverse import reverse
from rest_framework import status

class GetReplyListTestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.article = ArticleFactory.create()
        self.article_comment = ArticleCommentFactory.create()
        self.url = reverse('reply', args=[self.article.id, self.article_comment.id])
        self.article_reply_factory = ReplyFactory

    def test_get_no_replies_list(self):
        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_data['data'], [])
        self.assertTrue(json_data['success'])

    def test_get_replies_list(self):
        self.article_reply_factory.create_batch(10, comment_id = self.article_comment.id)

        response = self.client.get(self.url)

        json_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(json_data['data'], [])


