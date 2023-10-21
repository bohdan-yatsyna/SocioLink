from django.urls import path
from .views import PostCreateListView, PostRetrieveUpdateDestroyView


app_name = "posts"

urlpatterns = [
    path("", PostCreateListView.as_view(), name="post-list-create"),
    path(
        "<int:pk>/",
        PostRetrieveUpdateDestroyView.as_view(),
        name="post-detail-update-delete"
    ),
]
