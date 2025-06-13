from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget

from model import Model

class Controller:
    def __init__(self, ui_file_path, model):
        # Initialize controller with the path to the .ui file and a model instance
        self.ui_file_path = ui_file_path
        self.model = Model()
        self.ui = None

    def load_ui(self):
        # Load the .ui file using QUiLoader
        ui_file = QFile(self.ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Cannot open {self.ui_file_path}: {ui_file.errorString()}")

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("Failed to load the UI file.")

    def show_view(self):
        # Show the loaded UI window
        if self.ui:
            self.ui.show()

    def setup_views(self):
        from views.home_view import HomeView
        from views.alarms_view import AlarmsView
        from views.statistics_view import StatisticsView
        from views.chat_view import ChatView

        # Find widgets by name from the loaded UI
        self.homeView_widget = self.ui.findChild(QWidget, "homePage")
        self.alarmsView_widget = self.ui.findChild(QWidget, "alarmPage")
        self.statisticsView_widget = self.ui.findChild(QWidget, "statisticsPage")
        self.remindersView_widget = self.ui.findChild(QWidget, "remindersPage")
        self.chatView_widget = self.ui.findChild(QWidget, "chatPage")

        # Initialize each view
        self.homePage = HomeView(self.homeView_widget)
        self.alarmPage = AlarmsView(self.alarmsView_widget)
        self.statisticsPage = StatisticsView(self.statisticsView_widget)
        self.chatPage = ChatView(self.chatView_widget)

        # Connect controller
        self.statisticsPage.connect_controller(self)
        self.alarmPage.connect_controller(self)
        self.homePage.connect_controller(self)

        # Default values for staticstic view
        self.on_range_selected("Week")
        self.statisticsPage.week_button.setChecked(True)

        # Set up navigation between pages
        self.setup_navigation_buttons()

        # Load and display alarms
        self.update_alarm_list()

    # Connect navigation buttons to their corresponding pages
    def setup_navigation_buttons(self):
        self.ui.homeButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.homeView_widget))
        self.ui.alarmButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.alarmsView_widget))
        self.ui.statisticsButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.statisticsView_widget))
        self.ui.microphoneButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.chatView_widget))

        # Forward buttons from the main screen
        self.ui.f_alarmButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.alarmsView_widget))
        self.ui.f_statisticsButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.statisticsView_widget))
        self.ui.f_chatButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.chatView_widget))

    # Update the chart with data corresponding to the selected time period
    def on_range_selected(self, period: str):
        sleep_data, water_data = self.model.get_statistics(period)

        avg_sleep = self.model.compute_average(sleep_data)
        avg_water = self.model.compute_average(water_data)

        self.statisticsPage.update_chart(sleep_data, water_data, avg_sleep, avg_water)

    # Show popup to add a new alarm
    def show_add_alarm_popup(self):
        from views.alarm_popup import AlarmPopup
        self.update_alarm_list()

        popup = AlarmPopup("ui_files/popup.ui")
        popup.exec()

    # Show simulation of an active alarm - for display purposes
    def show_alarm_sim(self):
        from views.active_alarm_popup import ActiveAlarmPopup

        popup = ActiveAlarmPopup("ui_files/active_alarm.ui")
        popup.exec()

    # Update/display alarms - currently just displays as there is no real data
    def update_alarm_list(self):
        alarms = self.model.get_alarms()
        self.alarmPage.display_alarms(alarms)
