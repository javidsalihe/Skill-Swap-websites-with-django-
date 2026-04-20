import random
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import (
    User, Address, Skill, ExchangeRequest, Exchange,
    Rating, Comment, ContactMessage, UserSkill, District
)


class Command(BaseCommand):
    help = 'Erzeugt Testdaten für das Skillswap-Projekt'

    def handle(self, *args, **options):
        fake = Faker(['de_DE'])
        count = 30

        self.stdout.write(self.style.SUCCESS(f"Starte das Erstellen von {count} Testdatensätzen..."))

        districts = list(District.objects.all())
        skills = list(Skill.objects.all())

        if not districts or not skills:
            self.stdout.write(self.style.ERROR("Fehler: District oder Skill Tabellen sind leer!"))
            return

        for i in range(count):
            addr = Address.objects.create(
                district=random.choice(districts),
                street_name=fake.street_name(),
                street_number=fake.building_number(),
                postal_code=fake.postcode(),
                latitude=float(fake.latitude()),
                longitude=float(fake.longitude())
            )

            username = f"{fake.user_name()}_{random.randint(1000, 9999)}"
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                address_id=addr,
                bio=fake.text(max_nb_chars=200)
            )

            PROFICIENCY_LEVELS = [1, 2, 3, 4, 5]
            user_skill = UserSkill.objects.create(
                user_id=user,
                skill_id=random.choice(skills),
                proficiency_level=random.choice(PROFICIENCY_LEVELS)
            )

            ex_request = ExchangeRequest.objects.create(
                requester=user,
                requested_skill=random.choice(skills),
                offered_skill=user_skill,
                title=f"Suche Hilfe bei {fake.word()}",
                description=fake.sentence(),
                status=ExchangeRequest.Status.AVAILABLE
            )

            ContactMessage.objects.create(
                name=user.get_full_name() or user.username,
                email=user.email,
                message=fake.paragraph()
            )

        self.stdout.write(self.style.SUCCESS(f"Erfolgreich {count} Benutzer"))

        all_users = list(User.objects.all())
        for _ in range(20):
            try:
                u1, u2 = random.sample(all_users, 2)
                exchange = Exchange.objects.create(
                    user_x=u1,
                    user_y=u2,
                    skill_from_x_to_y=random.choice(skills),
                    skill_from_y_to_x=random.choice(skills),
                    status=Exchange.Status.COMPLETED
                )

                rating = Rating.objects.create(
                    exchange=exchange,
                    author=u1,
                    target_user=u2,
                    score=random.randint(4, 5),
                    comment=fake.sentence()
                )
            except:
                continue

        self.stdout.write(self.style.SUCCESS("Alle Testdaten wurden erfolgreich geladen!"))