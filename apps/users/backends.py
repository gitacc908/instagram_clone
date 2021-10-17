from django.contrib.auth.backends import ModelBackend
from .models import User


class UserBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        try:
            if 'email' in username:
                user = User.objects.get(email=username.get('email'))
            elif 'phone' in username:
                user = User.objects.get(phone=username.get('phone'))
            elif 'username' in username:
                user = User.objects.get(username=username.get('username'))
            if user.check_password(password) is True:
                if user.is_active:
                    return user
            #     raise forms.ValidationError("User with provided credentials banned from this site.")
            # else:
            #     raise forms.ValidationError("User with provided credentials doesn't exist.")
            return None
        except User.DoesNotExist:
            # raise forms.ValidationError("User with provided credentials doesn't exist.")
            return None