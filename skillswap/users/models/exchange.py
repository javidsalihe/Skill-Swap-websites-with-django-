from django.db import models
import uuid
from users.models.skill import Skill
from users.models.user import User
from users.models.exchangeRequest import ExchangeRequest



class Exchange(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Warten"
        ACCEPTED = "accepted", "Akzeptiert"
        REJECTED = "rejected", "Abgelehnt"
        COMPLETED = "completed", "Abgeschlossen"
        CANCELED = "canceled", "Abgebrochen"
    class LocationType(models.TextChoices):
        ONLINE = "online"
        IN_PERSON = "in_person"
        HYBRID = "hybrid"


    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_exchanges',null=True,blank=True)
    user_x = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchanges_as_x')
    user_y = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchanges_as_y')
    skill_from_x_to_y = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='exchanges_from_x_to_y')
    skill_from_y_to_x = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='exchanges_from_y_to_x')
    exchange_request = models.ForeignKey(ExchangeRequest,on_delete=models.CASCADE,related_name='offers',null=True,blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_seen_by_receiver = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    location_type = models.CharField(max_length=20, choices=LocationType.choices, default=LocationType.IN_PERSON)
    meeting_address = models.TextField(blank=True)
    description = models.TextField(blank=True, null=True)
    actual_duration_minutes = models.IntegerField(null=True, blank=True)
    final_agreement_reached = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    done_by_x = models.BooleanField(default=False)
    done_by_y = models.BooleanField(default=False)
    completed_at_x = models.DateTimeField(null=True, blank=True)
    completed_at_y = models.DateTimeField(null=True, blank=True)
    duration_minutes_x = models.IntegerField(null=True, blank=True)
    duration_minutes_y = models.IntegerField(null=True, blank=True)


    cancellation_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exchanges'
        verbose_name_plural = 'Exchanges'
        verbose_name = 'Exchange'
        unique_together = ['exchange_request', 'initiated_by', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Exchange: {self.user_x} ↔ {self.user_y}"

    @property
    def pdf_agreement(self):
        return self.documents.filter(document_type='agreement').first()

    @property
    def pdf_completion(self):
        return self.documents.filter(document_type='completion').first()

