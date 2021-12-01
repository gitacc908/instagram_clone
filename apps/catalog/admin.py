from django.contrib import admin
from apps.catalog.models import (
    Post, Image, Comment, Bookmark,
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

admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Bookmark)
