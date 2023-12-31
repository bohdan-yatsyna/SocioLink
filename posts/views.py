from datetime import datetime
from typing import Any

from django.db.models import Count
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, Like
from posts.serializers import PostSerializer, LikeSerializer
from posts.permissions import IsPostAuthorOrReadOnly


# Only for documentation endpoints details
@extend_schema_view(
    post=extend_schema(
        description="Endpoint for Post creating by User."
    ),
    get=extend_schema(
        description="Endpoint for listing all the Posts."
    ),
)
class PostCreateListView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Only for documentation endpoints details
@extend_schema_view(
    get=extend_schema(
        description="Endpoint with detailed Post page by id. "
    ),
    put=extend_schema(
        description=(
            "Endpoint for updating current Post details by id. "
            "Only post author can make it."
        )
    ),
    patch=extend_schema(
        description=(
            "Endpoint for partial updating current Post details by id. "
            "Only post author can make it."
        )
    ),
    delete=extend_schema(
        description=(
            "Endpoint for deleting current Post by id. "
            "Only post author can make it."
        )
    )
)
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = (IsPostAuthorOrReadOnly,)


class PostLikeView(CreateAPIView):
    """
    View for liking Post by its id,
    accessible only for authenticated users.
    """

    queryset = Like.objects.select_related("post", "liked_by")
    serializer_class = LikeSerializer

    def _get_post(self) -> Post:
        return get_object_or_404(Post, pk=self.kwargs["post_id"])

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        post = self._get_post()

        if Like.objects.filter(post=post, liked_by=request.user).exists():
            return Response(
                {"message": "You've already liked this post before."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().post(request, *args, **kwargs)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.data = {"message": "Liked successfully"}

        return response

    def perform_create(self, serializer: LikeSerializer) -> None:
        post = self._get_post()
        serializer.save(post=post, liked_by=self.request.user)


class PostUnlikeView(DestroyAPIView):
    """
    View for unliking a post by ID
    if this Post has been liked by the user.
    """

    queryset = Like.objects.select_related("post", "liked_by")
    serializer_class = LikeSerializer
    lookup_url_kwarg = "post_id"
    lookup_field = "post"

    def get_object(self) -> Like:
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return get_object_or_404(Like, post=post, liked_by=self.request.user)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        super().destroy(request, *args, **kwargs)

        return Response(
            {"message": "Unliked successfully"},
            status=status.HTTP_200_OK,
        )


# Only for documentation endpoint details
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="date_from",
            description=(
                "Parameter for start date in likes filtering "
                "(ex. '2023-10-21')."
            ),
            required=True,
            type=str,
        ),
        OpenApiParameter(
            name="date_to",
            description=(
                "Parameter for end date in likes filtering "
                "(ex. '2023-10-22')."
            ),
            required=True,
            type=str,
        ),
    ],
    responses={
        200: OpenApiResponse(description="List of like annotated per day"),
    }
)
class LikeAnalyticsView(APIView):
    """View for providing like analytics annotated by days"""

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
            Retrieve the number of likes aggregated by day according to
            provided date range. Requires 'date_from' and 'date_to' as
            query parameters in the format YYYY-MM-DD.
        """

        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if not date_from or not date_to:
            return Response(
                {"error": "Both 'date_from' and 'date_to' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {
                    "error": "Date format is invalid. "
                             "It supposed to be YYYY-MM-DD."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if date_to < date_from:
            return Response(
                {
                    "error": "The 'date_to' must to be greater than "
                             "'date_from' or equal."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        aggregated_likes = Like.objects.filter(
            liked_date__range=[date_from, date_to]
        ).values("liked_date").annotate(
            likes_count=Count("id")
        ).order_by("liked_date")

        if not aggregated_likes:
            return Response(
                {"message": "There are no likes in the provided time range."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(list(aggregated_likes), status=status.HTTP_200_OK)


@api_view(["GET"])
@swagger_auto_schema(
    operation_description="A simple API health check endpoint",
    responses={200: 'OK'}
)
def health_check(request: HttpRequest) -> HttpResponse:
    """
    An endpoint for health checking API.
    Returns a 200 OK response if the service is up.
    """

    return HttpResponse("OK")
