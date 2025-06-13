from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

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
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("Failed to load the UI file.")
        
        # Buttons
        self.save_button: QPushButton = self.ui.findChild(QPushButton, "saveButton")
        self.cancel_button: QPushButton = self.ui.findChild(QPushButton, "cancelButton")

        self.show()
        # Close pop up
        if self.save_button:
            self.save_button.clicked.connect(self.close)
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.close)
