from django.urls import path
from .api.views import *

urlpatterns = [
    path('article/<int:article_id>/comment/', CommentView.as_view(), name='comment'),
    path('article/<int:article_id>/comment/<int:comment_id>', CommentDetailView.as_view(), name='commentDetail'),
]
