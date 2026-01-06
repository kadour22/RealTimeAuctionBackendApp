import json
from channels.generic.websocket import AsyncWebsocketConsumer

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