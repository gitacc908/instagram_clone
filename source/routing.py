from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chat import routing as chat_routing



application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(chat_routing.websocket_urlpatterns)
    ),
})
