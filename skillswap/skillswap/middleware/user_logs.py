import threading
from django.contrib.contenttypes.models import ContentType
from users.models import SystemLog
import json

_thread_locals = threading.local()


class UserLogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ۱. ذخیره اطلاعات در حافظه موقت برای استفاده در سیگنال‌ها
        _thread_locals.user = request.user if request.user.is_authenticated else None
        _thread_locals.ip = self.get_client_ip(request)
        _thread_locals.agent = request.META.get('HTTP_USER_AGENT')

        # ۲. پردازش درخواست
        response = self.get_response(request)

        # ۳. ثبت خودکار "هر فعالیت" (بدون استثنا)
        # ما فقط درخواست‌های GET و POST اصلی را لاگ می‌کنیم که دیتابیس سنگین نشود
        if request.user.is_authenticated and not request.path.startswith('/static/'):
            action_type = 'UPDATE' if request.method == 'POST' else 'CREATE'

            # ثبت در SystemLog
            SystemLog.objects.create(
                content_type=ContentType.objects.get_for_model(request.user),
                object_id=request.user.id,
                action_by=request.user,
                action_type=action_type,
                ip_address=_thread_locals.ip,
                user_agent=_thread_locals.agent,
                new_value={
                    'path': request.path,
                    'method': request.method,
                    'status': response.status_code,
                    'description': f"User visited {request.path}"
                }
            )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def get_current_user(): return getattr(_thread_locals, 'user', None)


def get_current_ip(): return getattr(_thread_locals, 'ip', None)


def get_current_agent(): return getattr(_thread_locals, 'agent', None)