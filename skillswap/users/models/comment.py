from django.db import models
from users.models import User
from users.models.rating import Rating


class Comment(models.Model):
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    content = models.TextField()

    is_admin_reply = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    like_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']
