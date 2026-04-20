from django.core.management.base import BaseCommand
from users.models import Country

class Command(BaseCommand):
    help = 'Seed countries'
    def handle(self, *args, **options):
        countries_list = [
            {"name": "Germany", "code": "DE"},
            {"name": "France", "code": "FR"},
            {"name": "Italy", "code": "IT"},
            {"name": "Spain", "code": "ES"},
        ]

        for item in countries_list:
            Country.objects.get_or_create(country_name=item['name'], country_code=item['code'])


