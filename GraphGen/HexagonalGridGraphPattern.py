import random
import math
from GraphGen.GraphPattern import GraphPattern


# Паттерн в виде сот с учетом количества вершин и рёбер
class HexagonalGridGraphPattern(GraphPattern):
    def generate_graph(self, num_vertices, num_edges):
        graph = {str(i): {} for i in range(num_vertices)}

        # Генерация рёбер (сначала определим связи между соседними узлами)
        possible_edges = []
        for u in range(num_vertices):
            # Подключаем соседей для каждого узла (в данном примере, смежность по оси x и y)
            neighbors = self.get_neighbors(u, num_vertices)
            for v in neighbors:
                if u < v:  # чтобы не было повторных рёбер
                    possible_edges.append((u, v))

        # Случайный выбор рёбер из возможных
        selected_edges = random.sample(possible_edges, min(num_edges, len(possible_edges)))
        for u, v in selected_edges:
            weight = random.randint(1, 10)
            graph[str(u)][str(v)] = weight
            graph[str(v)][str(u)] = weight  # Для неориентированного графа

        return graph

    def get_neighbors(self, u, num_vertices):
        # Предполагаем, что граф реализуется в виде сетки 2D
        neighbors = []
        # Рассчитываем возможных соседей на основе индексов вершин
        # Например, соседями могут быть элементы справа, слева, выше, ниже
        # Реализация для шестиугольной сетки
        rows = 10
        cols = 10
        i, j = u // cols, u % cols  # Позиция узла в сетке (i, j)

        # Определяем соседей (в рамках границ сетки)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]  # Направления для шестиугольной сетки
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbor = ni * cols + nj
                if neighbor < num_vertices:
                    neighbors.append(neighbor)

        return neighbors

    def display_positions(self, canvas_width, canvas_height, positions):
        position_map = {}
        radius = 40  # Радиус для шестиугольников
        # Сетка с динамическим количеством строк и колонок, исходя из num_vertices
        rows = int(math.ceil(math.sqrt(len(positions))))
        cols = int(math.ceil(len(positions) / rows))

        for i in range(rows):
            for j in range(cols):
                if i * cols + j < len(positions):  # Проверяем, что узел существует
                    x = radius * 3 / 2 * j
                    y = radius * math.sqrt(3) * (i + 0.5 * (j % 2))
                    position_map[str(i * cols + j)] = (x, y)

        return position_map
