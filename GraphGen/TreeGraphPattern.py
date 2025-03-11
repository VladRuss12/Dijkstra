import random
import math
from GraphGen.GraphPattern import GraphPattern


class TreeGraphPattern(GraphPattern):
    def generate_graph(self, num_vertices, edge_probability, min_weight, max_weight):
        """
        Генерация связного древовидного графа.
        Каждая вершина (кроме корня) соединяется ровно с одним родителем.
        """
        graph = {str(i): {} for i in range(num_vertices)}
        self.parents = {}
        self.children = {str(i): [] for i in range(num_vertices)}

        for i in range(1, num_vertices):
            parent = random.choice(list(graph.keys())[:i])
            self.parents[str(i)] = parent
            self.children[parent].append(str(i))
            weight = random.randint(min_weight, max_weight)
            graph[parent][str(i)] = weight
            graph[str(i)][parent] = weight

        return graph

    def display_positions(self, canvas_width, canvas_height, graph):
        """
        Иерархическое позиционирование с гарантированным расстоянием между узлами
        """
        position_map = {}
        min_distance = 120  # Минимальное расстояние между узлами
        level_height = 120  # Расстояние между уровнями

        # Построение структуры дерева
        children = {node: [] for node in graph}
        for child, parent in self.parents.items():
            children[parent].append(child)

        # Расчёт максимальной глубины
        def calc_depth(node):
            if not children[node]:
                return 0
            return 1 + max(calc_depth(child) for child in children[node])

        max_depth = calc_depth('0')
        y_step = (canvas_height - 100) / (max_depth + 1) if max_depth > 0 else 0

        # Рекурсивное размещение с учётом расстояния
        def place_node(node, depth, x_min, x_max):
            child_nodes = children.get(node, [])
            num_children = len(child_nodes)

            # Позиция текущего узла
            if node == '0':
                x = canvas_width / 2
                y = 50
            else:
                x = (x_min + x_max) / 2
                y = 50 + depth * y_step

            position_map[node] = (x, y)

            # Расчёт доступного пространства для детей
            if num_children > 0:
                required_width = num_children * min_distance
                available_width = x_max - x_min
                x_step = max(min_distance, available_width / num_children)

                start_x = x - (x_step * (num_children - 1)) / 2
                for i, child in enumerate(child_nodes):
                    child_x = start_x + i * x_step
                    child_x = max(40, min(canvas_width - 40, child_x))
                    place_node(child, depth + 1,
                               child_x - x_step / 2,
                               child_x + x_step / 2)

        place_node('0', 0, 40, canvas_width - 40)

        # Проверка и коррекция коллизий
        nodes = list(position_map.items())
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1, (x1, y1) = nodes[i]
                n2, (x2, y2) = nodes[j]
                dx = x2 - x1
                dy = y2 - y1
                distance = math.hypot(dx, dy)

                if distance < min_distance:
                    # Корректируем позиции
                    adjust = (min_distance - distance) / 2
                    angle = math.atan2(dy, dx) if dx != 0 or dy != 0 else 0

                    position_map[n1] = (x1 - adjust * math.cos(angle),
                                        y1 - adjust * math.sin(angle))
                    position_map[n2] = (x2 + adjust * math.cos(angle),
                                        y2 + adjust * math.sin(angle))

        return position_map
