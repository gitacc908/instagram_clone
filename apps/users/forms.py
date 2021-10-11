from django import forms 
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


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
        data = self.cleaned_data.get('email_or_phone')
        regex = "^(\+\d{1,3})?,?\s?\d{8,13}"
        try:
            validate_email(data)
        except ValidationError:
            if re.search(regex, data):
                return {'phone': data}
            raise ValidationError('Please type valid data.')
        return {'email': data}
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        data = self.cleaned_data.get('email_or_phone')
        if 'phone' in data:
            user.phone = data.get('phone')
        elif 'email' in data:
            user.email = data.get('email')
        user.is_active = 1
        user.save()
        return user
