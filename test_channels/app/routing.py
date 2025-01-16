from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chats/", consumers.ChatConsumer.as_asgi()),
    # re_path(r"ws/messages/(?P<chat_id>\w+)/", consumers.MessageConsumer.as_asgi()),
    path("ws/messages/<str:chat_id>", consumers.MessageConsumer.as_asgi()),
    path("ws/user/<str:uid>", consumers.HomeViewConsumer.as_asgi()),
    path("ws/user_call/<str:uid>", consumers.CallConsumer.as_asgi()),
]