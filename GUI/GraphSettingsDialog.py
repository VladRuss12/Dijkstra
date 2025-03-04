from PySide6.QtWidgets import QDoubleSpinBox, QDialog, QVBoxLayout, QFormLayout, QSpinBox, QComboBox, QDialogButtonBox

class GraphSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройки генерации графа")

        # Создание виджетов
        self.num_vertices_spin = QSpinBox(self)
        self.num_vertices_spin.setRange(1, 100)
        self.num_vertices_spin.setValue(10)

        self.min_weight_spin = QSpinBox(self)
        self.min_weight_spin.setRange(1, 100)
        self.min_weight_spin.setValue(1)

        self.max_weight_spin = QSpinBox(self)
        self.max_weight_spin.setRange(1, 100)
        self.max_weight_spin.setValue(10)

        self.edge_probability_spin = QDoubleSpinBox(self)
        self.edge_probability_spin.setRange(0.01, 1.0)
        self.edge_probability_spin.setSingleStep(0.01)
        self.edge_probability_spin.setValue(0.25)

        # Добавление ComboBox для выбора паттерна
        self.pattern_combo = QComboBox(self)
        self.pattern_combo.addItem("Случайный граф")
        self.pattern_combo.addItem("Древовидный граф")
        self.pattern_combo.addItem("Граф с кластеризацией")
        self.pattern_combo.addItem("Граф в виде сот")

        # Кнопки
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Компоновка
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.addRow("Количество вершин:", self.num_vertices_spin)
        form_layout.addRow("Минимальный вес рёбер:", self.min_weight_spin)
        form_layout.addRow("Максимальный вес рёбер:", self.max_weight_spin)
        form_layout.addRow("Вероятность ребра:", self.edge_probability_spin)
        form_layout.addRow("Паттерн графа:", self.pattern_combo)

        layout.addLayout(form_layout)
        layout.addWidget(self.buttons)

    def getSettings(self):
        return {
            'num_vertices': self.num_vertices_spin.value(),
            'min_weight': self.min_weight_spin.value(),
            'max_weight': self.max_weight_spin.value(),
            'edge_probability': self.edge_probability_spin.value(),
            'pattern': self.pattern_combo.currentIndex()  # Добавляем индекс выбранного паттерна
        }
