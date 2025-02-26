from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox, QDialog
from GUI.GraphWidget import GraphWidget
from Graph import Graph
from GUI.GraphSettingsDialog import GraphSettingsDialog  # Импортируем наш диалог с настройками

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Генерация графов")
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowState(Qt.WindowMaximized)

        self.graph = None

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.graph_widget = None
        layout.addWidget(self.createMenu())
        layout.addWidget(self.createGraphArea())

    def createMenu(self):
        menu_bar = self.menuBar()
        graph_menu = menu_bar.addMenu("Граф")

        generate_action = QAction("Сгенерировать граф", self)
        generate_action.triggered.connect(self.showGraphSettingsDialog)  # Открываем диалог для настроек
        graph_menu.addAction(generate_action)

        return menu_bar

    def createGraphArea(self):
        self.graph_widget = GraphWidget(self.graph)
        return self.graph_widget

    def showGraphSettingsDialog(self):
        dialog = GraphSettingsDialog(self)  # Создаем диалог для ввода настроек
        if dialog.exec() == QDialog.Accepted:
            settings = dialog.getSettings()
            self.generateGraph(settings)

    def generateGraph(self, settings):
        num_vertices = settings['num_vertices']
        num_edges = settings['num_edges']
        min_weight = settings['min_weight']
        max_weight = settings['max_weight']
        graph_type = settings['graph_type']

        self.graph = Graph(num_vertices, graph_type, min_weight, max_weight)
        self.graph.generate_graph(num_edges)
        self.graph.display_positions(self.width(), self.height())

        self.graph_widget.graph = self.graph
        self.graph_widget.drawGraph()
