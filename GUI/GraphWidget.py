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

                # Использование QPen для рёбер
                pen = QPen(QColor(0, 0, 0))  # Черный цвет для рёбер
                pen.setWidth(8)  # Толщина рёбер
                pen.setCapStyle(Qt.RoundCap)  # Круглые окончания рёбер
                pen.setJoinStyle(Qt.RoundJoin)  # Скругленные соединения рёбер
                self.scene.addLine(u_pos[0], u_pos[1], v_pos[0], v_pos[1], pen)

                # Добавление текста с весом рёбер
                mid_x = (u_pos[0] + v_pos[0]) / 2
                mid_y = (u_pos[1] + v_pos[1]) / 2

                # Создаём текстовое поле для веса
                weight_text_item = self.scene.addText(str(weight))

                # Располагаем текст чуть выше линии ребра для лучшей читаемости
                weight_text_item.setPos(mid_x - 10, mid_y - 15)  # Сдвигаем текст немного вверх

                # Настройки для текста (белый цвет, жирный шрифт)
                weight_text_item.setDefaultTextColor(QColor(255, 255, 255))  # Белый цвет для текста
                weight_text_item.setFont(QFont("Arial", 10, QFont.Bold))  # Жирный шрифт для текста

                # Добавление фона под текст для лучшей читаемости (полупрозрачный чёрный фон)
                text_rect = weight_text_item.boundingRect()
                text_background = QBrush(QColor(0, 0, 0, 120))  # Чёрный полупрозрачный фон
                self.scene.addRect(text_rect, QPen(), text_background)

        # Генерация случайного цвета для каждого узла
        for vertex, pos in self.graph.positions.items():
            # Генерация случайного цвета (кроме белого)
            node_color = self.randomColor()

            # Увеличиваем радиус узлов для лучшей видимости
            radius = 20

            # Добавление закрашенного круга для узла с этим цветом
            node_brush = QBrush(QColor(node_color[0], node_color[1], node_color[2]))
            self.scene.addEllipse(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2, QPen(), node_brush)

            # Добавление текста с номером узла внутри, белого цвета и улучшенного шрифта
            text_item = self.scene.addText(vertex)
            text_item.setPos(pos[0] - 6, pos[1] - 6)  # Центрирование текста внутри круга
            text_item.setDefaultTextColor(QColor(255, 255, 255))  # Белый цвет для текста
            text_item.setFont(QFont("Arial", 10, QFont.Bold))  # Улучшенный шрифт для текста

    def randomColor(self):
        """Генерация случайного цвета RGB, исключая белый"""
        while True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            if (r, g, b) != (255, 255, 255):  # Исключаем белый цвет
                return (r, g, b)
