# chatbot/knowledge_base.py

SMART_HOME_KNOWLEDGE = {
    # General Information
    "about": "Our smart home system lets you control and automate your entire home. You can manage lights, temperature, security, entertainment, and more.",
    
    # Devices
    "lights": {
        "description": "Smart lighting throughout your home that can be controlled individually or in groups.",
        "commands": ["turn on", "turn off", "dim", "brighten", "set color"],
        "faq": [
            {
                "question": "How do I control the lights?",
                "answer": "You can control lights through the app, voice commands, or set up automations."
            },
            {
                "question": "Can I schedule my lights?",
                "answer": "Yes, you can create schedules for any light to turn on/off at specific times."
            }
        ]
    },
    
    "thermostat": {
        "description": "Smart climate control system that learns your preferences.",
        "commands": ["set temperature", "turn on heat", "turn on cooling", "set schedule"],
        "faq": [
            {
                "question": "How do I change the temperature?",
                "answer": "You can adjust the temperature in the app, through voice commands, or on the thermostat itself."
            },
            {
                "question": "Does it work with my heating system?",
                "answer": "Our thermostat is compatible with most heating and cooling systems including forced air, radiant, and heat pumps."
            }
        ]
    },
    
    "security": {
        "description": "Comprehensive security system with door/window sensors, motion detectors, and cameras.",
        "commands": ["arm system", "disarm system", "view cameras"],
        "faq": [
            {
                "question": "How do I arm the security system?",
                "answer": "You can arm the system through the app, control panel, or set it to arm automatically on a schedule."
            },
            {
                "question": "Can I view my cameras remotely?",
                "answer": "Yes, you can view live feeds from all your security cameras through our mobile app or web portal."
            }
        ]
    },
    
    # Features
    "automation": {
        "description": "Create routines and automations to control multiple devices at once.",
        "examples": [
            "Morning routine: gradually turn on lights, adjust thermostat, play news",
            "Leaving home: turn off all lights, lower thermostat, arm security",
            "Movie night: dim lights, lower blinds, turn on TV and sound system"
        ]
    },
    
    "voice_control": {
        "description": "Control your smart home with voice commands.",
        "compatibility": ["Amazon Alexa", "Google Assistant", "Apple HomeKit"],
        "example_commands": [
            "Turn on the living room lights",
            "Set the temperature to 72 degrees",
            "Lock all doors"
        ]
    },
    
    # Support
    "troubleshooting": {
        "connection_issues": "If a device is offline, try power cycling it by unplugging for 30 seconds then plugging it back in.",
        "app_problems": "Make sure your app is updated to the latest version. Try logging out and logging back in.",
        "device_reset": "To reset a device, hold the reset button for 10 seconds until the LED flashes."
    },
    
    "contact": {
        "support_email": "support@yoursmarthouse.com",
        "support_phone": "555-123-4567",
        "hours": "Monday-Friday, 9am-6pm"
    }
}

# Add to views.py:
from .knowledge_base import SMART_HOME_KNOWLEDGE

def get_chatbot_response(message):
    """Improved chatbot response system using the knowledge base"""
    message = message.lower()
    
    # Greetings
    if re.search(r'\b(hi|hello|hey|greetings)\b', message):
        return "Hello! I'm your Smart Home Assistant. How can I help you today?"
    
    # General information request
    if re.search(r'\b(what can you do|help me|how does this work)\b', message):
        return "I can help with your smart home system! You can ask me about lights, thermostat, security, automation, troubleshooting, and more."
    
    # Handle specific topic requests
    topics = {
        "lights": ["light", "lighting", "bulb", "lamp", "switch"],
        "thermostat": ["thermostat", "temperature", "heating", "cooling", "climate"],
        "security": ["security", "camera", "sensor", "alarm", "lock", "door"],
        "automation": ["automation", "routine", "scene", "schedule"],
        "voice_control": ["voice", "alexa", "google", "siri", "command"],
        "troubleshooting": ["problem", "issue", "not working", "error", "troubleshoot", "help"],
        "contact": ["contact", "support", "phone", "email", "help", "number"]
    }
    
    # Check if the message contains any topic keywords
    detected_topics = []
    for topic, keywords in topics.items():
        for keyword in keywords:
            if keyword in message:
                detected_topics.append(topic)
                break
    
    # If we found topics, respond with relevant information
    if detected_topics:
        topic = detected_topics[0]  # Take the first detected topic
        
        # Handle FAQ questions if available for this topic
        if topic in ["lights", "thermostat", "security"] and "faq" in SMART_HOME_KNOWLEDGE[topic]:
            for qa in SMART_HOME_KNOWLEDGE[topic]["faq"]:
                if any(keyword in message for keyword in qa["question"].lower().split()):
                    return qa["answer"]
        
        # General topic information
        if isinstance(SMART_HOME_KNOWLEDGE[topic], str):
            return SMART_HOME_KNOWLEDGE[topic]
        elif "description" in SMART_HOME_KNOWLEDGE[topic]:
            return SMART_HOME_KNOWLEDGE[topic]["description"]
        
        # If we reach here, give a general response about the topic
        return f"I have information about {topic}. Could you ask a more specific question?"
    
    # Handle specific device commands
    if re.search(r'turn (on|off)', message):
        device_match = re.search(r'turn (on|off) (?:the )?(.+)', message)
        if device_match:
            action, device = device_match.groups()
            return f"I'll {action} the {device} for you."
    
    if "temperature" in message and re.search(r'set|change|make', message):
        temp_match = re.search(r'(\d+)(?:\s*degrees)?', message)
        if temp_match:
            temp = temp_match.group(1)
            return f"I've set the temperature to {temp} degrees."
    
    # Default response
    return "I'm not sure how to help with that specific question. You can ask me about your smart home devices, automation features, or troubleshooting."