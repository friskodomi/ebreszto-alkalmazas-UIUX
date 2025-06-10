from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame

import ui_files.rc_icons

class AlarmsView:
    def __init__(self, alarmPage_widget):
        self.alarmPage = alarmPage_widget

        # Buttons
        self.add_alarm_button: QPushButton = self.alarmPage.findChild(QPushButton, "alarm_addButton")

    def connect_controller(self, controller):
        if self.add_alarm_button:
            self.add_alarm_button.clicked.connect(controller.show_add_alarm_popup)