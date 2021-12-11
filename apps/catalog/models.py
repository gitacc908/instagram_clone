from django.db import models
from apps.users.models import User
from apps.catalog.validators import validate_tag


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='host of post'
    )
    body = models.TextField(
        verbose_name='description of post', null=True, blank=True
    )
    likes = models.ManyToManyField(
        User, related_name='liked_posts', verbose_name='users who liked this post', blank=True
    )
    tags = models.ManyToManyField(
        'Tag', related_name='posts', verbose_name='tags of post', blank=True
    )
    total_likes = models.PositiveIntegerField(
        db_index=True, default=0
    )
    comments_off = models.BooleanField(
        default=False, verbose_name='is comments disabled?'
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
    likes = models.ManyToManyField(
        User, related_name='liked_comments', symmetrical=False, blank=True
    )
    total_likes = models.PositiveIntegerField(
        default=0, db_index=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'author: {self.user.username}, comment: {self.text}'
    
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


class Tag(models.Model):
    name = models.CharField(
        max_length=30, verbose_name='Tag', validators=[validate_tag]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class CommentReply(models.Model):
    text = models.CharField(
        max_length=255, verbose_name='reply'
    )
    user = models.ForeignKey(
        User, related_name='comment_replys', on_delete=models.CASCADE,
        verbose_name='author of reply'
    )
    comment = models.ForeignKey(
        Comment, related_name='replies', on_delete=models.CASCADE,
        verbose_name='replied comment'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='answer date'
    )
    
    def __str__(self):
        return f'author{self.user} reply: {self.text}'

    class Meta:
        verbose_name = 'Comment Reply'
        verbose_name_plural = 'Comment Replies'
        ordering = ('-created',)
