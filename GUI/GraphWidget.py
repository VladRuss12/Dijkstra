from typing import List
from PySide6.QtGui import QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsRectItem, QToolTip, \
    QGraphicsItem
import random
from PySide6.QtCore import Qt

from GUI.CustomToolTip import CustomToolTip


class GraphWidget(QGraphicsView):
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.highlighted_path = []
        self.setMouseTracking(True)  # Включаем отслеживание мыши
        self.current_item = None  # Переменная для хранения текущего элемента для подсказки
        self.tooltip = CustomToolTip(self)  # Создаем пользовательскую подсказку
        self.tooltip.hide()  # Скрываем подсказку при старте

    def drawGraph(self):
        self.scene.clear()
        self.adjustSceneSize()  # Добавляем автоматическое масштабирование

        # Рёбра
        for u, edges in self.graph.graph.items():
            for v, weight in edges.items():
                if int(u) < int(v):
                    u_pos = self.graph.positions[u]
                    v_pos = self.graph.positions[v]

                    u_pos_offset = (u_pos[0] + random.uniform(-5, 5), u_pos[1] + random.uniform(-5, 5))
                    v_pos_offset = (v_pos[0] + random.uniform(-5, 5), v_pos[1] + random.uniform(-5, 5))

                    pen = QPen(QColor(0, 0, 0))  # Черный цвет
                    pen.setWidth(2)  # Уменьшаем толщину
                    pen.setColor(QColor(0, 0, 0, 100))  # Прозрачный чёрный цвет
                    pen.setCapStyle(Qt.RoundCap)
                    pen.setJoinStyle(Qt.RoundJoin)
                    line = self.scene.addLine(u_pos_offset[0], u_pos_offset[1], v_pos_offset[0], v_pos_offset[1], pen)

                    # Ребро для подсказки
                    line.setData(0, (u, v, weight))  # Сохраняем данные ребра для использования при наведении

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

            ellipse = self.scene.addEllipse(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2, QPen(),
                                            node_brush)

            # Узел для подсказки
            ellipse.setData(0, (vertex, pos))  # Сохраняем данные узла

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

    def mouseMoveEvent(self, event):
        """Обработчик движения мыши, отображающий подсказки"""
        point = self.mapToScene(event.pos())
        item = self.scene.itemAt(point, self.transform())

        if item and isinstance(item, QGraphicsItem):
            data = item.data(0)
            if data:
                if self.current_item != item:
                    self.current_item = item
                    if len(data) == 3:  # Если это ребро
                        u, v, weight = data
                        connected_nodes = self.get_connected_nodes(u, v)
                        tooltip_text = f"Ребро: {u} → {v}, Вес: {weight}, Связанные узлы: {connected_nodes}"
                    elif len(data) == 2:  # Если это узел
                        vertex, pos = data
                        connected_edges = self.get_connected_edges(vertex)
                        tooltip_text = f"Узел: {vertex}, Позиция: {pos}, Связанные рёбра: {connected_edges}"

                    # Показываем пользовательскую подсказку
                    self.tooltip.setText(tooltip_text)
                    self.tooltip.adjustSize()

                    # Получаем глобальные координаты курсора
                    global_pos = event.globalPos()
                    # Получаем размеры подсказки
                    tooltip_size = self.tooltip.size()
                    # Получаем размеры экрана
                    screen_geometry = self.screen().availableGeometry()

                    # Вычисляем новую позицию подсказки, чтобы она не выходила за границы экрана
                    x = global_pos.x() + 10
                    y = global_pos.y() + 10

                    # Проверяем, не выходит ли подсказка за правую границу экрана
                    if x + tooltip_size.width() > screen_geometry.right():
                        x = screen_geometry.right() - tooltip_size.width()

                    # Проверяем, не выходит ли подсказка за нижнюю границу экрана
                    if y + tooltip_size.height() > screen_geometry.bottom():
                        y = screen_geometry.bottom() - tooltip_size.height()

                    # Перемещаем подсказку
                    self.tooltip.move(x, y)
                    self.tooltip.show()
            else:
                # Если элемент не содержит данных, скрываем подсказку
                self.tooltip.hide()
        else:
            # Если курсор не на элементе, скрываем подсказку
            self.tooltip.hide()

        super().mouseMoveEvent(event)

    def randomColor(self):
        """Генерация случайного цвета RGB, исключая белый"""
        while True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            if (r, g, b) != (255, 255, 255):
                return (r, g, b)

    def get_connected_nodes(self, u, v):
        """Получаем список узлов, связанных с данным ребром"""
        return [u, v]

    def get_connected_edges(self, vertex):
        """Получаем список уникальных рёбер, связанных с данным узлом"""
        edges = set()  # Используем множество для хранения уникальных рёбер
        for u, edges_dict in self.graph.graph.items():
            if vertex in edges_dict:
                edges.add((u, vertex))  # Добавляем ребро в одном направлении
            for v in edges_dict:
                if vertex == v:
                    edges.add((u, v))  # Добавляем ребро в другом направлении
        return list(edges)  # Возвращаем список уникальных рёбер

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

    def adjustSceneSize(self):
        """Автоматическое изменение размеров сцены по границам графа"""
        if not self.graph.positions:
            return

        min_x = min(pos[0] for pos in self.graph.positions.values())
        max_x = max(pos[0] for pos in self.graph.positions.values())
        min_y = min(pos[1] for pos in self.graph.positions.values())
        max_y = max(pos[1] for pos in self.graph.positions.values())

        padding = 50  # Дополнительное пространство для отступов
        self.scene.setSceneRect(min_x - padding, min_y - padding,
                                (max_x - min_x) + 2 * padding,
                                (max_y - min_y) + 2 * padding)