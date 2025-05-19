import sys
from PySide6.QtWidgets import QApplication
from controller import Controller
from views.statistics_view import StatisticsView

import ui_files.rc_icons

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize the controller with the path to the .ui file
    ui_file_path = "ui_files/ui.ui"
    app_controller = Controller(ui_file_path, model=None)

    # Load the UI and show it
    app_controller.load_ui()
    app_controller.setup_views()
    app_controller.show_view()

    sys.exit(app.exec())