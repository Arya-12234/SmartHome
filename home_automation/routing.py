# home_automation/routing.py (if you use this file)

from django.urls import re_path

from automation import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/', consumers.ChatConsumer.as_asgi()),
]
