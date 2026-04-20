from django.db import models

class SkillCategory(models.Model):
    skill_name = models.CharField(max_length=255)
    skill_description = models.TextField(null=True, blank=True)
    skill_image_url = models.ImageField(upload_to='skill_categories/',null=True, blank=True)
    skill_link_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.skill_name

    class Meta:
        db_table = 'skill_categories'
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'
        ordering = ['-created_at']