from PySide6.QtGui import QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
import random
from PySide6.QtCore import Qt

class GraphWidget(QGraphicsView):
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

    def drawGraph(self):
        self.scene.clear()

        # Рёбра с увеличенной толщиной (рисуем их первыми)
        for u, edges in self.graph.graph.items():
            for v, weight in edges.items():
                u_pos = self.graph.positions[u]
                v_pos = self.graph.positions[v]

                # Немного отодвигаем рёбра от узлов, чтобы они не перекрывали узлы
                u_pos_offset = (u_pos[0] + random.uniform(-5, 5), u_pos[1] + random.uniform(-5, 5))
                v_pos_offset = (v_pos[0] + random.uniform(-5, 5), v_pos[1] + random.uniform(-5, 5))

                pen = QPen(QColor(0, 0, 0))  # Черный цвет для рёбер
                pen.setWidth(3)  # Толщина рёбер
                pen.setCapStyle(Qt.RoundCap)  # Круглые окончания рёбер
                pen.setJoinStyle(Qt.RoundJoin)  # Скругленные соединения рёбер
                self.scene.addLine(u_pos_offset[0], u_pos_offset[1], v_pos_offset[0], v_pos_offset[1], pen)

                # Добавление текста с весом рёбер
                mid_x = (u_pos_offset[0] + v_pos_offset[0]) / 2
                mid_y = (u_pos_offset[1] + v_pos_offset[1]) / 2

                weight_text_item = self.scene.addText(str(weight))
                weight_text_item.setPos(mid_x - 10, mid_y - 15)
                weight_text_item.setDefaultTextColor(QColor(255, 255, 255))  # Белый цвет для текста
                weight_text_item.setFont(QFont("Arial", 10, QFont.Bold))

                # Добавление фона под текст
                text_rect = weight_text_item.boundingRect()
                text_background = QBrush(QColor(0, 0, 0, 120))  # Полупрозрачный чёрный фон
                self.scene.addRect(text_rect, QPen(), text_background)

        # Генерация случайного цвета для каждого узла
        for vertex, pos in self.graph.positions.items():
            node_color = self.randomColor()

            radius = 20  # Радиус узлов для лучшей видимости
            node_brush = QBrush(QColor(node_color[0], node_color[1], node_color[2]))

            # Узлы рисуются в их исходных позициях
            self.scene.addEllipse(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2, QPen(), node_brush)

            text_item = self.scene.addText(vertex)
            text_item.setPos(pos[0] - 6, pos[1] - 6)  # Центрирование текста внутри круга
            text_item.setDefaultTextColor(QColor(255, 255, 255))
            text_item.setFont(QFont("Arial", 10, QFont.Bold))

    def randomColor(self):
        """Генерация случайного цвета RGB, исключая белый"""
        while True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            if (r, g, b) != (255, 255, 255):  # Исключаем белый цвет
                return (r, g, b)
