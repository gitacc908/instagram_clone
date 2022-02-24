from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from apps.catalog.models import Post, Comment


@receiver(m2m_changed, sender=Post.likes.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(m2m_changed, sender=Comment.likes.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()
