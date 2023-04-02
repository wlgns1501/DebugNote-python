from django.urls import path
from .api.views import *


urlpatterns = [
    path('article/<int:article_id>/like', ArticleLikeView.as_view(), name='article_like')
]
