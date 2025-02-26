from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QSpinBox, QComboBox, QPushButton, QDialogButtonBox


class GraphSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройки генерации графа")

        # Создание виджетов
        self.num_vertices_spin = QSpinBox(self)
        self.num_vertices_spin.setRange(1, 100)
        self.num_vertices_spin.setValue(10)

        self.num_edges_spin = QSpinBox(self)
        self.num_edges_spin.setRange(1, 200)
        self.num_edges_spin.setValue(15)

        self.min_weight_spin = QSpinBox(self)
        self.min_weight_spin.setRange(1, 100)
        self.min_weight_spin.setValue(1)

        self.max_weight_spin = QSpinBox(self)
        self.max_weight_spin.setRange(1, 100)
        self.max_weight_spin.setValue(10)

        self.graph_type_combo = QComboBox(self)
        self.graph_type_combo.addItem("Ориентированный")
        self.graph_type_combo.addItem("Неориентированный")

        # Кнопки
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Компоновка
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.addRow("Количество вершин:", self.num_vertices_spin)
        form_layout.addRow("Количество рёбер:", self.num_edges_spin)
        form_layout.addRow("Минимальный вес рёбер:", self.min_weight_spin)
        form_layout.addRow("Максимальный вес рёбер:", self.max_weight_spin)
        form_layout.addRow("Тип графа:", self.graph_type_combo)

        layout.addLayout(form_layout)
        layout.addWidget(self.buttons)

    def getSettings(self):
        return {
            'num_vertices': self.num_vertices_spin.value(),
            'num_edges': self.num_edges_spin.value(),
            'min_weight': self.min_weight_spin.value(),
            'max_weight': self.max_weight_spin.value(),
            'graph_type': self.graph_type_combo.currentIndex()
        }