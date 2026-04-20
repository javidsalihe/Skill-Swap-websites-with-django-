# forms.py
from datetime import timezone
from django.utils import timezone

from django import forms
from users.models import SkillCategory, Skill, UserSkill, ExchangeRequest


class SkillCategoryForm(forms.ModelForm):
    class Meta:
        model = SkillCategory
        fields = ['skill_name', 'skill_description', 'skill_image_url', 'skill_link_url']
        labels = {
            'skill_name': 'Kategoriename',
            'skill_description': 'Beschreibung',
            'skill_image_url': 'Bild hochladen',
            'skill_link_url': 'Link-URL',
        }
        widgets = {
            'skill_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. Programmierung'
            }),
            'skill_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Beschreibung der Kategorie'
            }),
            'skill_image_url': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'skill_link_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/mehr-infos'
            }),
        }

    def skill_name(self):
        skill_name = self.cleaned_data.get('skill_name')
        if not skill_name:
            raise forms.ValidationError("Kategoriename ist erforderlich.")
        return skill_name


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_category_id', 'name', 'description']
        labels = {
            'skill_category_id': 'Kategoriename',
            'name': 'name',
            'description': 'Beschreibung',
        }
        widgets = {
            'skill_category_id': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Z.B. mit python'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Beschreibung der Skill'
            }),
        }

    def skill_name(self):
        skill_name = self.cleaned_data.get('name')
        if not skill_name:
            raise forms.ValidationError("Skill name ist erforderlich.")
        return skill_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skill_category_id'].empty_label = "Bitte wählen Sie ein Kategorie"


class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['user_id', 'skill_id', 'proficiency_level', 'working_status']
        widgets = {
            'user_id': forms.Select(attrs={'class': 'form-control search_select'}),
            'skill_id': forms.Select(attrs={'class': 'form-control search_select'}),
            'proficiency_level': forms.Select(attrs={'class': 'form-control'}),
            'working_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            if 'user_id' in self.fields:
                del self.fields['user_id']

        if 'skill_id' in self.fields:
            self.fields['skill_id'].empty_label = "Bitte wählen..."

        self.fields['proficiency_level'].choices = [
            ('', 'Bitte Kenntnisstand wählen'),
            (1, 'Anfänger (Beginner)'),
            (2, 'Fortgeschritten (Intermediate)'),
            (3, 'Geübt (Proficient)'),
            (4, 'Professionell (Professional)'),
            (5, 'Experte (Expert)'),
        ]


class ExchangeRequestForm(forms.ModelForm):
    preferred_days = forms.MultipleChoiceField(
        choices=ExchangeRequest.PreferredDays.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = ExchangeRequest
        fields = ['requested_skill', 'offered_skill', 'title', 'description',
                  'urgency_level', 'max_distance_km', 'preferred_days', 'preferred_time_range',
                  'estimated_duration_minutes',
                  'expires_at']
        widgets = {
            'requested_skill': forms.Select(attrs={'class': 'form-control search_select '}),
            'offered_skill': forms.Select(attrs={'class': 'form-control search_select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 5, 'placeholder': 'Beschreibung','style': 'resize: none;'}),
            'urgency_level': forms.Select(attrs={'class': 'form-control'}),
            'max_distance_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'estimated_duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'preferred_time_range': forms.Select(attrs={'class': 'form-control'}),
            'expires_at': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'preferred_days': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # گرفتن یوزری که لاگین شده است
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        today = timezone.now().date().isoformat()
        self.fields['expires_at'].widget.attrs['min'] = today

        if user:
            self.fields['offered_skill'].queryset = UserSkill.objects.filter(user_id=user)
        else:
            self.fields['offered_skill'].queryset = UserSkill.objects.none()

        if 'requested_skill' in self.fields:
            self.fields['requested_skill'].empty_label = "wählen sie Bitte gewunschte skill"

        if 'offered_skill' in self.fields:
            self.fields['offered_skill'].empty_label = "wählen sie Bitte ihre skill"

        if 'urgency_level' in self.fields:
            self.fields['urgency_level'].empty_label = "wählen sie ....."

        if 'preferred_time_range' in self.fields:
            self.fields['preferred_time_range'].empty_label = "wählen sie ....."


