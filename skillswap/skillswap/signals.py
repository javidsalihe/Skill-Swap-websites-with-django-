from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType
from users.models import SystemLog
from .middleware.user_logs import get_current_user, get_current_ip, get_current_agent

# ثبت لاگین
@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    SystemLog.objects.create(
        content_type=ContentType.objects.get_for_model(user),
        object_id=user.id,
        action_by=user,
        action_type='CREATE',
        new_value={'event': 'Login success'},
        ip_address=get_current_ip(),
        user_agent=get_current_agent()
    )

# ثبت تلاش‌های ناموفق برای ورود (بسیار مهم برای امنیت)
@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    SystemLog.objects.create(
        content_type=ContentType.objects.get_for_model(SystemLog), # به خود مدل لاگ وصل می‌کنیم
        object_id=0,
        action_type='DELETE',
        new_value={'event': 'Login failed', 'username_attempted': credentials.get('username')},
        ip_address=request.META.get('REMOTE_ADDR')
    )

# ثبت تغییرات دیتابیس (هر مدل)
@receiver(post_save)
def audit_db_save(sender, instance, created, **kwargs):
    if sender == SystemLog: return
    action = 'CREATE' if created else 'UPDATE'
    SystemLog.objects.create(
        content_object=instance,
        action_by=get_current_user(),
        action_type=action,
        new_value=model_to_dict(instance),
        ip_address=get_current_ip(),
        user_agent=get_current_agent()
    )