from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from .models import User


def validate_username(username, login_page=None):
    regex = "^(\+\d{1,3})?,?\s?\d{8,13}"
    if login_page:
        try:
            validate_email(username)
        except ValidationError:
            """
            validate phone
            """
            if re.search(regex, username):
                return {'phone': username}
            return {'username': username}
        return {'email': username}            
    else:
        # register page
        try:
            validate_email(username)
        except ValidationError:
            """
            validate phone
            """
            if re.search(regex, username):
                if not User.objects.filter(phone=username).exists():
                    return {'phone': username}
                raise ValidationError('User with this phone already exists.')
            raise ValidationError('Please type phone or email address.')
        else:
            if User.objects.filter(email=username).exists():
                raise ValidationError('User with this email already exists.')
            return {'email': username}
