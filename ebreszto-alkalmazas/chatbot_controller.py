from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QObject, QThread, Signal

import ollama

class ChatbotController:
    def __init__(self, chat_view):
        self.chat_view = chat_view

        self.model_name = "llama3.1"

        # Initial system prompt to define behaviour and personality of the assistant
        self.history = [
        {
        "role": "assistant",
        "content": (
            "You are a helpful assistant embedded in a mobile touchscreen alarm app. "
            "You help the user manage alarms and reminders. "
            "You can give statistics about the recent sleep session, weather, calender information which can be randomly generated."
            "You never mention being an AI model or give code."
            "If a user asks to 'set an alarm for 7 AM on weekdays', you respond as if it's done like: 'Okay, I’ve set an alarm for 7:00 AM on Monday through Friday.' "
            "If the user doesnt give proper information of the alarm (does not day hour, minute or when it is needed to be repeated) you can ask for more information. "
            "This app can store alarm in alarm groups. Make sure to ask quesstions about which alarmgoup the user wants to put the alarm in. Always list the existing alarm in this case. "
            "Keep the replies relatively short. "
            "Make sure to ask questions if something is not well said, informations are missing or something is not clear. "
            "Only ask one question at a time and make them simple. "
            "Be polite and friendly with the user. "
            )
        }
    ]

    # Handle user input of promt
    def handle_user_input(self, user_text: str):
        # Display the user's message in the chat
        self.chat_view.add_user_message(user_text)
        # Adding the user tex to the history
        self.history.append({"role": "user", "content": user_text})
        
        # Disable UI and show progress
        self.chat_view.send_button.setDisabled(True)
        self.chat_view.send_button.setText("Thinking...")
        self.chat_view.userinput_text.setDisabled(True)

        # Create the bot "chatbox" widget
        # Set the text to Typing... as placeholder
        self.stream_buffer = ""
        self.bot_widget = self.chat_view.create_bot_widget("Typing...")
        self.chat_view.chatLayout.addWidget(self.bot_widget)
        self.chat_view._scroll_to_bottom()

        self.bot_label = self.bot_widget.findChild(QLabel, "roboto_text")
        self.bot_label.setWordWrap(True)

        # Create a worker for the call
        # Make sure that it runs in a separate thread
        self.thread = QThread()
        self.worker = self.ChatWorker(self.model_name, self.history)
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.worker.update.connect(self._update_response)
        self.worker.finished.connect(self._finish_response)
        self.worker.error.connect(self._handle_error)
        self.thread.started.connect(self.worker.run)

        # Cleanup
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the worker thread
        self.thread.start()

    # Update the bot chatbox
    def _update_response(self, partial_text: str):
        if self.bot_label:
            self.bot_label.setText(partial_text)

    # Called when the response is generated, updated the histroy, enables the button and
    # text label so the user can send the new input
    def _finish_response(self, full_text: str):
        self.history.append({"role": "assistant", "content": full_text})
        self.chat_view.send_button.setEnabled(True)
        self.chat_view.send_button.setText("Send")
        self.chat_view.userinput_text.setEnabled(True)

    # Error handling
    # Displays error both at the chatbox of the robot and prints the error message
    def _handle_error(self, message: str):
        if self.bot_label:
            self.bot_label.setText("Roboto has encountered an error, please try again.")
            print(f"ERROR: while generating chat response: {message}")
        
        self.chat_view.send_button.setEnabled(True)
        self.chat_view.send_button.setText("Send")
        self.chat_view.userinput_text.setEnabled(True)

    # "Inner worker" class
    # Streams chat responses
    class ChatWorker(QObject):
        update = Signal(str)
        finished = Signal(str)
        error = Signal(str)

        def __init__(self, model, history):
            super().__init__()
            self.model = model
            self.history = history

        def run(self):
            try:
                buffer = ""
                for chunk in ollama.chat(
                    model=self.model,
                    messages=self.history,
                    stream=True
                ):
                    # Emits partial response so it looks like its typing
                    buffer += chunk["message"]["content"]
                    self.update.emit(buffer)
                # Final reponse
                self.finished.emit(buffer)
            except Exception as e:
                self.error.emit(str(e))
