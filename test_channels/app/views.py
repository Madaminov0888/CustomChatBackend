from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from django import http
from django.db.models import Q
from .models import AppUser, Chat, Message
from django.db.models import Max
from .serializer import AppUserSerializer, ChatSerializer, MessageSerializer


class ChannelsRoom(APIView):

    def get(request, room_name):
        return render(request, "room.html", {"room_name" : room_name})


class MessageUpdateAPIView(APIView):
    serializer_class = MessageSerializer

    def get(self, request, message_id, format = None):
        Message.objects.filter(id = message_id).update(is_it_seen = True)
        message = Message.objects.get(id = message_id)
        serializer = self.serializer_class(message, many = False)
        return Response(serializer.data)


class UsersAPIView(APIView):
    serializer_class = AppUserSerializer

    def get(self, request, *args, **kwargs):
        users = AppUser.objects.all()
        serializer = self.serializer_class(users, many= True)
        return Response(serializer.data)
    

class UserSingle(APIView):
    serializer_class = AppUserSerializer

    def get(self, request, uid, format = None):
        user = AppUser.objects.get(id = uid)
        serializer = self.serializer_class(user, many = False)
        return Response(serializer.data)
    

class UserPost(APIView):
    serializer_class = AppUserSerializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            existing_user = AppUser.objects.filter(id=id).first()
            if existing_user:
                return Response(self.serializer_class(existing_user).data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         id = serializer.validated_data.get('id')
    #         existing_user = AppUser.objects.filter(id=id).first()
    #         if existing_user:
    #             for attr, value in serializer.validated_data.items():
    #                 setattr(existing_user, attr, value)
    #             existing_user.save()
    #             return Response(self.serializer_class(existing_user).data)
    #         return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        # Retrieve the user ID from the request data
        id = request.data.get('id')
        existing_user = AppUser.objects.filter(id=id).first()

        if existing_user:
            # Initialize the serializer with the existing user instance and request data
            serializer = self.serializer_class(existing_user, data=request.data, partial=True)

            if serializer.is_valid():
                # Save the updated user data
                serializer.save()
                return Response(serializer.data)
            else:
                print("Validation Errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ChatsAPIView(APIView):
    serializer_class = ChatSerializer

    def get_object(id: str) -> object:
        try: 
            return Chat.objects.get(id = id)
        except:
            raise http.Http404


    def get(self, request, *args, **kwargs):
        chats = Chat.objects.all()
        serializer = self.serializer_class(chats, many = True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        chats = Chat.objects.all()
        serializer = self.serializer_class(chats, many = True)
        return Response(serializer.data)


class ChatById(APIView):
    serializer_class = ChatSerializer

    def get_object(self, id):
        try: 
            return Chat.objects.get(id = id)
        except:
            raise http.Http404
    
    def get(self, request, id, format = None):
        chat = self.get_object(id = id)
        serializer = self.serializer_class(chat)
        return Response(serializer.data)
    

class ChatByUser(APIView):
    serializer_class = ChatSerializer

    def get_object(self, id):
        try: 
            chats = Chat.objects.filter(Q(chat_creator__id=id) | Q(chat_user__id=id)).annotate(
            latest_message_date=Max('messages__date_sent')
            )
            # Order the queryset by the latest message date in descending order
            chats = chats.order_by('-latest_message_date')
            return chats
        except:
            raise http.Http404
    
    def get(self, request, id, format = None):
        chat = self.get_object(id = id)
        serializer = self.serializer_class(chat, many = True)
        return Response(serializer.data)
    





class MessagesByUserAndChat(APIView):
    serializer_class = MessageSerializer

    def get_object(self, chat_id):
        try: 
            return Message.objects.filter(Q(chat__id = chat_id)).order_by("date_sent")
        except:
            print("Error while getting message from query set")
            raise http.Http404
        
    def get_messages_chat(self,chat_id):
        return Chat.objects.get(id = chat_id)


    def get_message_sender(self, uid):
        return AppUser.objects.get(id = uid)
    
    def get(self, request, chat_id):
        message = self.get_object(chat_id=chat_id)
        serializer = self.serializer_class(message, many = True)
        return Response(serializer.data)
    

    def post(self, request,uid, chat_id, format = None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sender'] = self.get_message_sender(uid)
            serializer.validated_data['chat'] = self.get_messages_chat(chat_id=chat_id)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateChat(APIView):
    serializer_class = ChatSerializer

    def get_message_sender(self, uid):
        return AppUser.objects.get(id = uid)

    def get(self, request, creator_id, user_id, format = None):
        chat_obj = Chat.objects.get_or_create(chat_creator = self.get_message_sender(creator_id), chat_user = self.get_message_sender(user_id))
        serializer = self.serializer_class(chat_obj[0], many = False)
        return Response(serializer.data)