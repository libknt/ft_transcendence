# chat/routing.py
from django.urls import re_path
from . import chat_consumers, room_consumers

websocket_urlpatterns = [
    re_path(r"^ws/chat/rooms/?$", room_consumers.RoomConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>[\w-]+)/$", chat_consumers.ChatConsumer.as_asgi()),
]
