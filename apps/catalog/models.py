from django.db import models
from apps.users.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='host of post'
    )
    body = models.TextField(
        verbose_name='description of post'
    )
    likes = models.ManyToManyField(
        User, related_name='liked_posts', verbose_name='users who liked this post', blank=True
    )
    comments_off = models.BooleanField(
        default=True, verbose_name='is comments disabled?'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.id}'

    class Meta:
        ordering = ('-created', )
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Image(models.Model):
    """
    One user post can store many images
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(
        upload_to='users_post_images/'
    )

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='users_comments'
    )
    text = models.CharField(
        max_length=255, verbose_name='users comment',
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Bookmark(models.Model):
    """
    Saved posts by user
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='bookmarked'
    )
    posts = models.ManyToManyField(
        Post, related_name='bookmarks'
    )
    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        verbose_name = 'bookmarked post'
        verbose_name_plural = 'bookmarked posts'
