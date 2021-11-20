from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from django.urls import reverse
from django.utils import timezone


class User(PermissionsMixin, AbstractBaseUser):
    class Gender(models.TextChoices):
        MALE = 'male', 'male',
        FEMALE = 'female', 'female'

    phone = PhoneNumberField(
        verbose_name='phone', unique=True
    )
    username = models.CharField(
        unique=True, verbose_name='username', max_length=255
    )
    image = models.ImageField(
        upload_to='profile_images/'
    )
    full_name = models.CharField(
        verbose_name='full_name', max_length=255, null=True, blank=True
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
    web_site = models.URLField(
        verbose_name='web site', null=True, blank=True
    )
    following = models.ManyToManyField(
        'self', through='Contact', related_name='followers', symmetrical=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args=[self.username])


class Contact(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rel_from_set'
    )
    user_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rel_to_set'
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

    class Meta:
        ordering = ('created', )
