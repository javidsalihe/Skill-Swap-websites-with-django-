from django.urls import path
from api.views.skill_autocomplete import SkillAutocompleteAPIView
from api.views.search import SkillSearchAPIView


urlpatterns = [
    path('skills/autocomplete/', SkillAutocompleteAPIView.as_view()),
    path('search/', SkillSearchAPIView.as_view()),
]