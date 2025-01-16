from rest_framework import serializers
from .models import AppUser, Chat, Message


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = AppUserSerializer()
    class Meta:
        model = Message
        fields = "__all__"



class ChatSerializer(serializers.ModelSerializer):
    chat_creator = AppUserSerializer()
    chat_user = AppUserSerializer()
    chat_messages = serializers.ManyRelatedField(
        read_only=True,
        child_relation=MessageSerializer()
    )

    class Meta:
        model = Chat
        fields = "__all__"

