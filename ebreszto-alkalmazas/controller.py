from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QWidget,
    QPushButton
)

from ui_files import*

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
        widget = self.ui.findChild(widget_type, widget_name)
        if widget is None:
            print(f"[DEBUG] Widget '{widget_name}' not found in UI.")
        else:
            print(f"[DEBUG] Found widget '{widget_name}': {widget}")
        return widget

    def setup_views(self):
        from views.alarms_view import AlarmsView
        self.alarmsView_widget = self.ui.findChild(QWidget, "alarmPage")

        # Create the views
        self.alarmPage = AlarmsView(self.alarmsView_widget)
        # Add navigation buttons
        # self.setup_navigation_buttons()

    # def setup_navigation_buttons(self):
        # Find navigation buttons
        # TODO self.ui.home_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.mainPage))