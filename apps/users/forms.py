from django import forms 
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Repeat password',
    #                             widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('phone', 'email', 'full_name', 'username')
