from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)


class PersonData(models.Model):
    TEACHER = 0
    STUDENT = 1
    EXTERNAL = 2
    TYPE_CHOICES = (
        (TEACHER, 'Profesor'),
        (STUDENT, 'Estudiante'),
        (EXTERNAL, 'Externo')
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

    def __str__(self):
        return '%s %s (%s)' % (self.name, self.last_name, self.id_card_number)

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'person_id_card_number': self.id_card_number})

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
    title = models.CharField(max_length=512)
    student1 = models.ForeignKey(PersonData, models.PROTECT, related_name='student1')
    student2 = models.ForeignKey(PersonData, models.PROTECT, null=True, blank=True, related_name='student2')
    academic_tutor = models.ForeignKey(PersonData, models.PROTECT, related_name='academic_tutor')
    industry_tutor = models.ForeignKey(PersonData, models.PROTECT, null=True, blank=True, related_name='industry_tutor')
    term = models.ForeignKey(Term, models.PROTECT, related_name='term')

    def __str__(self):
        return '%s (%s)' % (self.title, self.code)


class HistoricProposalStatus(models.Model):
    date = models.DateField(auto_now=True)
    proposal = models.ForeignKey(Proposal, models.CASCADE)
    status = models.ForeignKey(ProposalStatus, models.PROTECT)

    class Meta:
        verbose_name_plural = 'Historic proposal statuses'


class ThesisStatus(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Thesis statuses'


class Thesis(models.Model):
    proposal = models.ForeignKey(Proposal, models.PROTECT)
    code = models.CharField(max_length=66, primary_key=True)
    title = models.CharField(max_length=512)
    delivery_term = models.ForeignKey(Term, models.PROTECT)
    NRC = models.CharField(max_length=32)
    description = models.CharField(max_length=50)
    thematic_category = models.CharField(max_length=50)
    submission_date = models.DateField()
    company_name = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Thesis'


class HistoricThesisStatus(models.Model):
    date = models.DateField(auto_now=True)
    thesis = models.ForeignKey(Thesis, models.CASCADE)
    status = models.ForeignKey(ThesisStatus, models.PROTECT)

    class Meta:
        verbose_name_plural = 'Historic thesis statuses'


class Defence(models.Model):
    thesis = models.ForeignKey(Thesis, models.PROTECT)
    code = models.CharField(max_length=68, primary_key=True)
    date_time = models.DateTimeField()
    grade = models.PositiveSmallIntegerField()
    is_publication_mention = models.BooleanField()
    is_honorific_mention = models.BooleanField()
    corrections_submission_date = models.DateField(null=True, blank=True)
    was_grade_loaded = models.BooleanField()
    observations = models.TextField()


class Jury(models.Model):
    person = models.ForeignKey(PersonData, models.PROTECT)
    defence = models.ForeignKey(Defence, models.PROTECT)
    confirmed_assistance = models.BooleanField(default=False)
    is_backup_jury = models.BooleanField(default=False)
    #  TODO: Field is_thesis_tutor which can be calculated with a query through the proposal's academic tutor (page 2-3)
    #        Maybe it's only shown when seeing a defence details
