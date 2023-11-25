# Example Django consumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
import pytz

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

         # current date and time
        date_time = datetime.now(tz=pytz.timezone('Asia/Tokyo'))

        # format specification
        format = '%Y-%m-%d %H:%M:%S'

            
        # applying strftime() to format the datetime
        string = date_time.strftime(format)
        await self.send(text_data=json.dumps({
            'message': string
        }))
