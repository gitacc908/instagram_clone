from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/room/private/(?P<username>\w+)/$', consumers.PrivateChatConsumer.as_asgi()),
    re_path(r'ws/chat/room/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
