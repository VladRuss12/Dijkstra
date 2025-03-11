from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QDialog

from GUI.GraphSettingsDialog import GraphSettingsDialog
from Algoritm.Dijkstra import Dijkstra
from GUI.GraphWidget import GraphWidget
from GUI.PathFinderDialog import PathFinderDialog
from GraphGen.Graph import Graph
from GraphGen.RandomGraphPattern import RandomGraphPattern
from GraphGen.TreeGraphPattern import TreeGraphPattern
from GraphGen.ClusteredGraphPattern import ClusteredGraphPattern
from GraphGen.HexagonalGridGraphPattern import HexagonalGridGraphPattern

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

        find_path_action = QAction("Найти кратчайший путь", self)
        find_path_action.triggered.connect(self.find_shortest_path)
        self.menuBar().addAction(find_path_action)

        return menu_bar
    def createGraphArea(self):
        self.graph = Graph(
            num_vertices=0,
            min_weight=0,
            max_weight=0,
            pattern=RandomGraphPattern(),
            edge_probability=0
        )
        self.graph_widget = GraphWidget(self.graph)
        return self.graph_widget

    def showGraphSettingsDialog(self):
        dialog = GraphSettingsDialog(self)  # Создаем диалог для ввода настроек
        if dialog.exec() == QDialog.Accepted:
            settings = dialog.getSettings()
            self.generateGraph(settings)

    def generateGraph(self, settings):
        num_vertices = settings['num_vertices']
        min_weight = settings['min_weight']
        max_weight = settings['max_weight']
        pattern_index = settings['pattern']
        edge_probability = settings.get('edge_probability')  # Если ключ не найден, установить значение по умолчанию

        # Выбор паттерна в зависимости от выбора пользователя
        if pattern_index == 0:
            pattern = RandomGraphPattern()
        elif pattern_index == 1:
            pattern = TreeGraphPattern()
        elif pattern_index == 2:
            pattern = ClusteredGraphPattern()
        elif pattern_index == 3:
            pattern = HexagonalGridGraphPattern()

        self.graph = Graph(num_vertices, min_weight, max_weight, pattern, edge_probability)

        # Теперь передаем все необходимые параметры
        self.graph.generate_graph()  # В методе generate_graph() все параметры уже использованы внутри объекта

        self.graph.display_positions(self.width(), self.height())

        self.graph_widget.graph = self.graph
        self.graph_widget.highlighted_path = []
        self.graph_widget.drawGraph()
        self.graph_widget.setInteractive(True)

    def find_shortest_path(self):
        if not self.graph or not self.graph.graph:
            return

        vertices = list(self.graph.graph.keys())
        dialog = PathFinderDialog(vertices, self)
        if dialog.exec() == QDialog.Accepted:
            start, end = dialog.get_selected_vertices()

            # Вычисляем путь
            path, distance = Dijkstra.find_shortest_path(
                self.graph.graph,
                start,
                end
            )

            if path:
                self.graph_widget.highlight_path(path)
                self.statusBar().showMessage(
                    f"Кратчайший путь: {' → '.join(path)} | Длина: {distance}"
                )
            else:
                self.statusBar().showMessage("Путь не найден!")