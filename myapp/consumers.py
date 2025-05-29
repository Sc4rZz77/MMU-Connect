import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import Message
        from django.contrib.auth.models import User
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']
        users = sorted([self.user.username, self.other_username])
        self.room_group_name = f"chat_{users[0]}_{users[1]}"
        print("User in connect:", self.user)
        print("Room group name:", self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("Disconnected", close_code)

    async def receive(self, text_data):
        from .models import Message
        from django.contrib.auth.models import User
        data = json.loads(text_data)
        if data.get('type') == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing',
                    'user': data.get('user', self.user.username)
                }
            )
        elif 'message' in data:
            message = data['message']
            # Fetch recipient asynchronously
            recipient = await database_sync_to_async(User.objects.get)(username=self.other_username)
            # Save to DB
            await database_sync_to_async(Message.objects.create)(
                sender=self.user,
                recipient=recipient,
                content=message,
                room=self.room_group_name
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f"{self.user.username}: {message}"
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    async def typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user']
        }))
