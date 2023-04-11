import factory
from faker import Faker
from account.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        # django_get_or_create = ('email', 'nickname')

    email = factory.Faker('email')
    nickname = factory.Faker('name')
    password = factory.Faker('password')
    
