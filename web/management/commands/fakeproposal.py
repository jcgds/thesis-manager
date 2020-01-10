from django.core.management.base import BaseCommand
from faker import Faker

from web.models import PersonData, Proposal, ProposalStatus, PersonType, Term


class Command(BaseCommand):
    help = 'Generates and inserts fake data into the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        loc_faker = Faker(['es_ES', 'es_MX', 'en_US'])
        faker = Faker()
        proposal_statuses = ProposalStatus.objects.all()
        terms = Term.objects.all()
        if not terms:
            Term(
                period='marzo-julio'
            ).save()
        for i in range(6):
            Proposal(
                code=loc_faker.random_int(),
                submission_date=loc_faker.date_time_between(start_date='-1y', end_date='now'),
                title=loc_faker.sentence(nb_words=6),
                proposal_status=faker.random.choice(proposal_statuses),
                student1=faker.random.choice(PersonData.objects.filter(type=PersonType.objects.get(name='Estudiante').id)),
                academic_tutor=faker.random.choice(PersonData.objects.filter(type=PersonType.objects.get(name='Profesor').id)),
                industry_tutor=faker.random.choice(PersonData.objects.filter(type=PersonType.objects.get(name='Externo').id)),
                term=faker.random.choice(Term.objects.all()),
            ).save()
        self.stdout.write(self.style.SUCCESS('Successfully created Proposals'))
