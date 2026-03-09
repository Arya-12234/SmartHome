from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import requests
from .models import ChatMessage
from .knowledge_base import SmartHomeProcessor

# Initialize processor globally
processor = SmartHomeProcessor()

@csrf_exempt
@require_POST
def chat_handler(request):
    """Unified chat handler with fallback to LLama"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        # Process through smart home processor first
        response = processor.process_command(user_message)
        
        # Fallback to LLama if no meaningful response
        if needs_llama_fallback(response):
            ll_response = get_llama_response(user_message)
            response = f"{response}\n\n[AI Suggestion] {ll_response}" if response else ll_response

        # Save conversation history
        if request.user.is_authenticated:
            ChatMessage.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=response
            )

        return JsonResponse({'response': response})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def needs_llama_fallback(response):
    """Determine if we need LLama fallback"""
    if not response:
        return True
    return any(phrase in response.lower() for phrase in [
        "not sure", 
        "need more information",
        "can you clarify"
    ])

def get_llama_response(prompt):
    """Enhanced LLama integration with error handling"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "smarthome-llama",
                "prompt": f"User is asking about their smart home: {prompt}",
                "options": {"temperature": 0.3}
            },
            timeout=5  # 5-second timeout
        )
        response.raise_for_status()
        return response.json().get('response', 
            "I need more information to assist with that.")
            
    except requests.Timeout:
        return "Our AI assistant is taking longer than usual to respond. Please try again."
    except Exception as e:
        print(f"LLama Error: {str(e)}")
        return "Our AI assistant is currently unavailable. Please try again later."

def chatbot_interface(request):
    """Render chat interface with initial context"""
    context = {
        'initial_greeting': processor.get_greeting(),
        'recent_devices': ["Living Room Lights", "Thermostat", "Front Door Lock"]
    }
    return render(request, 'chatbot/chat_interface.html', context)
