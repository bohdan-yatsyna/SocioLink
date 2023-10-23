from __future__ import annotations

from rest_framework import serializers
from posts.models import Post, Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = []


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author", "title", "text", "created_at", "likes")

    @staticmethod
    def get_likes(instance: Post) -> int:
        return instance.likes.count()
