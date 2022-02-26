from django.core.exceptions import ValidationError 
from django.utils.translation import gettext_lazy as _


def validate_tag(value):
    hash = value[0]
    if hash != '#':
         raise ValidationError("Tag should start with hash character!")
    if value.count(hash) > 1:
        raise ValidationError("Tag should contain only one hash")
    return value
