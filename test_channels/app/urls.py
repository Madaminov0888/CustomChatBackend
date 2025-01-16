from django.urls import path
from . import views
from rest_framework import routers

urlpatterns = [
    path("channel/<str:room_name>", views.ChannelsRoom.get, name="Channels"),
    path('users/', views.UsersAPIView.as_view(), name='users'), ##all users
    path("user/<str:uid>", views.UserSingle.as_view(), name="user by id"), ## get user by id
    path("user/", views.UserPost.as_view(), name="post user"), ## post user with data
    path("post_chat/<str:creator_id>/<str:user_id>", views.CreateChat.as_view(), name="create chat"), #post chat with creator and user
    path("chats/", views.ChatsAPIView.as_view(), name= "all chats"), ## all chats
    path('chats/<str:id>', views.ChatById.as_view(), name = "chats by id"), ##get chat by id
    path("chats/user/<str:id>", views.ChatByUser.as_view(), name="chat by userid"), ##users chats
    path("messages/chat/<str:chat_id>", views.MessagesByUserAndChat.as_view()), ## exact user's, chat's messages
    path("message/put/<str:message_id>", views.MessageUpdateAPIView.as_view()),  ##message update is_it_seen
]