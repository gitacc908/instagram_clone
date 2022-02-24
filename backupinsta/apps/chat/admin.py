from django.contrib import admin
from apps.chat.models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # list_display = ( 'name')
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')
