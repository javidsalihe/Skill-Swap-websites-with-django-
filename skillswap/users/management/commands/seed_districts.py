from django.core.management.base import BaseCommand
from users.models import District
from users.models import City


class Command(BaseCommand):
    help = 'Seed districts'
    def handle(self, *args, **options):
        all_districts = {
            "Berlin": [
                "Spandau",
                "Marzahn",
                "Pankow",
                "Mitte",
                "Tempelhof-Schöneberg",
                "Charlottenburg",
                "Neukölln",
                "Steglitz-Zehlendorf",
                "Lichtenberg",
                "Friedrichshain-Kreuzberg",
                "Treptow-Köpenick",
                "Reinickendorf"
            ],

            "Hamburg": [
                "Hamburg-Mitte",
                "Altona",
                "Eimsbüttel",
                "Hamburg-Nord",
                "Wandsbek",
                "Bergedorf",
                "Harburg"
            ],

            "Bayern": [
                "Altstadt-Lehel",
                "Ludwigsvorstadt-Isarvorstadt",
                "Maxvorstadt",
                "Schwabing-West",
                "Au-Haidhausen",
                "Sendling",
                "Sendling-Westpark",
                "Schwanthalerhöhe",
                "Neuhausen-Nymphenburg",
                "Moosach",
                "Milbertshofen-Am Hart",
                "Schwabing-Freimann",
                "Bogenhausen",
                "Berg am Laim",
                "Trudering-Riem",
                "Ramersdorf-Perlach",
                "Obergiesing-Fasangarten",
                "Untergiesing-Harlaching",
                "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln",
                "Hadern",
                "Pasing-Obermenzing",
                "Aubing-Lochhausen-Langwied",
                "Allach-Untermenzing",
                "Feldmoching-Hasenbergl",
                "Laim"
            ],

            "Baden-Württemberg": [
                "Stuttgart-Mitte",
                "Stuttgart-Nord",
                "Stuttgart-Ost",
                "Stuttgart-Süd",
                "Bad Cannstatt",
                "Birkach",
                "Botnang",
                "Degerloch",
                "Feuerbach",
                "Hedelfingen",
                "Möhringen",
                "Mühlhausen",
                "Münster",
                "Obertürkheim",
                "Plieningen",
                "Sillenbuch",
                "Stammheim",
                "Untertürkheim",
                "Vaihingen",
                "Wangen",
                "Weilimdorf",
                "Zuffenhausen"
            ]
        }

        for city_name, districts in all_districts.items():
            cities_obj = City.objects.filter(city_name=city_name).first()
            if not cities_obj:
                self.stdout.write(self.style.WARNING(f"{city_name} not found!"))
                continue
            else :
                for district in districts:
                    District.objects.get_or_create(city=cities_obj, district_name=district)





