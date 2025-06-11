from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QScrollArea,
    QLabel, QSizePolicy, QFormLayout, QGroupBox
)
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

import ui_files.rc_icons

class AlarmsView:
    def __init__(self, alarmPage_widget):
        self.alarmPage = alarmPage_widget

        self.add_alarm_button: QPushButton = self.alarmPage.findChild(QPushButton, "add_alarm_button")
        self.scrollArea: QScrollArea = self.alarmPage.findChild(QScrollArea, "scrollArea")

        # --- Setup container for scroll area ---
        self.scrollAreaContent = QWidget()
        self.scrollArea.setWidget(self.scrollAreaContent)
        self.scrollArea.setWidgetResizable(True)

        # --- Setup groupbox inside the scroll area ---
        self.alarms_groupbox = QGroupBox("Alarms")
        self.alarms_groupbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        # --- Layout for groupbox ---
        self.alarmLayout = QVBoxLayout()
        self.alarmLayout.setSpacing(8)
        self.alarmLayout.setContentsMargins(10, 10, 10, 10)
        self.alarms_groupbox.setLayout(self.alarmLayout)

        # --- Layout for scrollAreaContent ---
        self.containerLayout = QVBoxLayout()
        self.containerLayout.addWidget(self.alarms_groupbox)
        self.containerLayout.addStretch()  # Keep alarms top-aligned
        self.scrollAreaContent.setLayout(self.containerLayout)

        # Set size policy to allow vertical expansion
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.alarms_groupbox.setSizePolicy(size_policy)

    def connect_controller(self, controller):
        if self.add_alarm_button:
            self.add_alarm_button.clicked.connect(controller.show_add_alarm_popup)

    def create_alarm_widget(self, alarm_data: dict) -> QWidget:
        ui_file = QFile("ui_files/alarm_widget.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        alarm_widget = loader.load(ui_file)
        ui_file.close()

        if alarm_widget is None:
            return QWidget()

        alarm_widget.findChild(QLabel, "hour_label").setText(alarm_data["time"].split(":")[0])
        alarm_widget.findChild(QLabel, "minute_label").setText(alarm_data["time"].split(":")[1])
        alarm_widget.findChild(QLabel, "hour_minute_separator").setText(":")
        alarm_widget.findChild(QLabel, "days_repeat_label").setText(", ".join(alarm_data["repeat_days"]))
        alarm_widget.findChild(QLabel, "alarm_name").setText(alarm_data["alarm_name"])

        return alarm_widget

    def display_alarms(self, alarm_data_list: list[dict]):
        # Clear existing alarm widgets
        while self.alarmLayout.count():
            item = self.alarmLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add each alarm widget
        for alarm_data in alarm_data_list:
            alarm_widget = self.create_alarm_widget(alarm_data)
            self.alarmLayout.addWidget(alarm_widget)

