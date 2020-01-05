from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)


class PersonData(models.Model):
    TEACHER = 0
    STUDENT = 1
    EXTERNAL = 2
    TYPE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (EXTERNAL, 'External')
    )
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    id_card_number = models.CharField(max_length=16, unique=True)  # Cédula
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    ucab_email = models.EmailField(unique=True, null=True, blank=True)
    email = models.EmailField()
    primary_phone_number = PhoneNumberField()
    secondary_phone_number = PhoneNumberField(null=True, blank=True)
    observations = models.CharField(max_length=1_024, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Person data'


class Term(models.Model):
    name = models.CharField(max_length=16)

    # TODO: Make custom validator (201915 - 201925 etc) [Unit testable]

    def __str__(self):
        return self.name


class ProposalStatus(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Proposal statuses'


class Proposal(models.Model):
    code = models.CharField(max_length=64, primary_key=True)
    submission_date = models.DateField()
    title = models.CharField(max_length=256)
    student1 = models.ForeignKey(PersonData, models.PROTECT, related_name='student1')
    student2 = models.ForeignKey(PersonData, models.PROTECT, null=True, blank=True, related_name='student2')
    academic_tutor = models.ForeignKey(PersonData, models.PROTECT, related_name='academic_tutor')
    industry_tutor = models.ForeignKey(PersonData, models.PROTECT, null=True, blank=True, related_name='industry_tutor')
    term = models.ForeignKey(Term, models.PROTECT, related_name='term')


class HistoricProposalStatus(models.Model):
    date = models.DateField(auto_now=True)
    proposal = models.ForeignKey(Proposal, models.CASCADE)
    status = models.ForeignKey(ProposalStatus, models.PROTECT)
