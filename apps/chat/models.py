from django.db import models
from apps.users.models import User


class Room(models.Model):
    name = models.CharField(max_length=128)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_room',
        null=True
    )
    # only using if room name is common
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()
    
    class Meta:
        # unique_together = ('user_1', 'user_1')
        verbose_name = 'user room'
        verbose_name_plural = 'users rooms'

    def __str__(self):
        if not self.user:
            return self.name
        return f'{self.name} ({self.user})'


class Message(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='user_messages')
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, related_name='room_messages')
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
