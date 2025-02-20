import random
import math

class Graph:
    def __init__(self, num_vertices, graph_type, min_weight, max_weight):
        self.num_vertices = num_vertices
        self.graph_type = graph_type
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.graph = {str(i): {} for i in range(num_vertices)}
        self.positions = {}

    def generate_graph(self, num_edges):
        for _ in range(num_edges):
            u = random.choice(list(self.graph.keys()))
            v = random.choice(list(self.graph.keys()))

            if u == v:
                continue  # Не добавляем рёбра от вершины к самой себе

            weight = random.randint(self.min_weight, self.max_weight)

            if self.graph_type == 1:  # Ориентированный граф
                self.graph[u][v] = weight
            else:  # Неориентированный граф
                self.graph[u][v] = weight
                self.graph[v][u] = weight

    def display_positions(self, canvas_width, canvas_height):
        # Равномерно распределяем вершины по экрану
        positions = {}
        angle_step = 2*math.pi/self.num_vertices
        radius = 200
        center_x, center_y = canvas_width / 2, canvas_height / 2

        for i, vertex in enumerate(self.graph.keys()):
            angle = i * angle_step
            x = center_x + radius * 2 * random.random() * random.choice([1, -1])
            y = center_y + radius * 2 * random.random() * random.choice([1, -1])
            positions[vertex] = (x, y)

        self.positions = positions
