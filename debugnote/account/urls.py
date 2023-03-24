from django.urls import path
from .views import *


urlpatterns = [
    # path("v1/test", UserView.as_view(), name="test"),
    path("", UserView.as_view()),
    # path("signin/", UserView.signin, name="signin"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
