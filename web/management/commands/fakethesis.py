from django.core.management.base import BaseCommand
from faker import Faker

from web.models import Thesis, ThesisStatus, Term, Proposal, HistoricThesisStatus


class Command(BaseCommand):
    help = 'Generates and inserts fake data into the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        loc_faker = Faker(['es_ES', 'es_MX', 'en_US'])
        faker = Faker()
        thesis_statuses = ThesisStatus.objects.all()
        for i in range(6):
            proposal = faker.random.choice(
                Proposal.objects.exclude(code__in=Thesis.objects.all().values('proposal__code')))
            thesis = Thesis(
                # If the types are modified in the PersonData model, it should be updated here too
                title=proposal.title,
                proposal=proposal,
                delivery_term=faker.random.choice(Term.objects.all()),
                NRC=loc_faker.random_int(),
                description=loc_faker.paragraph(nb_sentences=3),
                thematic_category=loc_faker.sentence(nb_words=3),
                submission_date=loc_faker.date_time_between(start_date=proposal.submission_date, end_date='now'),
                company_name=loc_faker.company()
            )
            thesis.save()

            HistoricThesisStatus(
                thesis=thesis,
                status=faker.random.choice(list(thesis_statuses))
            ).save()
        self.stdout.write(self.style.SUCCESS('Successfully created Thesis'))
