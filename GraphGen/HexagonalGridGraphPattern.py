import random
import math
from GraphGen.GraphPattern import GraphPattern

class HexagonalGridGraphPattern(GraphPattern):
    def generate_graph(self, num_vertices, edge_probability, min_weight, max_weight):
        graph = {str(i): {} for i in range(num_vertices)}

        # Генерация рёбер: определяем связи между соседними узлами
        for u in range(num_vertices):
            neighbors = self.get_neighbors(u, num_vertices)
            for v in neighbors:
                # Ребро добавляем только если u < v, чтобы избежать дублирования
                if u < v:
                    # Добавляем ребро только с заданной вероятностью
                    if random.random() <= edge_probability:
                        weight = random.randint(min_weight, max_weight)
                        graph[str(u)][str(v)] = weight
                        graph[str(v)][str(u)] = weight  # Неориентированный граф
        return graph

    def get_neighbors(self, u, num_vertices):
        # Предполагаем, что граф реализуется в виде 2D-сетки
        neighbors = []
        rows = 10
        cols = 10
        i, j = u // cols, u % cols  # Позиция узла в сетке (i, j)

        # Определяем соседей для шестиугольной сетки
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbor = ni * cols + nj
                if neighbor < num_vertices:
                    neighbors.append(neighbor)
        return neighbors

    def display_positions(self, canvas_width, canvas_height, positions):
        position_map = {}
        # Увеличиваем радиус, чтобы узлы располагались дальше друг от друга
        radius = 120  # Увеличенный радиус для шестиугольников
        # Подбираем количество строк и столбцов по числу вершин
        rows = int(math.ceil(math.sqrt(len(positions))))
        cols = int(math.ceil(len(positions) / rows))

        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if index < len(positions):
                    # Изменённые коэффициенты для большей разнесенности узлов
                    x = radius * 2 * j
                    y = radius * math.sqrt(3) * (i + 0.5 * (j % 2))
                    position_map[str(index)] = (x, y)
        return position_map
