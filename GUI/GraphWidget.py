from typing import List

from PySide6.QtGui import QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsRectItem
import random
from PySide6.QtCore import Qt

class GraphWidget(QGraphicsView):
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.highlighted_path = []

    def drawGraph(self):
        self.scene.clear()

        # Рёбра с увеличенной толщиной
        for u, edges in self.graph.graph.items():
            for v, weight in edges.items():
                if int(u) < int(v):
                    u_pos = self.graph.positions[u]
                    v_pos = self.graph.positions[v]

                    # Лёгкий сдвиг рёбер, чтобы не перекрывали узлы
                    u_pos_offset = (u_pos[0] + random.uniform(-5, 5), u_pos[1] + random.uniform(-5, 5))
                    v_pos_offset = (v_pos[0] + random.uniform(-5, 5), v_pos[1] + random.uniform(-5, 5))

                    pen = QPen(QColor(0, 0, 0))  # Черный цвет
                    pen.setWidth(3)
                    pen.setCapStyle(Qt.RoundCap)
                    pen.setJoinStyle(Qt.RoundJoin)
                    self.scene.addLine(u_pos_offset[0], u_pos_offset[1], v_pos_offset[0], v_pos_offset[1], pen)

                    # Текст с весом ребра
                    mid_x = (u_pos_offset[0] + v_pos_offset[0]) / 2
                    mid_y = (u_pos_offset[1] + v_pos_offset[1]) / 2

                    offset_x = mid_x + 10
                    offset_y = mid_y + 10

                    weight_text_item = QGraphicsTextItem(str(weight))
                    weight_text_item.setDefaultTextColor(QColor(0, 0, 0))
                    weight_text_item.setFont(QFont("Arial", 10, QFont.Bold))
                    weight_text_item.setPos(offset_x, offset_y)

                    # Фон под текст
                    text_rect = weight_text_item.boundingRect()
                    background_rect = QGraphicsRectItem(text_rect)
                    background_rect.setPos(offset_x, offset_y)
                    background_rect.setBrush(QBrush(QColor(255, 255, 255, 200)))
                    background_rect.setZValue(-1)  # Фон под текстом

                    self.scene.addItem(background_rect)
                    self.scene.addItem(weight_text_item)

        # Узлы
        for vertex, pos in self.graph.positions.items():
            node_color = self.randomColor()

            radius = 20
            node_brush = QBrush(QColor(node_color[0], node_color[1], node_color[2]))

            self.scene.addEllipse(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2, QPen(), node_brush)

            # Подписываем узел
            text_item = QGraphicsTextItem(vertex)
            text_item.setDefaultTextColor(QColor(255, 255, 255))
            text_item.setFont(QFont("Arial", 10, QFont.Bold))

            # Центрируем текст внутри круга
            text_rect = text_item.boundingRect()
            text_item.setPos(pos[0] - text_rect.width() / 2, pos[1] - text_rect.height() / 2)

            self.scene.addItem(text_item)

        if self.highlighted_path:
            self._draw_highlighted_path()
    def randomColor(self):
        """Генерация случайного цвета RGB, исключая белый"""
        while True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            if (r, g, b) != (255, 255, 255):
                return (r, g, b)

    def highlight_path(self, path: List[str]):
        self.highlighted_path = path
        self.drawGraph()

    def _draw_highlighted_path(self):
        path_edges = []
        for i in range(len(self.highlighted_path) - 1):
            u = self.highlighted_path[i]
            v = self.highlighted_path[i + 1]
            path_edges.append((u, v))

        # Рисуем рёбра пути
        for u, v in path_edges:
            u_pos = self.graph.positions[u]
            v_pos = self.graph.positions[v]

            pen = QPen(QColor(255, 0, 0))  # Красный цвет
            pen.setWidth(5)
            line = self.scene.addLine(
                u_pos[0], u_pos[1],
                v_pos[0], v_pos[1],
                pen
            )
            line.setZValue(1)  # Поверх других элементов

        # Подсветка узлов
        for node in self.highlighted_path:
            pos = self.graph.positions[node]
            radius = 25  # Немного больше обычных узлов
            brush = QBrush(QColor(255, 0, 0, 100))  # Красная подсветка
            self.scene.addEllipse(
                pos[0] - radius,
                pos[1] - radius,
                radius * 2,
                radius * 2,
                QPen(Qt.NoPen),
                brush
            ).setZValue(0.5)