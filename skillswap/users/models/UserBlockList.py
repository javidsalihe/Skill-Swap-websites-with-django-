from django.db import models


class UserBlockList(models.Model):
    blocker = models.ForeignKey('User', on_delete=models.CASCADE, related_name='blocking_users')
    blocked_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='blocked_by_users')
    reason = models.TextField(blank=True, null=True) # برای گزارش به ادمین
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_block_lists'
        unique_together = ('blocker', 'blocked_user') # یک نفر را نمی‌توان دوبار بلاک کرد