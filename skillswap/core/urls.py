from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('searching_skills/', views.search_results_view, name='searching_skills'),
]
