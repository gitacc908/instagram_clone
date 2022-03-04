from source.celery import app
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.conf import settings
from django.shortcuts import get_object_or_404
from apps.users.models import User


# @app.task
def email_users(domain, user_pk):
    user = get_object_or_404(User, id=user_pk)
    subject = 'Reset your password'
    message = render_to_string('emails/password_reset_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
