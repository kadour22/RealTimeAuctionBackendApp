import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

class notifications_consumer(AsyncWebsocketConsumer) :
    
    async def connect(self):
        self.group_name = "notifications"
        await self.channel_layer.group_add(
            self.group_name , self.channel_name
            )
        await self.accept()
        print("connected..")
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name , self.channel_name
        )
        print("disconnected..")
    
    async def new_notification(self,event) :
        await self.send(text_data=json.dumps({
            "type":"new_notification",
            "message"    : event["message"],
            "is_read"    : event["is_read"],
            "created_at" : event["created_at"],
        }))

class mark_as_read_consumer(AsyncWebsocketConsumer) :
   
    async def connect(self):
        self.notification_id = self.scope['url_route']['kwargs']['notification_id']
        await self.channel_layer.group_add(self.notification_id, self.channel_name)
        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.notification_id, self.channel_name)
    
    async def receive(self, text_data ):
        if text_data["type"] == "mark_as_read" :
            pass
    
    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        Notification.objects.filter(id=notification_id).update(is_read=True)
    
    async def notification_read(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification_read",
            "notification_id": event["notification_id"]
        }))