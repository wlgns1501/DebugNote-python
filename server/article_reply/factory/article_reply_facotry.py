import factory
from faker import Faker
from article_comment.factory.article_comment_factory import ArticleCommentFactory
from account.factory.user_factory import UserFactory
from blog.factory.article_factory import ArticleFactory
from article_reply.models import Reply

class ArticleReplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reply

    content = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(ArticleCommentFactory)
    created_at = factory.Faker('date_time')