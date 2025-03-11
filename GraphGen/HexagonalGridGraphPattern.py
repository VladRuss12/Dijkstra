import random
import math
from typing import Dict, List, Tuple
from GraphGen.GraphPattern import GraphPattern


class HexagonalGridGraphPattern(GraphPattern):
    def __init__(self, base_connectivity_prob: float = 0.8):
        self.base_connectivity_prob = base_connectivity_prob

    def generate_graph(self, num_vertices: int, edge_probability: float,
                       min_weight: int, max_weight: int) -> Dict[str, Dict[str, int]]:
        graph = {str(i): {} for i in range(num_vertices)}
        rows, cols = self.calculate_grid_size(num_vertices)

        # Гарантированное соединение ближайших соседей
        for u in range(num_vertices):
            neighbors = self.get_valid_neighbors(u, num_vertices, rows, cols)

            # Только обязательные соединения с базовой вероятностью
            for v in neighbors:
                if u < v and (random.random() <= self.base_connectivity_prob):
                    self._add_edge(graph, u, v, min_weight, max_weight)

        return graph

    def _add_edge(self, graph: Dict[str, Dict[str, int]], u: int, v: int,
                  min_weight: int, max_weight: int):
        if str(v) not in graph[str(u)]:
            weight = random.randint(min_weight, max_weight)
            graph[str(u)][str(v)] = weight
            graph[str(v)][str(u)] = weight

    def get_valid_neighbors(self, u: int, num_vertices: int,
                            rows: int, cols: int) -> List[int]:
        i, j = divmod(u, cols)
        neighbors = []
        directions = self._get_directions(j)

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbor = ni * cols + nj
                if neighbor < num_vertices:
                    neighbors.append(neighbor)
        return neighbors

    def _get_directions(self, col: int) -> List[Tuple[int, int]]:
        # Убираем диагональные рёбра, оставляем только прямые
        if col % 2 == 0:
            return [(-1, 0), (0, -1), (0, 1), (1, 0)]
        else:
            return [(-1, 0), (0, -1), (0, 1), (1, 0)]

    def calculate_grid_size(self, num_vertices: int) -> Tuple[int, int]:
        cols = math.ceil(math.sqrt(num_vertices))
        rows = math.ceil(num_vertices / cols)
        return rows, cols

    def display_positions(self, canvas_width: float, canvas_height: float,
                          positions: List[str]) -> Dict[str, Tuple[float, float]]:
        position_map = {}
        rows, cols = self.calculate_grid_size(len(positions))

        # Автоматический расчет размера ячейки
        hex_width = canvas_width / max(cols, 1)
        hex_height = canvas_height / max(rows, 1)
        radius = min(hex_width, hex_height * 0.8) / 2

        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if index < len(positions):
                    x_offset = 0.5 * radius if i % 2 else 0
                    x = radius * 2 * j + x_offset
                    y = radius * math.sqrt(3) * i

                    # Центрирование на холсте
                    x += (canvas_width - (cols * radius * 2)) / 2
                    y += (canvas_height - (rows * radius * math.sqrt(3))) / 2

                    position_map[str(index)] = (x, y)
        return position_map
