from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import users
from skillswap.views import SmartLoginView
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path(
    #     'login/',
    #     auth_views.LoginView.as_view(
    #         template_name='users/auth/login.html'
    #     ),
    #     name='login'
    # ),

    path('login/', SmartLoginView.as_view(), name='login'),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout'
    ),

    # Password Reset
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/auth/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/auth/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/auth/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/auth/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('admin/', admin.site.urls),
    path('redirect/', users.views.login_redirect),
    path('', include('core.urls')),
    path('adminPanel/', include('adminPanel.urls')),
    path('users/', include('users.urls')),
    path('masterdata/', include('masterData.urls')),
    path('api/', include('api.urls')),
    path('skill/', include('skill.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
