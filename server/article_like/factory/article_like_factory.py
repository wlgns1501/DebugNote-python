import factory
from faker import Faker
from article_like.models import Article_Like
from account.factory.user_factory import UserFactory
from blog.factory.article_factory import ArticleFactory


class ArticleLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article_Like
    
    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)
    created_at = factory.Faker('date_time')
