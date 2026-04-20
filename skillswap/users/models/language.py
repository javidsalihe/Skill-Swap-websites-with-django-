from django.db import models

class Language(models.Model):
    language_name = models.CharField(max_length=100,unique=True)
    language_code = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.language_name

    class Meta:
        db_table = 'languages'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ['-created_at']