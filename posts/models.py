from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.title}, {self.created_at}"


class Like(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    liked_by = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="likes",
    )
    liked_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ["post", "liked_by"]
