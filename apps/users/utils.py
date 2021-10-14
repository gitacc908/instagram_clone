from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from .models import User


def validate_username(username, login_page=None):
    regex = "^(\+\d{1,3})?,?\s?\d{8,13}"
    try:
        validate_email(username)
    except ValidationError:
        if re.search(regex, username):
            if not User.objects.filter(phone=username).exists():
                return {'phone': username}
            raise ValidationError('User with this phone already exists.')
        if login_page:
            return {'username': username}
        raise ValidationError('Please type valid data.')
    else:
        if not User.objects.filter(email=username).exists():
            return {'email': username}
        raise ValidationError('User with this email already exists.')
