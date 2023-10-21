from django.urls import path
from .views import PostCreateListView, PostRetrieveUpdateDestroyView, PostLikeView, PostUnlikeView

app_name = "posts"

urlpatterns = [
    path("", PostCreateListView.as_view(), name="post-list-create"),
    path(
        "<int:pk>/",
        PostRetrieveUpdateDestroyView.as_view(),
        name="post-detail-update-delete",
    ),
    path("<int:post_id>/like/", PostLikeView.as_view(), name="like-post"),
    path(
        "<int:post_id>/unlike/",
        PostUnlikeView.as_view(),
        name="unlike-post",
    )
]
