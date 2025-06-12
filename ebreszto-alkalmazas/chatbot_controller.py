import ollama
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel


class ChatbotController:
    def __init__(self, chat_view):
        self.chat_view = chat_view
        self.model_name = "llama3"
        self.history = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant embedded in a mobile touchscreen alarm app. "
            "You help the user manage alarms and reminders. "
            "You can give statistics about the recent sleep session, weather, calender information which can be randomly generated."
            "You never mention being an AI model or give code."
            "If a user asks to 'set an alarm for 7 AM on weekdays', you respond as if it's done like: 'Okay, I’ve set an alarm for 7:00 AM on Monday through Friday.' "
            "If the user doesnt give proper information of the alarm (does not day hour, minute or when it is needed to be repeated) you can ask for more information. "
            " This app can store alarm in alarm groups. Make sure to ask quesstions about which alarmgoup the user wants to put the alarm in. Always list the existing alarm in this case. "
            "Keep the replies relatively short. "
            "Make sure to ask questions if something is not well said, informations are missing or something is not clear. "
            "Be polite and friendly with the user. "
        )
    }
]

    def handle_user_input(self, user_text: str):
        self.chat_view.add_user_message(user_text)
        self.history.append({"role": "user", "content": user_text})

        # Add temporary "Typing..." message
        self.stream_buffer = ""
        self.bot_widget = self.chat_view.create_bot_widget("Typing...")
        self.chat_view.chatLayout.addWidget(self.bot_widget)
        self._scroll_to_bottom()

        self.bot_label = self.bot_widget.findChild(QLabel, "roboto_text")
        self.bot_label.setWordWrap(True)

        def stream_step():
            try:
                for chunk in ollama.chat(
                    model=self.model_name,
                    messages=self.history,
                    stream=True
                ):
                    content = chunk["message"]["content"]
                    self.stream_buffer += content
                    self.bot_label.setText(self.stream_buffer)
                    QTimer.singleShot(10, lambda: None)

                # Update conversation history
                self.history.append({"role": "assistant", "content": self.stream_buffer})

            except Exception as e:
                self.bot_label.setText(f"Error: {e}")

        QTimer.singleShot(10, stream_step)

    def _scroll_to_bottom(self):
        scroll_bar = self.chat_view.scrollArea.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

