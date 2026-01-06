import json
from channels.generic.websocket import AsyncWebsocketConsumer

class auction_consumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.group_name = f"auction_{self.auction_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"WebSocket connected for auction {self.auction_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"WebSocket disconnected for auction {self.auction_id}")
    
    async def place_new_bid(self, event):
        # Send message to WebSocket as JSON string
        message = {
            "type": "place_new_bid",
            "amount": event["amount"],
            "auction_id": event["auction_id"],
            "user": event["user"]
        }
        await self.send(text_data=json.dumps(message))
