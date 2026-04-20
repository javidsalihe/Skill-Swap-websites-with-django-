from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=10,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = 'countries'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['-created_at']