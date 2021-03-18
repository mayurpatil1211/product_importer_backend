import asyncio
import json
from datetime import datetime, timedelta
import time
import _thread

from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.db import connections, close_old_connections
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync



# class EventConsumer(WebsocketConsumer):
#     groups = ["broadcast"]
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         print(text_data)
#         self.send(text_data="death")
#         if text_data == "echo":
#             self.send(text_data="death")



# class ObdConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         imei = self.scope['url_route']['kwargs']['imei']
#         self.imei = imei
#         await self.channel_layer.group_add(
#                 imei,
#                 self.channel_name
        
#             )
#         # await self.accept()
#         await self.send({
#             "type": "websocket.accept"
#         })



#     async def websocket_receive(self, event):
#         close_old_connections()
#         imei = self.scope['url_route']['kwargs']['imei']
#         details = event.get('text', None)
#         details = json.loads(details)
#         self.chat_room = 'event'

#         await self.send({
#             "type":"websocket.send",
#             "text":'event[]'
#             })
    

#     async def websocket_disconnect(self, event):
#         print("Disconnected", event)