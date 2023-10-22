from rest_framework import serializers
from posts.models import Post, Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ("post", "liked_by", "liked_date")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author", "title", "text", "created_at", "likes")

    @staticmethod
    def get_likes(instance):
        return instance.likes.count()
