from django.db import models

class Skill(models.Model):
    skill_category_id = models.ForeignKey('SkillCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='skill_category')
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'skills'
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['-created_at']