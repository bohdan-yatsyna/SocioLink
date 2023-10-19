from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    CustomTokenObtainPairView,
    ManageUserView,
    SignupUserView,
    UserLastActivityView,
)


app_name = "users"

urlpatterns = [
    path("signup/", SignupUserView.as_view(), name="signup"),
    path(
        "login/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair_and_login",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="manage_user_details"),
    path(
        "user_activity/",
        UserLastActivityView.as_view(),
        name="user_activity"
    ),
]
