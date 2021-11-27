from django import template
from apps.users.models import User

from django.templatetags.static import static


register = template.Library()


def get_user_photo(user):
    if user.image:
        return user.image.url
    else:
        return static('assets/default-user.png')


register.filter('get_user_photo', get_user_photo)
