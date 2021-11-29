from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.users.models import User


class Action(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='actions', db_index=True
    )
    verb = models.CharField(
        max_length=255, verbose_name='name of action'
    )
    target_ct = models.ForeignKey(
        ContentType, blank=True, null=True, related_name='target_obj', 
        on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(
        null=True, blank=True
    )
    target = GenericForeignKey(
        'target_ct', 'target_id'
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-created', )
