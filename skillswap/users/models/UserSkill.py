from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models.skill import Skill
from users.models.user import User


class UserSkill(models.Model):
    PROFICIENCY_LEVELS = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Proficient'),
        (4, 'Professional'),
        (5, 'Expert'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.IntegerField(choices=PROFICIENCY_LEVELS, validators=[MinValueValidator(1), MaxValueValidator(5)])
    working_status = models.BooleanField(default=True)


    def __str__(self):
        return str(self.skill_id)

    class Meta:
        db_table = 'user_skills'
        verbose_name = 'User Skill'
        verbose_name_plural = 'User skill'
        unique_together = (('user_id', 'skill_id'),)