# obj = ChatMessage.objects.create(content=message_extract)
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import *
from rest_framework_simplejwt.backends import TokenBackend
from accounts.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    def save_message(self, message):
        print('save_message_ran')
        print(message['message'])

    def get_user(self, token):
        valid_data = TokenBackend(
            algorithm='HS256').decode(token, verify=False)
        user = valid_data['user_id']
        self.my_id = user
        profile = Profile.objects.get(user=user)
        return profile

    def set_name(self, profile):
        return profile.user.name

    def check_user_and_room(self, room_name, my_id, other_user_id):
        if not ChatRoom.objects.filter(room_name=room_name).exists():
            ChatRoom.objects.create(
                user_id_1=my_id, user_id_2=other_user_id, room_name=room_name)
        room = ChatRoom.objects.get(room_name=room_name)
        if my_id != room.user_id_1 and other_user_id != room.user_id_2:
            print('Relevant users dont exists------------------------')

    def add_messages_to_room(self, room_name, message, name, my_id, other_id, profile):
        room = ChatRoom.objects.get(room_name=room_name)
        msg_obj = ChatMessage.objects.create(
            profile=profile, content=message, name=name)
        room.messages.add(msg_obj)

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        temp_array = self.room_name.split('_')
        print('prininging temp array-----------------------------------', temp_array)
        self.my_id = temp_array[1]
        other_user_id = temp_array[2]
        if(self.my_id > other_user_id):
            self.small_id = other_user_id
            self.big_id = self.my_id
            print(self.small_id, 'small')
            print(self.big_id, 'big')
        else:
            self.small_id = self.my_id
            self.big_id = other_user_id
            print(self.small_id, 'small')
            print(self.big_id, 'big')
        self.room_name = str(self.small_id)+'_'+str(self.big_id)
        self.room_group_name = 'chat_%s' % self.room_name
        await database_sync_to_async(self.check_user_and_room)(self.room_group_name, self.my_id, other_user_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # self.commands[text_data_json['save_message']](self, text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        temp_array = self.room_group_name.split('_')
        one = temp_array[1]
        two = temp_array[2]

        profile = await database_sync_to_async(self.get_user)(text_data_json['token'])
        name = await database_sync_to_async(self.set_name)(profile)
        # obj = ChatMessage(
        #     content=message, profile=profile, name=name)
        # message_object = await database_sync_to_async(obj.save)()
        if(one == self.my_id):
            self.other_user_id = two
        else:
            self.other_user_id = one
        await database_sync_to_async(self.add_messages_to_room)(self.room_group_name, message, name, self.my_id, self.other_user_id, profile)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
