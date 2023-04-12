import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from blog.factory.article_factory import ArticleFactory
from rest_framework import status


class ArticleTestAPIViewTestCase(APITestCase):
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
        
        json_data = json.dumps(response.data['articles'])
        print(response.data['count'])
        print(len(json_data))
