from django.contrib import admin
from apps.catalog.models import (
    Post, Image, Comment, Bookmark, CommentReply, Tag
)

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'total_likes', 'body', 'comments_off', 'created'
    )
    list_filter = (
        'author', 'comments_off', 'created'
    )
    search_fields = (
        'body', 'author'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post', 'user', 'text', 
    )
    list_filter = (
        'post', 
    )
    # search_fields = (
    #     'body', 'author'
    # )
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(CommentReply)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bookmark)
