from django import forms
from django.core.exceptions import ValidationError
from .models import User
from .utils import validate_username

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import (
    password_validation,
)
from django.core.validators import validate_email
from apps.users.tasks import email_users
from django.contrib.sites.shortcuts import get_current_site
from apps.users.choices import *


class RegisterForm(forms.ModelForm):
    email_or_phone = forms.CharField(
        max_length=255, required=True
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('full_name', 'username')

    def clean_email_or_phone(self):
        return validate_username(
            self.cleaned_data.get('email_or_phone')
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        data = self.cleaned_data.get('email_or_phone')
        if 'phone' in data:
            user.phone = data.get('phone')
        elif 'email' in data:
            user.email = data.get('email')
        user.is_active = 1
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class LoginForm(forms.Form):
    username_email_phone = forms.CharField(
        max_length=255, required=True, label='username'
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    def clean_username_email_phone(self):
        return validate_username(
            self.cleaned_data.get('username_email_phone'),
            login_page=True
        )


class UserEmailForm(forms.Form):
    email = forms.CharField(
        max_length=255, required=True, label='email'
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Please type your email address.')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                'Given email is not registered in this site.')
        else:
            domain = get_current_site(self.request)
            # sending asynchronomous emails
            email_users.delay(str(domain), user.pk)
            return email


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image',)


class UserForm(forms.ModelForm):
    # like_notification = forms.ChoiceField(
    #     choices=LIKE, widget=forms.RadioSelect())
    # comment_notification = forms.ChoiceField(
    #     choices=COMMENT, widget=forms.RadioSelect())
    # comment_like_notification = forms.ChoiceField(
    #     choices=COMMENT_LIKE, widget=forms.RadioSelect())
    # follow_request_notification = forms.ChoiceField(
    #     choices=FOLLOW_REQUEST, widget=forms.RadioSelect())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'phone', 'username', 'image', 'full_name', 'biography', 
            'gender', 'email', 'web_site', 'is_active', 'is_staff', 
            'password'
        ]
