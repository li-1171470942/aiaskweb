# myapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # 接受 WebSocket 连接

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # 这里可以处理客户端发送来的信息
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
