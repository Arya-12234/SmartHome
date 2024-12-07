from .models import ChatMessage

def save_chat_message(user_message, bot_response):
    chat = ChatMessage(user_message=user_message, bot_response=bot_response)
    chat.save()

def get_chat_history():
    return ChatMessage.objects.all()