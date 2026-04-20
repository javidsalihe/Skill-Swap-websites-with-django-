from django.db import models
import uuid
from users.models.user import User


class ActivityLog(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')

    class ActivityTypes(models.TextChoices):
        USER_LOGIN = "user_login"
        USER_LOGOUT = "user_logout"
        USER_REGISTRATION = "user_registration"
        PROFILE_UPDATE = "profile_update"
        PASSWORD_CHANGE = "password_change"
        SKILL_ADDED = "skill_added"
        SKILL_REMOVED = "skill_removed"
        SKILL_UPDATED = "skill_updated"
        EXCHANGE_REQUESTED = "exchange_requested"
        EXCHANGE_MATCHED = "exchange_matched"
        EXCHANGE_REJECTED = "exchange_rejected"
        RATING_GIVEN = "rating_given"

    activity_type = models.CharField(max_length=50, choices=ActivityTypes.choices)
    description = models.TextField()
    metadata = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_logs'
        verbose_name_plural = 'activity_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.activity_type} - {self.user.email if self.user else 'System'}"



