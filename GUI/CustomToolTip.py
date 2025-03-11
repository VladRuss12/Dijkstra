from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLabel

class CustomToolTip(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            background-color: yellow;
            border: 1px solid black;
            padding: 5px;
        """)