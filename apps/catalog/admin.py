from django.contrib import admin
from apps.catalog.models import (
    Post, Image, Comments, Bookmark,
)


admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comments)
admin.site.register(Bookmark)
