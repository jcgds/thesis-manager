from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)

    def is_manager_or_admin(self):
        return self.is_manager or self.is_superuser


class PersonType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class PersonData(models.Model):
    type = models.ForeignKey(PersonType, models.PROTECT)
    id_card_number = models.CharField(max_length=16, primary_key=True)  # Cédula
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    ucab_email = models.EmailField(unique=True, null=True, blank=True)
    email = models.EmailField()
    primary_phone_number = models.CharField(max_length=32)
    secondary_phone_number = models.CharField(max_length=32, null=True, blank=True)
    observations = models.CharField(max_length=1_024, null=True, blank=True)

    def __str__(self):
        return '%s %s (%s)' % (self.name, self.last_name, self.id_card_number)

    def get_short_name(self):
        return '%s. %s' % (self.name.split(' ')[0].capitalize()[0], self.last_name)

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'person_id_card_number': self.id_card_number})

    class Meta:
        verbose_name_plural = 'Person data'


class ProposalStatus(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Proposal statuses'


class Term(models.Model):
    period = models.PositiveIntegerField(unique=True)

    # TODO: Make custom validator (201915 - 201925 etc) [Unit testable]

    def __str__(self):
        return str(self.period)


class Proposal(models.Model):
    code = models.CharField(max_length=64, primary_key=True)
    submission_date = models.DateField()
    title = models.CharField(max_length=512)
    student1 = models.ForeignKey(PersonData, models.PROTECT, related_name='student1')
    student2 = models.ForeignKey(PersonData, models.PROTECT, null=True, blank=True, related_name='student2')
    academic_tutor = models.ForeignKey(PersonData, models.PROTECT, related_name='academic_tutor')
    industry_tutor = models.ForeignKey(PersonData, models.PROTECT, null=True, blank=True, related_name='industry_tutor')
    term = models.ForeignKey(Term, models.PROTECT, related_name='term')
    proposal_status = models.ForeignKey(ProposalStatus, models.PROTECT, related_name='proposal_status')

    def __str__(self):
        return '%s (%s)' % (self.title, self.code)

    def get_absolute_url(self):
        return reverse('proposal_detail', kwargs={'proposal_code': self.code})


class HistoricProposalStatus(models.Model):
    date = models.DateField(auto_now=True)
    proposal = models.ForeignKey(Proposal, models.CASCADE)
    status = models.ForeignKey(ProposalStatus, models.PROTECT)

    class Meta:
        verbose_name_plural = 'Historic proposal statuses'


class ThesisStatus(models.Model):
    name = models.CharField(max_length=64)

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
    description = models.CharField(max_length=1_024)
    thematic_category = models.CharField(max_length=50)
    submission_date = models.DateField()
    company_name = models.CharField(max_length=128, null=True, blank=True)

    def save(self, **kwargs):
        self.code = 'TG{}'.format(self.proposal.code)
        if not self.title:
            self.title = self.proposal.title
        super().save(*kwargs)

    def __str__(self):
        return '%s (%s)' % (self.title, self.code)

    class Meta:
        verbose_name_plural = 'Thesis'


class HistoricThesisStatus(models.Model):
    date = models.DateField(auto_now=True)
    thesis = models.ForeignKey(Thesis, models.CASCADE)
    status = models.ForeignKey(ThesisStatus, models.PROTECT)

    class Meta:
        verbose_name_plural = 'Historic thesis statuses'


class Defence(models.Model):
    MAX_JUDGES = 3
    thesis = models.ForeignKey(Thesis, models.PROTECT)
    code = models.CharField(max_length=68, primary_key=True)
    date_time = models.DateTimeField()
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    is_publication_mention = models.BooleanField(default=False)
    is_honorific_mention = models.BooleanField(default=False)
    corrections_submission_date = models.DateField(null=True, blank=True)
    was_grade_loaded = models.BooleanField(default=False)
    observations = models.TextField(null=True, blank=True)

    def save(self, **kwargs):
        self.code = 'D{}'.format(self.thesis.code)
        super().save(*kwargs)

    def get_students(self):
        return self.thesis.proposal.student1, self.thesis.proposal.student2

    def get_academic_tutor(self):
        return self.thesis.proposal.academic_tutor

    def get_complete_jury(self):
        return Jury.objects.filter(defence=self)

    def get_jury_members(self):
        """
        Get the principal jury members for this defence, excluding the backup Judge.
        """
        return Jury.objects.filter(defence=self, is_backup_jury=False)

    def get_backup_judge(self):
        """
        Get the backup judge for this defence.
        """
        backup_juries = Jury.objects.filter(defence=self, is_backup_jury=True)
        if len(backup_juries) > 1:
            print('More than one backup jury for defence %s.' % self.code)
        elif len(backup_juries) == 0:
            return None
        else:
            return backup_juries[0]

    def current_status(self):
        return HistoricThesisStatus.objects.filter(thesis=self.thesis).order_by('-date').first()


class Jury(models.Model):
    person = models.ForeignKey(PersonData, models.PROTECT)
    defence = models.ForeignKey(Defence, models.PROTECT)
    confirmed_assistance = models.BooleanField(default=False)
    is_backup_jury = models.BooleanField(default=False)
