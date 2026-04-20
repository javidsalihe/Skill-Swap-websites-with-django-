from django.db import models
from users.models import Exchange, User


class Rating(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'published', 'Published'
        REPORTED = 'reported', 'Reported'
        HIDDEN = 'hidden', 'Hidden'

    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    score = models.IntegerField()
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exchange', 'author')
        db_table = 'ratings'

# from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from django.core.validators import MinValueValidator, MaxValueValidator
# import uuid
#
# class Rating(models.Model):
#     class Status(models.TextChoices):
#         PUBLISHED = 'published', 'Published'
#         REPORTED = 'reported', 'Reported'
#         HIDDEN = 'hidden', 'Hidden'
#
#     uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='ratings_given')
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True, blank=True)
#     object_id = models.UUIDField(null=True, blank=True)
#     content_object = GenericForeignKey('content_type', 'object_id')
#     score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField(blank=True)
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
#     report_count = models.IntegerField(default=0)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         unique_together = ['author', 'content_type', 'object_id']
#         db_table = 'ratings'
#         ordering = ('-created_at',)
#
#     def __str__(self):
#         return f"{self.author.username} rated {self.content_object} = {self.score}"
