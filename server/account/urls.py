from django.urls import path
from .api.views import *


urlpatterns = [
    path('', UserDetailView.as_view(), name='user'),
    path("signup", SignUpView.as_view(), name="signup"),
    path("signin", SignInView.as_view(), name="signin"),
    path("signout", SignOutView.as_view(), name="signout")
]

# urlpatterns = format_suffix_patterns(urlpatterns)
