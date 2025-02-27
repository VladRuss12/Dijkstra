import random

from GraphGen.GraphPattern import GraphPattern


class RandomGraphPattern(GraphPattern):
    def generate_graph(self, num_vertices, num_edges):
        graph = {str(i): {} for i in range(num_vertices)}
        for _ in range(num_edges):
            u = random.choice(list(graph.keys()))
            v = random.choice(list(graph.keys()))

            if u == v:
                continue  # Не добавляем рёбра от вершины к самой себе

            weight = random.randint(1, 10)
            graph[u][v] = weight
            graph[v][u] = weight  # Для неориентированного графа

        return graph

    def display_positions(self, canvas_width, canvas_height, positions):
        # Простое случайное распределение вершин
        return {str(i): (random.uniform(0, canvas_width), random.uniform(0, canvas_height)) for i in range(len(positions))}