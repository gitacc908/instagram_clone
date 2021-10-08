from django.db import models
from django.db.models.fields import CharField, URLField
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from django.urls import reverse
from django.utils import timezone


# Custom USER MODEL
class User(PermissionsMixin, AbstractBaseUser):
    class Gender(models.TextChoices):
        MALE = 'male', 'male',
        FEMALE = 'female', 'female'

    phone = PhoneNumberField(
        verbose_name='phone', unique=True
    )
    username = CharField(
        unique=True, verbose_name='username', max_length=255
    )
    first_name = models.CharField(
        verbose_name='first_name', max_length=255, null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name='last_name', max_length=255, null=True, blank=True
    )
    biography = models.CharField(
        verbose_name='about me', max_length=255, null=True, blank=True
    )
    gender = models.CharField(
        max_length=32,
        verbose_name='sex',
        choices=Gender.choices,
        default=Gender.MALE,
    )
    email = models.EmailField(
        unique=True, verbose_name='email', max_length=255, null=True, blank=True
    )
    web_site = URLField(
        verbose_name='web site', null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone)

    def get_full_name(self):
        return f"{self.last_name}, {self.first_name}"

    # def get_absolute_url(self):
    #     return reverse('get_profile', args=[self.id])
