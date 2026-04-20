from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models.user import User
from users.models.address import Address
from users.models.City import City
from users.models.Country import Country
from users.models.district import District
from users.models.language import Language
from users.models.skill import Skill
from users.models.SkillCategory import SkillCategory
from users.models.UserSkill import UserSkill
from users.models.exchange import Exchange
from users.models.exchangeRequest import ExchangeRequest
from users.models.rating import Rating
from users.models.comment import Comment
from users.models.activityLog import ActivityLog
from users.models.socialMediaLink import SocialMediaLink

# Register User with custom UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

# Register all other models
admin.site.register(Address)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(District)
admin.site.register(Language)
admin.site.register(Skill)
admin.site.register(SkillCategory)
admin.site.register(UserSkill)
admin.site.register(Exchange)
admin.site.register(ExchangeRequest)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(ActivityLog)
admin.site.register(SocialMediaLink)
