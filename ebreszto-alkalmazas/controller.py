from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QWidget,
)

from ui_files.icons import*

class Controller:
    def __init__(self, ui_file_path, model):
        self.ui_file_path = ui_file_path
        self.model = model
        self.ui = None

    
    def load_ui(self):
        ui_file = QFile(self.ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Cannot open {self.ui_file_path}: {ui_file.errorString()}")

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("Failed to load the UI file.")

    def show_view(self):
        if self.ui:
            self.ui.show()

    # Find a widget by name and type
    def find_widget(self, widget_type, widget_name: str):
        return self.window.findChild(widget_type, widget_name)

    def setup_views(self):
        from views.home_view import HomeView
        from views.alarms_view import AlarmsView

        self.homeView_widget = self.find_widget(QWidget, "homePage")
        # self.alarmsView_widget = self.find_widget(QWidget, "alarmPage")

        # Create the views
        self.home_view = HomeView(self.homeView_widget)
        # self.alarms_view = AlarmsView(self.alarmsView_widget)

