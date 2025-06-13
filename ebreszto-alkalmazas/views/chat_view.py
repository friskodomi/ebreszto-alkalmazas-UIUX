from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QScrollArea,
    QLabel, QSizePolicy, QGroupBox, QPlainTextEdit
)
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from chatbot_controller import ChatbotController

class ChatView:
    def __init__(self, chatView_widget):
        self.chatPage = chatView_widget

        # Getting the widgets from the ui file
        self.userinput_text: QPlainTextEdit = self.chatPage.findChild(QPlainTextEdit, "userinputTextEdit")
        self.send_button: QPushButton = self.chatPage.findChild(QPushButton, "sendButton")
        self.scrollArea: QScrollArea = self.chatPage.findChild(QScrollArea, "chatbotScrollArea")

        # Set up for the scroll area
        # Creating the content widget
        self.scrollAreaContent = QWidget()
        self.scrollArea.setWidget(self.scrollAreaContent)
        self.scrollArea.setWidgetResizable(True)

        # Group box that will hold created widgets of the messages
        self.chat_groupbox = QGroupBox("")
        self.chat_groupbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        # Vertical layout for the groupbox to hold the widgets
        self.chatLayout = QVBoxLayout()
        self.chatLayout.setSpacing(0)
        self.chatLayout.setContentsMargins(0, 0, 10, 10)
        self.chat_groupbox.setLayout(self.chatLayout)

        # Vertical layout to hold the groupbox
        self.containerLayout = QVBoxLayout()
        self.containerLayout.addWidget(self.chat_groupbox)
        self.containerLayout.addStretch()  # Keep alarms top-aligned
        self.scrollAreaContent.setLayout(self.containerLayout)

        # Set size policy to allow vertical expansion
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.chat_groupbox.setSizePolicy(size_policy)
        
        # Connect controller
        self.chat_controller = ChatbotController(self)

        # Connect signals
        self.send_button.clicked.connect(self.send_chat_message)

    # Handles sending a message when the user clicks the send button
    def send_chat_message(self):
        if self.userinput_text is None:
            return

        text = self.userinput_text.toPlainText()
        if text.strip():
            self.userinput_text.clear()
            self.chat_controller.handle_user_input(text)

    # Adds the created user message widget to the chat layout
    def add_user_message(self, message: str):
        widget = self.create_user_widget(message)
        self.chatLayout.addWidget(widget)
        self._scroll_to_bottom()

    # Adds the created bot message widget to the chat layout
    def add_bot_message(self, message: str):
        widget = self.create_bot_widget(message)
        self.chatLayout.addWidget(widget)
        self._scroll_to_bottom()

    # Creates the widget from the user messages
    def create_user_widget(self, message: str) -> QWidget:
        ui_file = QFile("ui_files/user_input.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        user_widget = loader.load(ui_file)
        ui_file.close()

        if user_widget is None:
            return QWidget()

        label = user_widget.findChild(QLabel, "user_text")
        label.setWordWrap(True)

        if label:
            label.setText(message)

        return user_widget

    # Creates the widget from the bot messages
    def create_bot_widget(self, message: str) -> QWidget:
        ui_file = QFile("ui_files/roboto_chat.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        bot_widget = loader.load(ui_file)
        ui_file.close()

        if bot_widget is None:
            return QWidget()

        label = bot_widget.findChild(QLabel, "roboto_text")
        label.setWordWrap(True)

        if label:
            label.setText(message)

        return bot_widget

    # Ensuring that the newest messages will be displayed, scrolls to the bottom (almost)
    def _scroll_to_bottom(self):
        scroll_bar = self.scrollArea.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())