from django.core.management.base import BaseCommand
from users.models import Language


class Command(BaseCommand):
    help = 'Seed languages'

    def handle(self, *args, **options):
        languages = [
            {"language_name": "Deutsch", "language_code": "de"},
            {"language_name": "English", "language_code": "en"},
            {"language_name": "Mandarin Chinese", "language_code": "zh"},
            {"language_name": "Hindi", "language_code": "hi"},
            {"language_name": "Spanish", "language_code": "es"},
            {"language_name": "Arabic", "language_code": "ar"},
            {"language_name": "French", "language_code": "fr"},
            {"language_name": "Bengali", "language_code": "bn"},
            {"language_name": "Portuguese", "language_code": "pt"},
            {"language_name": "Russian", "language_code": "ru"},
            {"language_name": "Urdu", "language_code": "ur"},

            {"language_name": "Dutch", "language_code": "nl"},
            {"language_name": "Dari (Afghan Persian)", "language_code": "fa"},
            {"language_name": "Italian", "language_code": "it"},
            {"language_name": "Ukrainian", "language_code": "uk"},
            {"language_name": "Turkish", "language_code": "tr"},
        ]

        for language in languages:
            obj, created = Language.objects.get_or_create(
                language_name=language["language_name"],
                language_code=language["language_code"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.language_name}"))
            else:
                self.stdout.write(f"Exists: {obj.language_name}")