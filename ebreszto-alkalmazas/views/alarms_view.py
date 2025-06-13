from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QScrollArea,
    QLabel, QSizePolicy, QGroupBox, QHBoxLayout, QFrame
)
from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QGraphicsOpacityEffect

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

        # Set labels
        alarm_widget.findChild(QLabel, "hour_label").setText(alarm_data["time"].split(":")[0])
        alarm_widget.findChild(QLabel, "minute_label").setText(alarm_data["time"].split(":")[1])
        alarm_widget.findChild(QLabel, "hour_minute_separator").setText(":")
        alarm_widget.findChild(QLabel, "days_repeat_label").setText(", ".join(alarm_data["repeat_days"]))

        # Add toggle button
        toggle = QPushButton()
        toggle.setCheckable(True)
        toggle.setChecked(alarm_data.get("enabled", True))
        toggle.setFixedSize(50, 28)
        toggle.setStyleSheet("""
            QPushButton {
                background-color: #b4c3d0;
                border-radius: 14px;
                border: 2px solid #9aaab9;
            }
            QPushButton:checked {
                background-color: #4d5e6d;
                border-radius: 14px;
                border: 2px solid #3a4956;
            }
        """)

        # Set initial opacity
        opacity_effect = QGraphicsOpacityEffect()
        alarm_widget.setGraphicsEffect(opacity_effect)

        def update_opacity(checked):
            opacity_effect.setOpacity(1.0 if checked else 0.4)

        # Apply initial state
        update_opacity(toggle.isChecked())

        # Connect toggle to update opacity
        toggle.toggled.connect(update_opacity)

        # Insert toggle into layout
        layout = alarm_widget.layout()
        if layout:
            layout.insertWidget(0, toggle)

        return alarm_widget


    def display_alarms(self, alarm_groups_data: list[dict], controller=None):
        while self.containerLayout.count():
            item = self.containerLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.group_alarm_layouts.clear()
        self.group_onoff_buttons = {}

        for group_index, group in enumerate(alarm_groups_data):
            group_id = f"group_{group_index}"
            group_name = group["group_name"]
            alarms = group["alarms"]

            group_widget = QWidget()
            group_layout = QVBoxLayout()
            group_widget.setLayout(group_layout)

            # --- Group Header ---
            header_widget = QWidget()
            header_layout = QHBoxLayout()
            header_widget.setLayout(header_layout)

            toggle_button = QPushButton("▶")
            toggle_button.setCheckable(True)
            toggle_button.setChecked(False)
            toggle_button.setFixedSize(28, 28)
            toggle_button.setObjectName(f"toggle_button_{group_id}")
            toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: #b4c3d0;
                    border-radius:10px;
                    font-size: 16px;
                    font-weight: bold;
                    color: #333;
                }
                QPushButton:pressed {
                    background-color: #b4c3d0;
                    border-radius:10px;
                    font-size: 16px;
                    font-weight: bold;
                    color: #333;
                }
            """)

            group_label = QLabel(group_name)
            group_label.setStyleSheet("""
                QLabel {
                    font-family: 'Roboto';
                    font-size: 24px;
                    background-color: transparent;
                    font-weight: bold;
                    color: #4d5e6d;
                }
            """)

            onoff_button = QPushButton("On")
            onoff_button.setText("")  # Optional: remove text for visual-only toggle
            onoff_button.setFixedSize(40, 20)
            onoff_button.setCheckable(True)
            onoff_button.setObjectName(f"onoff_button_{group_id}")
            onoff_button.setStyleSheet("""
                QPushButton {
                    background-color: #b4c3d0;
                    border-radius: 10px;
                }
                QPushButton:checked {
                    background-color:#4d5e6d;
                    border-radius: 10px;
                }
            """)

            header_layout.addWidget(toggle_button)
            header_layout.addWidget(group_label)
            header_layout.addStretch()
            header_layout.addWidget(onoff_button)

            group_layout.addWidget(header_widget)

            # --- Alarms Container ---
            alarms_container = QWidget()
            alarms_layout = QVBoxLayout()
            alarms_container.setLayout(alarms_layout)

            for alarm_data in alarms:
                alarm_widget = self.create_alarm_widget(alarm_data)
                alarms_layout.addWidget(alarm_widget)

            alarms_container.setVisible(False)
            group_layout.addWidget(alarms_container)

            self.group_alarm_layouts[group_id] = alarms_container
            self.group_onoff_buttons[group_id] = onoff_button

            toggle_button.clicked.connect(lambda checked, gid=group_id: self.toggle_group(gid, checked))
            onoff_button.clicked.connect(lambda checked, gid=group_id: self.toggle_group_onoff(gid, checked))

            self.containerLayout.addWidget(group_widget)

        self.containerLayout.addStretch()


    def toggle_group_onoff(self, group_id: str, checked: bool):
        # Placeholder logic: for now, just print the status.
        print(f"Group '{group_id}' toggled {'ON' if checked else 'OFF'}")
        # Future idea: disable all alarms in that group visually or logically.




    def toggle_group(self, group_id: str, checked: bool):
        container = self.group_alarm_layouts.get(group_id)
        if container:
            container.setVisible(checked)

        # Optional: update button text to ▼ / ▶
        toggle_button = self.scrollAreaContent.findChild(QPushButton, f"toggle_button_{group_id}")
        if toggle_button:
            toggle_button.setText("▼" if checked else "▶")


