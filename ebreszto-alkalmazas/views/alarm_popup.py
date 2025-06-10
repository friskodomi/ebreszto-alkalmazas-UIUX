from PySide6.QtWidgets import QDialog, QTimeEdit, QComboBox, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTime

import ui_files.rc_icons

class AlarmPopup(QDialog):
    def __init__(self, ui_file_path):
        super().__init__()
        self.ui_file_path = ui_file_path
        self.load_ui()

    def load_ui(self):
        ui_file = QFile(self.ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Cannot open {self.ui_file_path}: {ui_file.errorString()}")

        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  # load into this dialog
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("Failed to load the UI file.")

        self.show()
