from .models import Room, RoomMessages
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
import json
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    async def disconnect(self):
        await self.channel_layer.group_discard(self.channel_layer, self.room_group_name)


    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = data['messagebody']
        room = data['roomid']
        uname = data['username']


        await self.save_message_to_db(room= room, user=uname, message= msg)


        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message_action', # include key : 'type'  when creating another async functon to handle sending response back to JS. Value is new async function name.
                'message': msg,
                'username': uname,
                'roomid': room
            })
        
        # await self.chat_message_action(data)


    async def chat_message_action(self, event): 
        message = event['message'] # that dict value is the key from self.room_group_name above.
        room = event['roomid'] # this dict value is the key from self.room_group_name
        username = event['username'] # same with the two above.

        await self.send(text_data= json.dumps({
                'messagebody': message,
                'username': username,
                'roomid': room
            }
        )) 
        

    @sync_to_async
    def save_message_to_db(self, user, room, message):
        user = User.objects.filter(username = user).first()
        room = Room.objects.get(slug = room)

        room_message = RoomMessages(user = user, room = room, message = message)
        room_message.save()