# chat/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage

logger = logging.getLogger(__name__)

# Global dictionary to track online users: channel_name -> username.
online_users = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'
        self.username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        # Add or update online users dictionary.
        online_users[self.channel_name] = self.username
        logger.info(f"{self.username} connected on channel {self.channel_name}. Active users: {list(online_users.values())}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        removed_user = online_users.pop(self.channel_name, None)
        logger.info(f"{removed_user} disconnected from channel {self.channel_name}. Active users: {list(online_users.values())}")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info(f"Received data from {self.username}: {text_data}")
        try:
            data = json.loads(text_data)
            message = data.get('message', '')
            username = data.get('username', self.username)
            logger.info(f"Broadcasting message from {username}: {message}")

            # Save message to the database.
            await self.save_message(username, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def chat_message(self, event):
        logger.info(f"Sending message on channel {self.channel_name}: {event}")
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @sync_to_async
    def save_message(self, username, message):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Optionally, handle anonymous users differently.
            return
        ChatMessage.objects.create(user=user, message=message)
