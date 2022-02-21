from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    # re_path(r'ws/chat/room/(?P<user_id>\d+)/$', consumers.ChatConsumer),
    re_path(r'ws/chat/room/private/(?P<username>\w+)/$', consumers.PrivateChatConsumer.as_asgi()),
    # re_path(r'ws/chat/room/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/default/', consumers.ChatConsumer.as_asgi()),
]
