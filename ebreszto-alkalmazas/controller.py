from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QWidget,
    QPushButton
)

from ui_files.icons import*

class Controller:
    def __init__(self, ui_file_path, model):
        self.ui_file_path = ui_file_path
        self.model = model
        self.ui = None

    
    def load_ui(self):
        ui_file = QFile(self.ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Cannot open {self.ui_file_path}: {ui_file.errorString()}")

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("Failed to load the UI file.")

    def show_view(self):
        if self.ui:
            self.ui.show()

    # Find a widget by name and type
    def find_widget(self, widget_type, widget_name: str):
        return self.ui.findChild(widget_type, widget_name)

    def setup_views(self):
        from views.home_view import HomeView
        from views.alarms_view import AlarmsView
        from views.chat_view import ChatView
        from views.information_view import InformationView
        from views.reminders_view import RemindersView
        from views.statistics_view import StatisticsView

        self.homeView_widget = self.find_widget(QWidget, "homePage")
        self.alarmsView_widget = self.find_widget(QWidget, "alarmPage")
        self.chatView_widget = self.find_widget(QWidget, "chatPage")
        self.informationView_widget = self.find_widget(QWidget, "informationPage")
        self.remindersView_widget = self.find_widget(QWidget, "remindersPage")
        self.statisticsView_widget = self.find_widget(QWidget, "statisticsPage")


        # Create the views
        self.home_view = HomeView(self.homeView_widget)
        self.alarms_view = AlarmsView(self.alarmsView_widget)
        self.chat_view = ChatView(self.chatView_widget)
        self.information_view = InformationView(self.informationView_widget)
        self.reminders_view = RemindersView(self.remindersView_widget)
        self.statistics_view = StatisticsView(self.statisticsView_widget)

        # Add navigation buttons
        self.setup_navigation_buttons()

    def setup_navigation_buttons(self):
        # Find navigation buttons
        self.ui.alarm_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.alarmsView_widget))
        self.ui.information_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.informationView_widget))
        self.ui.microphone_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.chatView_widget))
        self.ui.statistics_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.statisticsView_widget))
        self.ui.reminders_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.remindersView_widget))


