from django.core.management.base import BaseCommand
from users.models import Country
from users.models import City
class Command(BaseCommand):

    def handle(self, *args, **options):

        countries_cities = {
            "Germany":[
                "Baden-Württemberg",
                "Bayern",
                "Berlin",
                "Brandenburg",
                "Bremen",
                "Hamburg",
                "Hesse",
                "Lower Saxony",
                "Mecklenburg-Vorpommern",
                "North Rhine-Westphalia",
                "Rhineland-Palatinate",
                "Saarland",
                "Saxony",
                "Saxony-Anhalt",
                "Schleswig-Holstein",
                "Thuringia"
            ],
            "France": ["Paris", "Marseille", "Lyon", "Bordeaux"],
            "Italy": ["Rome", "Milan", "Florence", "Naples"],
            "Spain": ["Madrid", "Barcelona", "Seville", "Valencia"]
        }


        for country_name, cities in countries_cities.items():
            country_obj = Country.objects.filter(country_name=country_name).first()
            if not country_obj:
                self.stdout.write(self.style.WARNING(f"{country_name} not found!"))
                continue
            else :
                for item in cities:
                    City.objects.get_or_create(country=country_obj, city_name=item)




