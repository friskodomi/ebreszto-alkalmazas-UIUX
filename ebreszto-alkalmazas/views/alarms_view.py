from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QScrollArea,
    QLabel, QHBoxLayout,
    QGraphicsOpacityEffect
)
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


class AlarmsView:
    def __init__(self, alarmPage_widget):
        self.alarmPage = alarmPage_widget

        # Getting the widgets from the ui file
        self.add_alarm_button: QPushButton = self.alarmPage.findChild(QPushButton, "add_alarm_button")
        self.scrollArea: QScrollArea = self.alarmPage.findChild(QScrollArea, "scrollArea")

        # Set up for the scroll area
        # Creating the content widget
        self.scrollAreaContent = QWidget()
        self.scrollArea.setWidget(self.scrollAreaContent)
        self.scrollArea.setWidgetResizable(True)

        # Create the layout for the alarm widgets
        self.containerLayout = QVBoxLayout()
        self.scrollAreaContent.setLayout(self.containerLayout)

        self.group_alarm_layouts = {}
        self.group_onoff_buttons = {}
        self.alarm_toggles_per_group = {}

    # Connect controller with the button to pop up the add alarm window
    def connect_controller(self, controller):
        if self.add_alarm_button:
            self.add_alarm_button.clicked.connect(controller.show_add_alarm_popup)

    # Creates the alarm from the .ui file template
    def create_alarm_widget(self, alarm_data: dict, group_id: str = "") -> tuple[QWidget, QPushButton]:
        ui_file = QFile("ui_files/alarm_widget.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        alarm_widget = loader.load(ui_file)
        ui_file.close()

        if alarm_widget is None:
            return QWidget(), QPushButton()

        # Set time and repeat days
        alarm_widget.findChild(QLabel, "hour_label").setText(alarm_data["time"].split(":")[0])
        alarm_widget.findChild(QLabel, "minute_label").setText(alarm_data["time"].split(":")[1])
        alarm_widget.findChild(QLabel, "hour_minute_separator").setText(":")
        alarm_widget.findChild(QLabel, "days_repeat_label").setText(", ".join(alarm_data["repeat_days"]))

        # Created a button for toggle on/off
        # This is the way i found to create unique buttons that work with some backround logic
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

        opacity_effect = QGraphicsOpacityEffect()
        alarm_widget.setGraphicsEffect(opacity_effect)

        # Adjust opactiy for better visual feedback
        def update_opacity(checked):
            opacity_effect.setOpacity(1.0 if checked else 0.4)

        update_opacity(toggle.isChecked())
        toggle.toggled.connect(update_opacity)

        # Insert the toggle button into the layout
        layout = alarm_widget.layout()
        if layout:
            layout.insertWidget(0, toggle)

        return alarm_widget, toggle

    # Clears and rebuilds the list of alarm groups and their alarms
    def display_alarms(self, alarm_groups_data: list[dict], controller=None):
        while self.containerLayout.count():
            item = self.containerLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.group_alarm_layouts.clear()
        self.group_onoff_buttons.clear()
        self.alarm_toggles_per_group.clear()

        # Building each group
        for group_index, group in enumerate(alarm_groups_data):
            group_id = f"group_{group_index}"
            group_name = group["group_name"]
            alarms = group["alarms"]

            self.alarm_toggles_per_group[group_id] = []

            # Main group container
            group_widget = QWidget()
            group_layout = QVBoxLayout()
            group_widget.setLayout(group_layout)

            # Group Header
            header_widget = QWidget()
            header_layout = QHBoxLayout()
            header_widget.setLayout(header_layout)

            # Expand/collapse toggle
            # Creating the uique buttons here
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

            # Group label for the name
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

            # Group-level on/off toggle
            onoff_button = QPushButton("")
            onoff_button.setFixedSize(40, 20)
            onoff_button.setCheckable(True)
            onoff_button.setChecked(True)
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

            # Alarms Container
            alarms_container = QWidget()
            alarms_layout = QVBoxLayout()
            alarms_container.setLayout(alarms_layout)

            for alarm_data in alarms:
                alarm_widget, toggle = self.create_alarm_widget(alarm_data, group_id)
                alarms_layout.addWidget(alarm_widget)

                self.alarm_toggles_per_group[group_id].append(toggle)

                # Ensure group is on if any alarm is on
                toggle.toggled.connect(lambda checked, gid=group_id: self.enable_group_if_alarm_on(gid, checked))

            alarms_container.setVisible(False)
            group_layout.addWidget(alarms_container)

            # Connect group controls
            self.group_alarm_layouts[group_id] = alarms_container
            self.group_onoff_buttons[group_id] = onoff_button

            toggle_button.clicked.connect(lambda checked, gid=group_id: self.toggle_group(gid, checked))
            onoff_button.clicked.connect(lambda checked, gid=group_id: self.toggle_group_onoff(gid, checked))

            self.containerLayout.addWidget(group_widget)

        self.containerLayout.addStretch()

    # Toggles all alarms in a group on/off based on the alarms in the group
    def toggle_group_onoff(self, group_id: str, checked: bool):
        for toggle in self.alarm_toggles_per_group.get(group_id, []):
            toggle.blockSignals(True)
            toggle.setChecked(checked)
            toggle.blockSignals(False)

            effect = toggle.parentWidget().graphicsEffect()
            if effect:
                effect.setOpacity(1.0 if checked else 0.4)

    # Ensures the group switch is enabled if any alarm in the group is on
    # disables it if all alarms are off
    def enable_group_if_alarm_on(self, group_id: str, _checked: bool):
        toggles = self.alarm_toggles_per_group.get(group_id, [])
        group_button = self.group_onoff_buttons.get(group_id)

        if not group_button:
            return

        if any(toggle.isChecked() for toggle in toggles):
            # At least one alarm is on → group should be on
            if not group_button.isChecked():
                group_button.setChecked(True)
        else:
            # All alarms are off → group should be off
            if group_button.isChecked():
                group_button.setChecked(False)

    # Expand of collapse the alarm group
    def toggle_group(self, group_id: str, checked: bool):
        container = self.group_alarm_layouts.get(group_id)
        if container:
            container.setVisible(checked)

        toggle_button = self.scrollAreaContent.findChild(QPushButton, f"toggle_button_{group_id}")
        if toggle_button:
            toggle_button.setText("▼" if checked else "▶")
