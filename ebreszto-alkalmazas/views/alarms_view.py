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
        self.alarms_groupbox = QGroupBox("")
        self.alarms_groupbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        # --- Layout for groupbox ---
        self.alarmLayout = QVBoxLayout()
        self.alarmLayout.setSpacing(0)
        self.alarmLayout.setContentsMargins(0, 0, 10, 10)
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

    def create_alarm_widget(self, alarm_data: dict, group_name: str) -> QWidget:
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

        return alarm_widget


    def display_alarms(self, alarm_groups_data: list[dict], controller=None):
        # Clear layout
        while self.alarmLayout.count():
            item = self.alarmLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for group_index, group in enumerate(alarm_groups_data):
            group_name = group["group_name"]
            alarms = group["alarms"]

            for i, alarm_data in enumerate(alarms):
                alarm_widget = self.create_alarm_widget(alarm_data, group_name)

                # Show group_details only for first alarm in group
                group_details = alarm_widget.findChild(QWidget, "group_details")
                if i == 0:
                    group_label = group_details.findChild(QLabel, "group_name")
                    if group_label:
                        group_label.setText(group_name)

                else:
                    group_details.hide()  # Hide for other alarms in group

                self.alarmLayout.addWidget(alarm_widget)

