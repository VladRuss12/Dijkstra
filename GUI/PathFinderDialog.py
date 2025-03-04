from typing import Tuple

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox


class PathFinderDialog(QDialog):
    def __init__(self, vertices, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Найти кратчайший путь")

        layout = QVBoxLayout()
        self.start_combo = QComboBox()
        self.end_combo = QComboBox()

        for v in vertices:
            self.start_combo.addItem(v)
            self.end_combo.addItem(v)

        layout.addWidget(QLabel("Начальная вершина:"))
        layout.addWidget(self.start_combo)
        layout.addWidget(QLabel("Конечная вершина:"))
        layout.addWidget(self.end_combo)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_selected_vertices(self) -> Tuple[str, str]:
        return (
            self.start_combo.currentText(),
            self.end_combo.currentText()
        )