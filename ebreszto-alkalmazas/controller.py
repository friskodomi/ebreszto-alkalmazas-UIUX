from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

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

    def setup_views(self):
        from views.home_view import HomeView
        from views.alarms_view import AlarmsView

        # Create the views
        self.home_view = HomeView()
        self.alarms_view = AlarmsView()

    def show_view(self):
        if self.ui:
            self.ui.show()

