from django import forms
from users.models import Country, City, District, Language


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['country_name', 'country_code']
        labels = {
            'country_name': 'Ländername',
            'country_code': 'Ländercode',
        }
        widgets = {
            'country_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. Deutschland'
            }),
            'country_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. DE',
            }),

        }


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city_name', 'country']
        labels = {
            'city_name': 'Stadtname',
            'country': 'Land',
        }
        widgets = {
            'city_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. Berlin',
                'required': 'true',

            }),
            'country': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].empty_label = "Bitte wählen Sie ein Land"


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district_name', 'city']
        labels = {
            'city': 'Stadtname',
            'district_name': 'Bezirk name',
        }
        widgets = {
            'district_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. Spandau',
                'required': 'true',

            }),
            'city': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true',
            }),
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['city'].empty_label = "Bitte wählen Sie ein Stadt"


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language_name', 'language_code']
        labels = {
            'language_name': 'Sprachname',
            'language_code': 'Sprachcode',
        }
        widgets = {
            'language_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. English',
            }),
            'language_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. EN',
            }),

        }