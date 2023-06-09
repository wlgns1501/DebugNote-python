from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.routers import DefaultRouter


from blog.api.views import *

router = routers.DefaultRouter()



schema_view = get_schema_view(
    openapi.Info(
        title="Statchung API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# router = DefaultRouter()
# router.register('blog/', ArticleViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('auth/', include('account.urls')),
    path('', include('blog.urls')),
    path('', include('article_like.urls')),
    path('', include('article_comment.urls')),
    path('', include('article_reply.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

