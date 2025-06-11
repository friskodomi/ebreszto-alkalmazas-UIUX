from PySide6.QtWidgets import QPushButton, QListWidget
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QListWidgetItem, QWidget, QLabel


import ui_files.rc_icons

class AlarmsView:
    def __init__(self, alarmPage_widget):
        self.alarmPage = alarmPage_widget

        # Buttons
        self.add_alarm_button: QPushButton = self.alarmPage.findChild(QPushButton, "add_alarm_button")

        self.scrollWidget: QWidget = self.alarmPage.findChild(QWidget, "scrollWidget")
        self.scrollArea: QScrollArea = self.alarmPage.findChild(QScrollArea, "scrollArea")
        self.add_alarm_button: QPushButton = self.alarmPage.findChild(QPushButton, "add_alarm_button")
        self.alarmLayout: QVBoxLayout = self.scrollWidget.layout()


    def connect_controller(self, controller):
        if self.add_alarm_button:
            self.add_alarm_button.clicked.connect(controller.show_add_alarm_popup)

    def create_alarm_widget(self, alarm_data: dict) -> QWidget:
        print(alarm_data)
        ui_file = QFile("ui_files/alarm_widget.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        widget = loader.load(ui_file)
        ui_file.close()

        # Fill in alarm details
        widget.findChild(QLabel, "hour_label").setText(alarm_data["time"].split(":")[0])
        widget.findChild(QLabel, "minute_label").setText(alarm_data["time"].split(":")[1])
        widget.findChild(QLabel, "hour_minute_separator").setText(":")
        widget.findChild(QLabel, "days_repeat_label").setText(", ".join(alarm_data["repeat_days"]))
        widget.findChild(QLabel, "alarm_name").setText(alarm_data["alarm_name"])

        print(widget)
        return widget
    

    def display_alarms(self, alarm_data_list: list[dict]):
        # Insert alarm widgets before the spacer
        for alarm_data in alarm_data_list:
            alarm_widget = self.create_alarm_widget(alarm_data)
            print(alarm_data)
            self.alarmLayout.insertWidget(self.alarmLayout.count() - 1, alarm_widget)





