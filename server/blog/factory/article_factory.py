import factory
from faker import Faker
from blog.models import Article
from account.factory.user_factory import UserFactory


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
    

    content = factory.Faker('paragraph')
    user = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')