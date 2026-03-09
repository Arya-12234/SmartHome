# chatbot/admin.py
from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'bot_response', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user_message', 'bot_response')
    date_hierarchy = 'timestamp'

# chatbot/management/commands/export_chat_data.py
from django.core.management.base import BaseCommand
import json
from chatbot.models import ChatMessage

class Command(BaseCommand):
    help = 'Export chat messages for training data'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='chat_training_data.jsonl', 
                            help='Output file path')

    def handle(self, *args, **kwargs):
        output_file = kwargs['output']
        
        # Get all chat messages
        messages = ChatMessage.objects.all().order_by('timestamp')
        
        # Convert to training data format
        training_data = []
        for msg in messages:
            training_data.append({
                "instruction": msg.user_message,
                "response": msg.bot_response
            })
        
        # Save to jsonl file
        with open(output_file, 'w') as f:
            for item in training_data:
                f.write(json.dumps(item) + '\n')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully exported {len(training_data)} messages to {output_file}'))