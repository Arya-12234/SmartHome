from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Initialize model with 4-bit quantization
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# Knowledge base
COMMAND_PATTERNS = {
    "turn on the lights": {"action": "light_control", "parameters": {"state": "on"}},
    "turn off the lights": {"action": "light_control", "parameters": {"state": "off"}}
}

HELP_ADVICE = {
    "stuck": [
        "Try saying 'How do I control lights?'",
        "Need help with devices? Ask 'Show connected devices'",
        "For setup help, type 'Setup guide'"
    ],
    "error": [
        "Please check device connections",
        "Ensure your hub is powered on",
        "Try restarting the app"
    ]
}

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning! 🌞"
    elif 12 <= hour < 17:
        return "Good afternoon! ☀️"
    else:
        return "Good evening! 🌙"

def process_command(user_message):
    user_message = user_message.lower()
    
    # Greeting detection
    if any(word in user_message for word in ["hi", "hello", "hey"]):
        return f"{get_greeting()} I'm your Smart Home Assistant. How can I help you today?"
    
    # Help detection
    if any(word in user_message for word in ["help", "stuck", "trouble"]):
        return "Here's what you can do:\n• " + "\n• ".join(HELP_ADVICE["stuck"])
    
    # Error detection
    if any(word in user_message for word in ["error", "not working", "broken"]):
        return "Try these troubleshooting steps:\n• " + "\n• ".join(HELP_ADVICE["error"])
    
    # Command processing
    if "turn on" in user_message and "lights" in user_message:
        return "Turning lights on... ✅"
    elif "turn off" in user_message and "lights" in user_message:
        return "Turning lights off... 🔴"
    
    # LLM fallback
    inputs = tokenizer(user_message, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=50)
    llm_response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return sanitize_response(llm_response)

def sanitize_response(response):
    # Security check
    if "turn on" in response.lower() and "security" in response.lower():
        return "For security reasons, I need you to confirm this action verbally first."
    
    # Remove redundant prefixes
    if "Assistant:" in response:
        response = response.split("Assistant:")[-1].strip()
    
    return response

# Initial greeting for new sessions
INITIAL_GREETING = f"{get_greeting()} I'm here to help with your smart home. You can ask me to control devices or get assistance."
