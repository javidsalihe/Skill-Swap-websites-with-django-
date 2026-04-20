from django.db import models

from users.models.City import City


class District(models.Model):
    district_name = models.CharField(max_length=150)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"The district name is  : {self.district_name}"

    class Meta:
        db_table = 'districts'
        verbose_name = 'district'
        verbose_name_plural = 'districts'
        ordering = ['-created_at']