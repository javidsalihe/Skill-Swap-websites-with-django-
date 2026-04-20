from django.db import models
from users.models import User,Exchange


class ExchangeDocument(models.Model):

    class DocType(models.TextChoices):
        AGREEMENT = 'agreement', 'Vereinbarung'
        COMPLETION = 'completion', 'Abschlussbericht'

    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=20,
        choices=DocType.choices
    )

    file = models.FileField(upload_to='exchange_documents/')
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    is_final = models.BooleanField(default=True)

    class Meta:
        db_table = 'exchange_documents'
        unique_together = ('exchange', 'document_type')
