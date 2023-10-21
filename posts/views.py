from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from posts.models import Post, Like
from posts.serializers import PostSerializer, LikeSerializer
from posts.permissions import IsAuthorOrReadOnly


class PostCreateListView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class PostLikeView(generics.CreateAPIView):
    queryset = Post.objects.select_related("author")
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])

        if Like.objects.filter(post=post, liked_by=self.request.user).exists():
            raise serializers.ValidationError(
                "You've already liked this post before."
            )

        serializer.save(post=post, liked_by=self.request.user)


class PostUnlikeView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    lookup_field = "post__id"
    lookup_url_kwarg = "post_id"

    def get_object(self):
        instance = super().get_object()

        if instance.liked_by != self.request.user:
            raise serializers.ValidationError(
                "Impossible to unlike, You haven't liked this post."
            )

        return instance

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": "Post is unliked."},
            status=status.HTTP_200_OK
        )
