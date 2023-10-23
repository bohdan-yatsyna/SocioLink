from django.urls import path
from .views import (
    PostCreateListView,
    PostRetrieveUpdateDestroyView,
    health_check,
    PostLikeUnlikeView,
)

app_name = "posts"

urlpatterns = [
    path("", PostCreateListView.as_view(), name="post-list-create"),
    path(
        "<int:pk>/",
        PostRetrieveUpdateDestroyView.as_view(),
        name="post-detail-update-delete",
    ),
    path(
        "<int:post_id>/like/",
        PostLikeUnlikeView.as_view(),
        name="like-unlike-post",
    ),
    path("health/", health_check, name="api-health-check"),
]
