from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import MeView

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api-token-auth"),
    path("users/me/", MeView.as_view(), name="api-user-me"),
]
