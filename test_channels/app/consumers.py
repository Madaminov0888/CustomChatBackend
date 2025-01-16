from channels.generic.websocket import WebsocketConsumer
import json
from django.http import Http404
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import AppUser, Chat, Message
from .serializer import AppUserSerializer, ChatSerializer, MessageSerializer
from django.db.models import Q



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        text_json = json.loads(text_data)
        if text_json["type"] == "users_chats":
            user_id = text_json["chat_creator_id"]
            print(user_id)
            chats_query = Chat.objects.filter(Q(chat_creator__id = user_id) | Q(chat_user__id = user_id))
            serialized = ChatSerializer(chats_query, many = True).data
            self.send(text_data=json.dumps(serialized))
        else:
            print(f"Type Not Found: {text_json}")
            


class MessageConsumer(WebsocketConsumer):
    def connect(self):
        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_name = chat_id
        chat = Chat.objects.filter(id = chat_id)
        if len(chat) == 1:
            self.room_group_name = f'chat_{self.room_name}'

            # Add user to the room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        else:
            raise Http404("Chat not found")

        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        request_type = text_data_json["type"]
        if request_type == "message":
            message = text_data_json["message"]
            message_id = text_data_json["message_id"]
            sender_id = text_data_json["sender"]
            sender = AppUser.objects.get(id = sender_id)
            chat = Chat.objects.get(id = self.room_name)
            message = Message.objects.create(id = message_id,chat = chat, sender = sender, content = message, is_it_seen = False)
            message_json = json.dumps(MessageSerializer(message, many = False).data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_creator.id, 
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_user.id,
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )
        elif request_type == "message_with_image":
            message = text_data_json["message"]
            message_id = text_data_json["message_id"]
            sender_id = text_data_json["sender"]
            image_url = text_data_json["image_url"]
            sender = AppUser.objects.get(id = sender_id)
            chat = Chat.objects.get(id = self.room_name)
            message = Message.objects.create(id = message_id,chat = chat, sender = sender, content = message, is_it_seen = False, image_URL = image_url)
            message_json = json.dumps(MessageSerializer(message, many = False).data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_creator.id, 
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_user.id,
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )
        elif request_type == "message_with_video":
            message = text_data_json["message"]
            message_id = text_data_json["message_id"]
            sender_id = text_data_json["sender"]
            video_url = text_data_json["video_url"]
            sender = AppUser.objects.get(id = sender_id)
            chat = Chat.objects.get(id = self.room_name)
            message = Message.objects.create(id = message_id,chat = chat, sender = sender, content = message, is_it_seen = False, video_url = video_url)
            message_json = json.dumps(MessageSerializer(message, many = False).data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_creator.id, 
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_user.id,
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )
        elif request_type == "message_with_audio":
            message = text_data_json["message"]
            message_id = text_data_json["message_id"]
            sender_id = text_data_json["sender"]
            audio_url = text_data_json["audio_url"]
            sender = AppUser.objects.get(id = sender_id)
            chat = Chat.objects.get(id = self.room_name)
            message = Message.objects.create(id = message_id,chat = chat, sender = sender, content = message, is_it_seen = False, audio_url = audio_url)
            message_json = json.dumps(MessageSerializer(message, many = False).data)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_creator.id, 
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                chat.chat_user.id,
                {
                    'type': 'chat_update',
                    'chat_id': self.room_name,
                    'message': message_json
                }
            )
        elif request_type == "message_state":
            message_id = text_data_json["message_id"]
            sender_id = text_data_json["sender"]
            chat = Chat.objects.get(id = self.room_name)
            Message.objects.filter(chat=chat, id = message_id).update(is_it_seen=True)
            message = Message.objects.get(id = message_id, chat=chat)
            message_json = json.dumps(MessageSerializer(message, many = False).data)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'message_state',
                    'chat_id':self.room_name,
                    'message': message_json
                }
            )


    # Receive message from room group
    def message_state(self, event):
        message = event['message']
        self.send(text_data=message)


    def chat_message(self, event):
        message = event['message']
        self.send(text_data=message)


class HomeViewConsumer(WebsocketConsumer):
    def connect(self):
        uid = self.scope["url_route"]["kwargs"]["uid"]
        self.room_name = uid
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def chat_update(self, event):
        chat_id = event['chat_id']
        message = event['message']
        self.send(text_data=message)















##UDP connection phone calls handler
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["uid"]
        await self.channel_layer.group_add(
            f"user_{self.user_id}", self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user_id}", self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            print(f"Received from client: {text_data}")
            data = json.loads(text_data)
            action = data.get("action")
            
            if action in ["send_offer", "send_answer", "send_candidate"]:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "call_message",
                        "message": data,
                    }
                )

    async def call_message(self, event):
        message = event["message"]
        print(f"Broadcasting to group: {message}")
        await self.send(text_data=json.dumps(message))