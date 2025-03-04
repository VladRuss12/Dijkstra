# GUI/DijkstraDialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox
from PySide6.QtCore import Qt


class DijkstraDialog(QDialog):
    def __init__(self, graph, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Поиск кратчайшего пути (Дейкстра)")

        self.graph = graph

        self.start_vertex_combo = QComboBox(self)
        self.end_vertex_combo = QComboBox(self)

        if graph is not None:
            vertices = list(graph.get_adj_list().keys())
            self.start_vertex_combo.addItems(map(str, vertices))
            self.end_vertex_combo.addItems(map(str, vertices))

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Начальная вершина:", self))
        layout.addWidget(self.start_vertex_combo)
        layout.addWidget(QLabel("Конечная вершина:", self))
        layout.addWidget(self.end_vertex_combo)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_selected_vertices(self):
        start = int(self.start_vertex_combo.currentText())
        end = int(self.end_vertex_combo.currentText())
        return start, end
