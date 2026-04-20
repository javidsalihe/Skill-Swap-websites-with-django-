import uuid
from django.db import models


class SkillVerification(models.Model):
    class VerificationType(models.TextChoices):
        DOCUMENT = 'document', 'Zertifikat/Dokument'
        ENDORSEMENT = 'endorsement', 'Bestätigung durch Nutzer'
        ADMIN_REVIEW = 'admin_review', 'Admin-Prüfung'

    class VerificationStatus(models.TextChoices):
        PENDING = 'pending', 'Ausstehend'
        APPROVED = 'approved', 'Verifiziert'
        REJECTED = 'rejected', 'Abgelehnt'

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # ارتباط با مهارت خاص کاربر
    user_skill = models.ForeignKey('UserSkill', on_delete=models.CASCADE, related_name='verifications')

    # کسی که تایید می‌کند (می‌تواند کاربر دیگر باشد یا ادمین)
    verifier = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='given_verifications')

    verification_type = models.CharField(max_length=20, choices=VerificationType.choices)
    status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)

    # فایل مدرک (PDF یا تصویر)
    evidence_file = models.FileField(upload_to='verifications/%Y/%m/%d/', null=True, blank=True)

    # توضیحات ادمین در صورت رد شدن مدرک
    admin_notes = models.TextField(blank=True, null=True)

    # چه زمانی تایید نهایی شد؟
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skill_verifications'
        verbose_name = 'Skill Verification'
        verbose_name_plural = 'Skill Verifications'

    def __str__(self):
        return f"Verification for {self.user_skill.skill_id.name} - {self.status}"