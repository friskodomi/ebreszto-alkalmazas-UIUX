import re

class ChatbotController:
    def __init__(self, chat_view):
        self.chat_view = chat_view
        self.waiting_for_time = False
        self.waiting_for_days = False
        self.temp_time = None

    def handle_user_input(self, user_text: str):
        # The view already adds the user message
        response = self.generate_response(user_text)
        self.chat_view.add_bot_message(response)

    def generate_response(self, user_text: str):
        user_text = user_text.lower()

        if self.waiting_for_time:
            self.temp_time = user_text
            self.waiting_for_time = False
            self.waiting_for_days = True
            return "Great! And which days should the alarm repeat on?"

        if self.waiting_for_days:
            time = self.temp_time
            self.waiting_for_days = False
            self.temp_time = None
            return f"Okay! I’ll (pretend to) set an alarm for {time} on {user_text}."

        if "set alarm" in user_text:
            self.waiting_for_time = True
            return "What time should the alarm be set to?"

        if "hello" in user_text or "hi" in user_text:
            return "Hey there! I can help you set pretend alarms"

        return "I'm just a pretend assistant, but I can chat and fake alarms!"
