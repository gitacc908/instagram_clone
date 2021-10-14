from django import forms 
from .models import User
from .utils import validate_username


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
