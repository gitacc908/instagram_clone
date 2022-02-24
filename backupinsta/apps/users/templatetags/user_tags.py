from os import replace
from django import template
from apps.users.models import User

from django.templatetags.static import static


register = template.Library()


def get_user_photo(user):
    if user.image:
        return user.image.url
    else:
        return static('assets/default-user.png')

@register.simple_tag
def format_current_url_with_lang_code(request, language_code, curren_lang_code):
    return request.path.replace(curren_lang_code, language_code)


register.filter('get_user_photo', get_user_photo)
