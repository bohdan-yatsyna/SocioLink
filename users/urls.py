from django.urls import path

from users.views import SignupUserView, ManageUserView


app_name = "users"

urlpatterns = [
    path("signup/", SignupUserView.as_view(), name="signup"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
