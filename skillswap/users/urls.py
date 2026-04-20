from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_list, name="users_list"),
    path('user_form', views.user_form, name="user_form"),
    path('load_cities', views.load_cities, name="load_cities"),
    path('load_districts', views.load_districts, name="load_districts"),
    path('create_user', views.create_user, name="create_user"),
    path('destroy_user/<uuid:userId>/', views.destroy_user, name="destroy_user"),
    path('edit_form/<uuid:userId>/', views.edit_form, name="edit_form"),
    path('update_user/<uuid:userId>/', views.update_user, name="update_user"),
    path('user_info/<uuid:userId>/', views.user_info, name="user_info"),

    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('register/', views.register_view, name='register'),

    path('profile/<uuid:userId>/', views.profile, name="profile"),
    path('update_user_profile/<uuid:userId>/', views.update_user_profile, name="update_user_profile"),

    path('user_skill/', views.user_skill, name="user_skill"),
    path('load_skills', views.load_skills, name="load_skills"),
    path('/create_user_skill_category', views.create_user_skill_category, name='create_user_skill_category'),
    path('/ajax_create_skill', views.ajax_create_skill, name='ajax_create_skill'),
    path('user_skill_create', views.user_skill_create, name='user_skill_create'),
    path('user_skill_delete/<int:pk>/', views.user_skill_delete, name='user_skill_delete'),

    path('ajax/skills-by-category/', views.skills_by_category, name='skills_by_category'),
    path('user_skill_update/<int:pk>/', views.user_skill_update, name='user_skill_update'),

    path('save_contact/', views.save_contact, name='save_contact'),

    # system log
    path('admin/logs/', views.system_logs_list, name='system_logs_list'),
    path('admin/logs/delete/<int:log_id>/', views.delete_log, name='delete_log'),


]
