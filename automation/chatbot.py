# automation/chatbot.py

def get_bot_response(user_message):
    # Simple chatbot logic for now
    if "hello" in user_message.lower():
        return "Hi there! How can I help you today?"
    elif "bye" in user_message.lower():
        return "Goodbye! Have a nice day."
    return "I'm sorry, I don't understand that."
