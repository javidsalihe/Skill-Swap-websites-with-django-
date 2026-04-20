from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class SystemLog(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    object_id = models.CharField(max_length=255, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    action_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=10,
                                   choices=[('CREATE', 'hinzufügen'), ('UPDATE', 'bearbeiten'), ('DELETE', 'löchen')])
    previous_value = models.JSONField(default=dict, blank=True, null=True)
    new_value = models.JSONField(default=dict, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_agent

    class Meta:
        db_table = 'system_logs'
        verbose_name = 'system_log'
        verbose_name_plural = 'system_logs'
        ordering = ['-created_at']