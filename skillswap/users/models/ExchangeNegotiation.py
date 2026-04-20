from django.db import models
from users.models import Exchange
from users.models.user import User


class ExchangeNegotiation(models.Model):

    class NegotiationStatus(models.TextChoices):
        PENDING = "pending", "Warten"
        ACCEPTED = "accepted", "Akzeptiert"
        REJECTED = "rejected", "Abgelehnt"
        SUPERSEDED = "superseded", "Ersetzt"

    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='negotiations')
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposed_negotiations')
    proposed_scheduled_at = models.DateTimeField(null=True, blank=True)
    proposed_location_type = models.CharField(max_length=20,choices=Exchange.LocationType.choices,default=Exchange.LocationType.IN_PERSON)
    proposed_meeting_address = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20,choices=NegotiationStatus.choices,default=NegotiationStatus.PENDING)
    is_seen_by_recipient = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exchange_negotiation'
        verbose_name_plural = 'exchange negotiations'
        ordering = ['-created_at']