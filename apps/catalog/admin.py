from django.contrib import admin
from apps.catalog.models import (
    Post, Image, Comment, Bookmark,
)


admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Bookmark)
