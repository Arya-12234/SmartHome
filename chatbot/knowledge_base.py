import re
from datetime import datetime

# Core Knowledge Base
SMART_HOME_KNOWLEDGE = {
    # General Information
    "about": "Our smart home system lets you control and automate your entire home. You can manage lights, temperature, security, entertainment, and more.",
    
    # Devices
    "lights": {
        "description": "Smart lighting throughout your home that can be controlled individually or in groups.",
        "commands": ["turn on", "turn off", "dim", "brighten", "set color"],
        "action_map": {
            "turn on": "light_control_on",
            "turn off": "light_control_off",
            "dim": "light_dim",
            "brighten": "light_brighten",
            "set color": "light_color"
        },
        "faq": [
            {
                "question": "how control lights",
                "keywords": ["control", "manage", "use"],
                "answer": "You can control lights through the app, voice commands, or automations. Try 'Turn on kitchen lights'."
            },
            {
                "question": "schedule lights",
                "keywords": ["schedule", "timer", "routine"],
                "answer": "Create light schedules in the Automation tab. Lights can follow sunrise/sunset times."
            }
        ]
    },
    
    "thermostat": {
        "description": "Smart climate control system that learns your preferences.",
        "commands": ["set temperature", "heat", "cool", "schedule"],
        "action_map": {
            "set temperature": "thermostat_set",
            "heat": "thermostat_heat",
            "cool": "thermostat_cool",
            "schedule": "thermostat_schedule"
        },
        "faq": [
            {
                "question": "change temperature",
                "keywords": ["adjust", "set", "change"],
                "answer": "Say 'Set temperature to 72°F' or use the app's temperature slider."
            },
            {
                "question": "compatibility",
                "keywords": ["works with", "compatible", "system"],
                "answer": "Works with forced air, radiant heat, and heat pumps. Supports multi-zone control."
            }
        ]
    },
    
    "security": {
        "description": "Comprehensive security system with door/window sensors, motion detectors, and cameras.",
        "commands": ["arm", "disarm", "view cameras", "lock doors"],
        "action_map": {
            "arm": "security_arm",
            "disarm": "security_disarm",
            "view cameras": "camera_view",
            "lock doors": "doors_lock"
        },
        "faq": [
            {
                "question": "arm system",
                "keywords": ["activate", "enable", "turn on"],
                "answer": "Say 'Arm security system' or use the app's security panel. Automatically arms at bedtime."
            },
            {
                "question": "camera access",
                "keywords": ["view", "camera", "feed"],
                "answer": "View live feeds in the app's Security section. 30-day cloud storage included."
            }
        ]
    },
    
    # Features
    "automation": {
        "description": "Create routines and automations to control multiple devices at once.",
        "action_map": {
            "create routine": "automation_create",
            "edit automation": "automation_edit"
        },
        "examples": [
            "Morning: lights on, thermostat to 70°F, play news",
            "Away: lights off, thermostat eco-mode, security on",
            "Movie night: dim lights, lower blinds, start entertainment"
        ]
    },
    
    "voice_control": {
        "description": "Control your smart home with voice commands.",
        "compatibility": ["Alexa", "Google Assistant", "Siri"],
        "action_map": {
            "add voice": "voice_add",
            "remove voice": "voice_remove"
        },
        "example_commands": [
            "Turn on kitchen lights",
            "Set bedroom temperature to 68°F",
            "Lock front door"
        ]
    },
    
    # Support
    "troubleshooting": {
        "connection": {
            "description": "Device connection issues",
            "steps": [
                "1. Power cycle the device",
                "2. Check Wi-Fi signal strength",
                "3. Verify app is updated"
            ]
        },
        "app": {
            "description": "Mobile app problems",
            "steps": [
                "1. Force quit and restart app",
                "2. Clear app cache",
                "3. Reinstall latest version"
            ]
        }
    },
    
    "contact": {
        "email": "support@smarthome.com",
        "phone": "555-SMART-HOME",
        "hours": "24/7 emergency support available"
    }
}

# Enhanced Processing Functions
class SmartHomeProcessor:
    def __init__(self):
        self.command_history = []
        self.last_action = None

    def get_greeting(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning! 🌞 How can I assist with your smart home?"
        elif 12 <= hour < 17:
            return "Good afternoon! ☀️ What would you like to control?"
        else:
            return "Good evening! 🌙 Ready to automate your home?"

    def detect_emergency(self, message):
        emergency_keywords = ["break-in", "fire", "flood", "urgent"]
        return any(word in message.lower() for word in emergency_keywords)

    def process_command(self, user_message):
        user_message = user_message.lower()
        self.command_history.append(user_message)

        # Emergency detection
        if self.detect_emergency(user_message):
            return "🚨 Emergency detected! Contacting security services and turning on all lights."

        # Greeting response
        if re.search(r'\b(hi|hello|hey)\b', user_message):
            return self.get_greeting()

        # Knowledge base search
        response = self._search_knowledge_base(user_message)
        if response:
            return response

        # Command processing
        device_actions = self._detect_device_actions(user_message)
        if device_actions:
            return self._execute_action(device_actions)

        # Fallback to general help
        return "I can help with:\n• Device control\n• Automations\n• Troubleshooting\nTry 'How do I set up a lighting schedule?'"

    def _search_knowledge_base(self, message):
        # FAQ matching
        for category in ["lights", "thermostat", "security"]:
            if category in message:
                for qa in SMART_HOME_KNOWLEDGE[category]["faq"]:
                    if any(keyword in message for keyword in qa["keywords"]):
                        return qa["answer"]
        
        # Troubleshooting
        if "troubleshoot" in message or "problem" in message:
            issue = "connection" if "connect" in message else "app"
            return "Try these steps:\n" + "\n".join(SMART_HOME_KNOWLEDGE["troubleshooting"][issue]["steps"])
        
        # Contact information
        if "contact" in message:
            contact = SMART_HOME_KNOWLEDGE["contact"]
            return f"Contact support:\n📧 {contact['email']}\n📞 {contact['phone']}\n⏰ {contact['hours']}"

        return None

    def _detect_device_actions(self, message):
        for device, data in SMART_HOME_KNOWLEDGE.items():
            if isinstance(data, dict) and "action_map" in data:
                for command, action in data["action_map"].items():
                    if command in message:
                        return {
                            "device": device,
                            "action": action,
                            "parameters": self._extract_parameters(message)
                        }
        return None

    def _extract_parameters(self, message):
        params = {}
        if "temperature" in message:
            temp = re.search(r'(\d+)\s*degrees?', message)
            if temp:
                params["temperature"] = int(temp.group(1))
        if "color" in message:
            color = re.search(r'(red|blue|green|warm white)', message)
            if color:
                params["color"] = color.group(1)
        return params

    def _execute_action(self, action_data):
        device = action_data["device"]
        action = action_data["action"]
        params = action_data["parameters"]
        
        # Format response based on action
        if action.startswith("light"):
            color = params.get("color", "")
            if color:
                return f"Setting {device} to {color} ✅"
            return f"Adjusting {device} {action.split('_')[-1]} ✅"
        
        if action.startswith("thermostat"):
            temp = params.get("temperature", "")
            if temp:
                return f"Setting thermostat to {temp}°F ✅"
            return f"Adjusting climate control ✅"
        
        return f"Executing {action.replace('_', ' ')} on {device} ✅"

# Integration Example for views.py
def get_chatbot_response(message):
    processor = SmartHomeProcessor()
    response = processor.process_command(message)
    
    # Add security verification for critical actions
    if any(cmd in message.lower() for cmd in ["arm system", "lock all"]):
        response += "\n🔒 Please confirm this security action in the app."
    
    return response
