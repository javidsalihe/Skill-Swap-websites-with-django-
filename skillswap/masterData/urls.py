from django.urls import path
from masterData.views import country
from masterData.views import city
from masterData.views import district
from masterData.views import language

urlpatterns = [

    path('countries', country.countries_list, name='countries_list'),
    path('countries/create/', country.create_country, name='create_country'),
    path('countries/update/<int:pk>/', country.update_country, name='update_country'),
    path('countries/delete/<int:pk>/', country.delete_country, name='delete_country'),

    path('cities', city.cities_list, name='cities_list'),
    path('cities/create/', city.create_city, name='create_city'),
    path('cities/update/<int:pk>/', city.update_city, name='update_city'),
    path('cities/delete/<int:pk>/', city.delete_city, name='delete_city'),

    path('districts', district.districts_list, name='districts_list'),
    path('districts/create/', district.create_district, name='create_district'),
    path('districts/update/<int:pk>/', district.update_district, name='update_district'),
    path('districts/delete/<int:pk>/', district.delete_district, name='delete_district'),

    path('languages', language.languages_list, name='languages_list'),
    path('languages/create/', language.create_language, name='create_language'),
    path('languages/update/<int:pk>/', language.update_language, name='update_language'),
    path('languages/delete/<int:pk>/', language.delete_language, name='delete_language'),

]
