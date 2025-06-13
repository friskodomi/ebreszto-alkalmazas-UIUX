from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QScrollArea,
    QLabel, QSizePolicy, QFormLayout, QGroupBox, QHBoxLayout
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


    from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QScrollArea,
    QLabel, QSizePolicy, QGroupBox, QHBoxLayout, QFrame
)
from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader

import ui_files.rc_icons


class AlarmsView:
    def __init__(self, alarmPage_widget):
        self.alarmPage = alarmPage_widget

        self.add_alarm_button: QPushButton = self.alarmPage.findChild(QPushButton, "add_alarm_button")
        self.scrollArea: QScrollArea = self.alarmPage.findChild(QScrollArea, "scrollArea")

        self.scrollAreaContent = QWidget()
        self.scrollArea.setWidget(self.scrollAreaContent)
        self.scrollArea.setWidgetResizable(True)

        self.containerLayout = QVBoxLayout()
        self.containerLayout.setSpacing(8)
        self.scrollAreaContent.setLayout(self.containerLayout)

        # Keep track of group alarm layouts for toggling
        self.group_alarm_layouts = {}

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

        return alarm_widget




    def display_alarms(self, alarm_groups_data: list[dict], controller=None):
        while self.containerLayout.count():
            item = self.containerLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.group_alarm_layouts.clear()

        for group_index, group in enumerate(alarm_groups_data):
            group_id = f"group_{group_index}"
            group_name = group["group_name"]
            alarms = group["alarms"]

            # --- Group wrapper ---
            group_widget = QWidget()
            group_layout = QVBoxLayout()
            group_layout.setContentsMargins(0, 0, 0, 0)
            group_widget.setLayout(group_layout)

            # --- Group header (manual) ---
            header_widget = QWidget()
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(8, 2, 8, 2)
            header_widget.setLayout(header_layout)

            group_label = QLabel(group_name)
            group_label.setStyleSheet("font-weight: bold; font-size: 14px;")

            toggle_button = QPushButton("▼")
            toggle_button.setCheckable(True)
            toggle_button.setChecked(True)
            toggle_button.setFixedSize(24, 24)
            toggle_button.setObjectName(f"toggle_button_{group_id}")

            header_layout.addWidget(toggle_button)
            header_layout.addWidget(group_label)
            header_layout.addStretch()

            group_layout.addWidget(header_widget)

            # --- Alarm container ---
            alarms_container = QWidget()
            alarms_layout = QVBoxLayout()
            alarms_layout.setContentsMargins(20, 4, 4, 4)
            alarms_container.setLayout(alarms_layout)

            for alarm_data in alarms:
                alarm_widget = self.create_alarm_widget(alarm_data)
                alarms_layout.addWidget(alarm_widget)

            group_layout.addWidget(alarms_container)

            # --- Store reference for toggling ---
            self.group_alarm_layouts[group_id] = alarms_container

            # --- Connect toggle ---
            toggle_button.clicked.connect(lambda checked, gid=group_id: self.toggle_group(gid, checked))

            # --- Add to scroll area ---
            self.containerLayout.addWidget(group_widget)

        self.containerLayout.addStretch()



    def toggle_group(self, group_id: str, checked: bool):
        container = self.group_alarm_layouts.get(group_id)
        if container:
            container.setVisible(checked)

        # Optional: update button text to ▼ / ▶
        toggle_button = self.scrollAreaContent.findChild(QPushButton, f"toggle_button_{group_id}")
        if toggle_button:
            toggle_button.setText("▼" if checked else "▶")


