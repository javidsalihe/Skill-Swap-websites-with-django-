from django.db import models
from users.models.Country import Country


class City(models.Model):
    city_name = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.city_name

    class Meta:
        db_table = 'cities'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['-created_at']
