import random
from GraphGen.GraphPattern import GraphPattern

class RandomGraphPattern(GraphPattern):
    def generate_graph(self, num_vertices, edge_probability, min_weight, max_weight):
        # Создание пустого графа
        graph = {str(i): {} for i in range(num_vertices)}

        # Определение возможных рёбер
        possible_edges = []
        for u in range(num_vertices):
            for v in range(u + 1, num_vertices):  # Только u < v, чтобы избежать дублирования
                possible_edges.append((u, v))

        # Считаем, сколько рёбер нужно сгенерировать, исходя из вероятности
        num_edges = int(len(possible_edges) * edge_probability)

        # Выбираем случайные рёбра без дублирования
        selected_edges = random.sample(possible_edges, num_edges)

        # Добавляем рёбра в граф с весом
        for u, v in selected_edges:
            weight = random.randint(min_weight, max_weight)

            # Для неориентированного графа добавляем рёбра только в одну сторону
            if str(v) not in graph[str(u)]:
                graph[str(u)][str(v)] = weight
            if str(u) not in graph[str(v)]:
                graph[str(v)][str(u)] = weight  # Для неориентированного графа

        return graph

    def display_positions(self, canvas_width, canvas_height, positions):
        # Простое случайное распределение вершин
        return {str(i): (random.uniform(0, canvas_width), random.uniform(0, canvas_height)) for i in range(len(positions))}
