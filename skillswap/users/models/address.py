from django.db import models
from users.models.district import District

class Address(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True, related_name='addresses')
    street_name = models.CharField(max_length=200, null=True, blank=True)
    street_number = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timezone = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        parts = [self.street_name, self.street_number, self.postal_code]
        address_str = ", ".join(filter(None, parts))
        return f"{address_str}" if address_str else "Address not provided"

    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['-created_at']
