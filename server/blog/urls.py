from django.urls import path
from .api.views import ArticleView, ArticleDetailView



urlpatterns = [
    path('article/', ArticleView.as_view(), name='article'),
    path('article/<int:article_id>/', ArticleDetailView.as_view(), name='articleDetail')
]
