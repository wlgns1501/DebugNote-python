from django.urls import path
from article_reply.api.views import *


urlpatterns = [
    path('article/<int:article_id>/comment/<int:comment_id>/reply', ReplyView.as_view(), name='reply'),
    path('article/<int:article_id>/comment/<int:comment_id>/reply/<int:reply_id>', ReplyDetailView.as_view(), name='replyDetail')
]
