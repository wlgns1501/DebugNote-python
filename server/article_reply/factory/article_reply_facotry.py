import factory
from faker import Faker
from article_comment.models import Article_Comment
from account.factory.user_factory import UserFactory
from blog.factory.article_factory import ArticleFactory
from article_reply.models import Reply
from article_comment.factory.article_comment_factory import ArticleCommentFactory

class ReplyFactory(factory.django.DjangoModelFactory):
    class Meta :
        model= Reply
    
    content = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(ArticleCommentFactory)
    created_at = factory.Faker('date_time')
    # updated_at = factory.Faker('date_time')