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
    ucab_email = models.EmailField(unique=True)
    email = models.EmailField()
    primary_phone_number = PhoneNumberField()
    secondary_phone_number = PhoneNumberField()
    observations = models.CharField(max_length=1_024, default='')

    class Meta:
        verbose_name_plural = 'Person data'
