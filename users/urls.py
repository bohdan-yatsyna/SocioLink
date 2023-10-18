from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from users.views import SignupUserView, ManageUserView


app_name = "users"

urlpatterns = [
    path("signup/", SignupUserView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair_and_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="manage_user_details"),
]
