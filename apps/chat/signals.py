from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import User
from apps.chat.models import Room

@receiver(post_save, sender=User)
def user_room(sender, instance, created, **kwargs):
    if created:
        Room.objects.create(user=instance, name=instance.username)
