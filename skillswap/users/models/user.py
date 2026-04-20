from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from users.models.address import Address
from users.models.language import Language


class User(AbstractUser):

    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('phone', 'Phone')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image_url = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    notifications_via = models.CharField(
        max_length=100,
        choices=NOTIFICATION_CHOICES,
        null=True,
        blank=True
    )
    preferred_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True,related_name='preferred_language')
    address_id = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True,related_name='user_address')
    is_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-created_at',)


    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'
