import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection directly for the chatbot (no room needed)
        await self.accept()

    async def disconnect(self, close_code):
        # Optionally handle any disconnection logic here
        pass

    async def receive(self, text_data):
        try:
            # Receive message from WebSocket
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')

            if not message:
                raise ValueError("Message content is required.")

            # Replace this with your chatbot logic (e.g., use an NLP model)
            bot_response = "You said: " + message  # Placeholder chatbot logic

            # Send the chatbot response back to the WebSocket
            await self.send(text_data=json.dumps({
                'message': bot_response
            }))

        except (json.JSONDecodeError, ValueError) as e:
            # Handle errors (e.g., invalid JSON or missing message)
            await self.send(text_data=json.dumps({
                'error': f'Error: {str(e)}'
            }))
