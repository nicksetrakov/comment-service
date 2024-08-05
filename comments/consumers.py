import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.comment_id = self.scope["url_route"]["kwargs"].get("comment_id")
        if self.comment_id:
            self.group_name = f"comment_{self.comment_id}"

            # Join the comment group
            await self.channel_layer.group_add(
                self.group_name, self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave the comment group
        if self.comment_id:
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        comment_id = text_data_json.get("comment_id")

        if message and comment_id:
            # Send the message to the comment group
            await self.channel_layer.group_send(
                f"comment_{comment_id}",
                {
                    "type": "comment_message",
                    "message": message,
                    "comment_id": comment_id,
                },
            )

    async def comment_message(self, event):
        message = event["message"]

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
