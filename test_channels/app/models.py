from django.db import models
import uuid



class AppUser(models.Model):
    id = models.CharField(max_length = 100, unique=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField(null=True, max_length=255)
    user_name = models.CharField(null=True, unique=True, max_length=255)
    auth_id = models.CharField(null=True, blank = True,max_length=255)
    phone_number = models.CharField(null=True, blank = True,max_length=50)
    email = models.EmailField(null=True)
    is_anonymous = models.BooleanField(default=True)
    photo_url = models.CharField(null=True, blank = True, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)



class Chat(models.Model):
    id = models.CharField(max_length = 100,unique=True, primary_key=True, default=uuid.uuid4)
    chat_creator = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='created_chats')
    chat_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='chats_participated', null= True, blank=True)

    @property
    def chat_messages(self):
        return Message.objects.filter(chat=self)
    
    def __str__(self):
        return self.chat_creator.name + " | " + self.chat_user.name


class Message(models.Model):
    id = models.CharField(max_length = 100,unique=True, primary_key=True, default=uuid.uuid4)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    content = models.TextField()
    image_URL = models.CharField(null= True, default= None, blank = True, max_length=255)
    video_url = models.CharField(null= True, default= None ,blank = True, max_length=255)
    audio_url = models.CharField(null= True, default= None ,blank = True, max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_it_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.content

