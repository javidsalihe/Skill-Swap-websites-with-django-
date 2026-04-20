from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class SocialMediaLink(models.Model):
    SOCIAL_MEDIA_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]

    type = models.CharField(
        max_length=20,
        choices=SOCIAL_MEDIA_CHOICES,
        null=True,
        blank=True,
        default='other'
    )
    link = models.URLField(null=True, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,related_name='social_media_link')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type}: {self.link}"

    class Meta:
        db_table = 'social_media_links'
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'
