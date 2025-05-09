from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QWidget,
)


class UIManager:
    def __init__(self, ui_file_name: str, parent: QWidget):
        self.ui_file_name = ui_file_name
        self.parent = parent
        self.window = self._load_ui()

    # Load the UI file and return the main window widget
    def _load_ui(self) -> QWidget:
        loader = QUiLoader()
        ui_file = QFile(self.ui_file_name)

        if not ui_file.open(QIODevice.ReadOnly):
            raise IOError(f"Cannot open {self.ui_file_name}: {ui_file.errorString()}")

        window = loader.load(ui_file, self.parent)
        ui_file.close()

        if not window:
            raise RuntimeError(loader.errorString())

        return window

    # Find a widget by name and type
    def find_widget(self, widget_type, widget_name: str):
        return self.window.findChild(widget_type, widget_name)
