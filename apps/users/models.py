from email.policy import default
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from .choices import (
    LIKE, COMMENT_LIKE, COMMENT, FOLLOW_REQUEST, OFF, FROM_ALL, FROM_FOLLOWING
)


class User(PermissionsMixin, AbstractBaseUser):
    class Gender(models.TextChoices):
        MALE = 'male', 'male',
        FEMALE = 'female', 'female'

    phone = PhoneNumberField(
        _('phone'), unique=True, null=True, blank=True
    )
    username = models.CharField(
        _('username'), unique=True, max_length=255
    )
    image = models.ImageField(
        _('image'), upload_to='profile_images/', null=True, blank=True
    )
    full_name = models.CharField(
        _('full name'), max_length=255, null=True, blank=True
    )
    biography = models.CharField(
        _('about me'), max_length=255, null=True, blank=True
    )
    gender = models.CharField(
        _('gender'),
        max_length=32,
        # verbose_name='sex',
        choices=Gender.choices,
        default=Gender.MALE,
    )
    email = models.EmailField(
        _('email'), unique=True, max_length=255, null=True, blank=True
    )
    web_site = models.URLField(
        _('web site'), null=True, blank=True
    )
    following = models.ManyToManyField(
        'self', through='Contact', related_name='followers', symmetrical=False
    )

    # checkbox fields
    like_notification = models.CharField(
        choices=LIKE, default=FROM_ALL, blank=True, max_length=50,
    )
    comment_notification = models.CharField(
        choices=COMMENT, default=FROM_ALL, blank=True, max_length=50,
    )
    comment_like_notification = models.CharField(
        choices=COMMENT_LIKE, default=FROM_ALL, blank=True, max_length=50,
    )
    follow_request_notification = models.CharField(
        choices=FOLLOW_REQUEST, default=FROM_ALL, blank=True, max_length=50,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('-date_joined',)
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
