from django.urls import path
from .api.views import *

urlpatterns = [
    path('article/', ArticleView.as_view(), name='article')
]
