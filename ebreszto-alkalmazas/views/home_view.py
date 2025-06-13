from PySide6.QtWidgets import QPushButton

class HomeView:
    def __init__(self, homePage_widget):
        self.homePage = homePage_widget

        self.alarm_sim_button: QPushButton = self.homePage.findChild(QPushButton, "acitve_alarm_simButton")

    # Connect controler for the alarm simulation
    def connect_controller(self, controller):
        if self.alarm_sim_button:
            self.alarm_sim_button.clicked.connect(controller.show_alarm_sim)