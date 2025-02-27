import random
import math
from GraphGen.GraphPattern import GraphPattern

class TreeGraphPattern(GraphPattern):
    def generate_graph(self, num_vertices, num_edges):
        """
        Генерация древовидного графа с указанным числом вершин и рёбер.
        Древовидная структура создаётся путём добавления рёбер от случайных
        вершин к родителям.
        """
        graph = {str(i): {} for i in range(num_vertices)}

        # Формируем древовидную структуру, добавляя рёбра от случайных родителей
        for i in range(1, num_vertices):
            parent = random.choice(list(graph.keys())[:i])  # Родитель для текущей вершины
            weight = random.randint(1, 10)
            graph[parent][str(i)] = weight
            graph[str(i)][parent] = weight  # Для неориентированного графа

        return graph

    def display_positions(self, canvas_width, canvas_height, graph):
        """
        Генерация позиций для древовидного графа на холсте.
        """
        position_map = {}
        visited = set()  # Множество для отслеживания посещённых вершин

        # Корень дерева в центре холста
        position_map["0"] = (canvas_width / 2, canvas_height / 2)
        visited.add("0")

        def place_children(node, level, y_offset):
            """
            Рекурсивное размещение дочерних вершин на холсте относительно текущей вершины.
            """
            # Получаем детей для текущей вершины
            children = [k for k in graph.keys() if k != node and node in graph[k]]

            # Убираем уже посещённые вершины
            children = [child for child in children if child not in visited]

            if not children:
                return

            # Расставляем детей по горизонтали с отступом, по вертикали с постоянным шагом
            angle_step = 2 * math.pi / len(children)  # Делим круг между дочерними вершинами
            x_offset = 150  # Ширина между дочерними вершинами
            for i, child in enumerate(children):
                # Позиционируем дочерние элементы по горизонтали
                x = position_map[node][0] + x_offset * math.cos(i * angle_step)
                y = position_map[node][1] + y_offset  # Вертикальный сдвиг не меняется
                position_map[child] = (x, y)
                visited.add(child)  # Отмечаем вершину как посещённую
                place_children(child, level + 1, y_offset + 100)  # Отступ для следующего уровня

        # Начинаем размещение с корня дерева
        place_children("0", 0, 100)
        return position_map
