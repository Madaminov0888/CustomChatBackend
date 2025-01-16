from django.contrib import admin
from . import models


@admin.register(models.AppUser)
class AdminAppUser(admin.ModelAdmin):
    list_display = ["name", "phone_number", "date_created"]


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "chat_creator", "chat_user"]


@admin.register(models.Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ["chat", "sender", "content", "date_sent"]