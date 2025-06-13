from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QIcon

import ui_files.rc_icons

class HomeView:
    def __init__(self, homePage_widget):
        self.homePage = homePage_widget

        self.alarm_sim_button: QPushButton = self.homePage.findChild(QPushButton, "acitve_alarm_simButton")

    def connect_controller(self, controller):
        if self.alarm_sim_button:
            self.alarm_sim_button.clicked.connect(controller.show_alarm_sim)