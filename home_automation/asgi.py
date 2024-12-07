

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from automation.urls import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_automation.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests normally
    "websocket": AuthMiddlewareStack(  # Handle WebSocket connections
        URLRouter(websocket_urlpatterns),  # Use the WebSocket URL patterns from chatbot/routing.py
    ),
})
