from django.core.management.base import BaseCommand
from faker import Faker

from web.models import PersonData, PersonType


class Command(BaseCommand):
    help = 'Generates and inserts fake data into the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        loc_faker = Faker(['es_ES', 'es_MX', 'en_US'])
        faker = Faker()
        id_types = ['V', 'E']
        person_types = PersonType.objects.all()
        for i in range(20):
            PersonData(
                # If the types are modified in the PersonData model, it should be updated here too
                type=faker.random.choice(list(person_types)),
                id_card_number='%s%d' % (faker.random.choice(id_types), loc_faker.random_int(1_000_000, 30_000_000)),
                name=loc_faker.first_name(),
                last_name=loc_faker.last_name(),
                ucab_email=loc_faker.company_email(),
                email=loc_faker.email(),
                primary_phone_number=loc_faker.phone_number()
            ).save()
        self.stdout.write(self.style.SUCCESS('Successfully created Persons'))
