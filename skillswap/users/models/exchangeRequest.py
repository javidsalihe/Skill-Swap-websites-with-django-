from django.db import models
import uuid

from users.models import UserSkill
from users.models.skill import Skill
from users.models.user import User


class ExchangeRequest(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = "available", "Offen"
        CLOSED = "closed", "Geschlossen"
        MATCHED = "matched", "Erfolgreich"
        EXPIRED = "expired", "Abgelaufen"

    class UrgencyLevel(models.TextChoices):
        NORMAL = "normal"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
    class PreferredDays(models.TextChoices):
        MONDAY = "monday"
        TUESDAY = "tuesday"
        WEDNESDAY = "wednesday"
        THURSDAY = "thursday"
        FRIDAY = "friday"
        SATURDAY = "saturday"
        SUNDAY = "sunday"
    class PreferredTimeRange(models.TextChoices):
        MORGEN = "morgen"
        VORMITTAG = "vormittage"
        NACHMITTAG = "nachmittage"
        ABEND = "abend"

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_requests')
    requested_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='requested_in_exchanges')
    offered_skill = models.ForeignKey(UserSkill, on_delete=models.CASCADE, related_name='offered_in_exchanges')
    description = models.TextField(blank=True,null= True)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    urgency_level = models.CharField(max_length=20, choices=UrgencyLevel.choices, default=UrgencyLevel.NORMAL)
    preferred_time_range = models.CharField(max_length=30,blank=True,null=True,choices=PreferredTimeRange.choices)
    max_distance_km = models.IntegerField(default=10,blank=True,null=True)
    estimated_duration_minutes = models.IntegerField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    preferred_days = models.JSONField(default=list, blank=True,null=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.title

    class Meta:
        db_table = 'exchange_requests'
        verbose_name = 'Exchange Request'
        verbose_name_plural = "Exchange Requests"
        ordering = ["-created_at"]