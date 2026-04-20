from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Öffentliche URLs (genau diese)
        self.public_urls = [
            '/',  # Homepage
            '/login/',  # Login-Seite
            '/users/register/',  # Registrierungsseite
            '/logout/',  # Logout-Seite
            '/password_reset/',
            '/password_reset/done/',
            '/reset/',
            '/reset/done/',
            '/users/save_contact/'
        ]

        # Öffentliche Präfixe (alles was damit beginnt)
        self.public_prefixes = [
            '/admin/',  # Django Admin
            '/static/',  # Statische Dateien
            '/media/',  # Medien-Dateien
            '/reset/',
            '/api/',
        ]

    def __call__(self, request):
        path = request.path

        # Wenn Benutzer nicht authentifiziert ist
        if not request.user.is_authenticated:
            # Prüfe auf exakte Übereinstimmung mit öffentlichen URLs
            if path in self.public_urls:
                return self.get_response(request)

            # Prüfe auf Präfixe
            is_public_prefix = any(path.startswith(prefix) for prefix in self.public_prefixes)
            if is_public_prefix:
                return self.get_response(request)

            # Sonderfall: Login- und Register-URLs ohne trailing slash
            if path in ['/login', '/users/register', '/logout',
                        '/password_reset/',
                        '/password_reset/done/',
                        '/reset/done/',
                        '/users/save_contact/'

                        ]:
                return self.get_response(request)

            # Wenn keine der obigen Bedingungen zutrifft, redirect zum Login
            # Aber nicht, wenn wir bereits auf der Login-Seite sind (vermeide Redirect-Loop)
            if not path.startswith('/login'):
                return redirect(f'{settings.LOGIN_URL}?next={path}')

        return self.get_response(request)
