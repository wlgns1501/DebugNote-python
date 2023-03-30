from django.urls import path
from .api.views import ArticleView


urlpatterns = [
    path("", ArticleView.as_view(), name="article")
]

