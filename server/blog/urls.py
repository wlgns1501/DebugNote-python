from django.urls import path
from .api.views import ArticleView, ArticleDetailView
# from .api.views import ArticleViewSet

# article_list = ArticleViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create'
# })

# article_detail = ArticleViewSet.as_view({
#     'get' : 'retrieve',
#     'patch' : 'partial_update',
#     'delete' : 'destroy'
# })

urlpatterns = [
    path('article/', ArticleView.as_view(), name='article'),
    path('article/<int:article_id>/', ArticleDetailView.as_view(), name='articleDetail')
    # path('article/', article_list, name='article'),
    # path('article/<int:article_id>/', article_detail, name='articleDetail')
]
