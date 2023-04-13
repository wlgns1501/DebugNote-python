import factory
from faker import Faker
from article_comment.models import Article_Comment
from account.factory.user_factory import UserFactory
from blog.factory.article_factory import ArticleFactory


class ArticleCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article_Comment
    
    content = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')