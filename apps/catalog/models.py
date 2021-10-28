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
        User, related_name='liked_posts', verbose_name='users who liked this post'
    )
    comments_on = models.BooleanField(
        default=True, verbose_name='is comments allowed?'
    )

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Image(models.Model):
    """
    One user post can store many images
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='image'
    )
    image = models.ImageField(
        upload_to='users_post_images/'
    )

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'


class Comments(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='users_comments'
    )
    text = models.CharField(
        max_length=255, verbose_name='users comment',
    )

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Bookmark(models.Model):
    """
    Saved posts by user
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmarked_user_posts'
    )
    posts = models.ManyToManyField(
        Post, related_name='bookmarked_posts'
    )
    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = 'bookmarked post'
        verbose_name_plural = 'bookmarked posts'
