from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QWidget,
    QPushButton
)

import ui_files.rc_icons
from model import Model

class Controller:
    def __init__(self, ui_file_path, model):
        self.ui_file_path = ui_file_path
        self.model = Model()
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

    def setup_views(self):
        from views.home_view import HomeView
        from views.alarms_view import AlarmsView
        from views.statistics_view import StatisticsView
        from views.reminders_view import RemindersView
        from views.chat_view import ChatView

        self.homeView_widget = self.ui.findChild(QWidget, "homePage")
        self.alarmsView_widget = self.ui.findChild(QWidget, "alarmPage")
        self.statisticsView_widget = self.ui.findChild(QWidget, "statisticsPage")
        self.remindersView_widget = self.ui.findChild(QWidget, "remindersPage")
        self.chatView_widget = self.ui.findChild(QWidget, "chatPage")

        # Create the views
        self.homePage = HomeView(self.homeView_widget)
        self.alarmPage = AlarmsView(self.alarmsView_widget)
        self.statisticsPage = StatisticsView(self.statisticsView_widget)
        self.remindersPage = RemindersView(self.remindersView_widget)
        self.chatPage = ChatView(self.chatView_widget)

        # Add navigation buttons
        self.setup_navigation_buttons()

        self.statisticsPage.connect_controller(self)
        self.alarmPage.connect_controller(self)
        self.on_range_selected("Week")
        self.statisticsPage.week_button.setChecked(True)

    def setup_navigation_buttons(self):
        # Find navigation buttons
        self.ui.homeButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                           (self.homeView_widget))
        self.ui.alarmButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                            (self.alarmsView_widget))
        self.ui.statisticsButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                                 (self.statisticsView_widget))
        self.ui.remindersButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                                 (self.remindersView_widget))
        self.ui.microphoneButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                                 (self.chatView_widget))

        # Forward buttons on the mainscreen
        self.ui.f_alarmButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                                 (self.alarmsView_widget))
        self.ui.f_statisticsButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                                 (self.statisticsView_widget))
        self.ui.f_reminderButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                                 (self.remindersView_widget))
        self.ui.f_chatButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget
                                                 (self.chatView_widget))

    def on_range_selected(self, period: str):
            # Get data from model
            sleep_data, water_data = self.model.get_statistics(period)

            # Compute averages
            avg_sleep = self.model.compute_average(sleep_data)
            avg_water = self.model.compute_average(water_data)

            # Update view with new data
            self.statisticsPage.update_chart(sleep_data, water_data, avg_sleep, avg_water)

    def show_add_alarm_popup(self):
        from views.alarm_popup import AlarmPopup

        popup = AlarmPopup("ui_files/popup.ui")
        popup.exec()