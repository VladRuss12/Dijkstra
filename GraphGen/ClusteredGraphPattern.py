import random
import math
import numpy as np
from GraphGen.GraphPattern import GraphPattern


class ClusteredGraphPattern(GraphPattern):
    def __init__(self):
        # По умолчанию значения будут переопределяться в зависимости от количества вершин
        self.num_clusters = 3
        self.cluster_radius = 300

    def generate_graph(self, num_vertices, edge_probability, min_weight, max_weight):
        # Динамически определяем количество кластеров на основе количества вершин.
        # Например, используем квадратный корень от количества вершин (минимум 2).
        self.num_clusters = max(2, int(math.sqrt(num_vertices)))
        # Можем также масштабировать радиус кластера (например, с корневой зависимостью)
        self.cluster_radius = 300 * (num_vertices / 100) ** 0.5

        # Сначала распределим вершины по кластерам
        cluster_assignments = self.assign_clusters(num_vertices, self.num_clusters)

        graph = {str(i): {} for i in range(num_vertices)}

        # Определяем вероятность для межкластерных рёбер (нам нужно меньше связей между кластерами)
        edge_probability_inter = edge_probability * 0.2  # например, 20% от базовой вероятности

        for u in range(num_vertices):
            for v in range(u + 1, num_vertices):
                if cluster_assignments[u] == cluster_assignments[v]:
                    # Если вершины принадлежат одному кластеру – используем базовую вероятность
                    if random.random() <= edge_probability:
                        weight = random.randint(min_weight, max_weight)
                        graph[str(u)][str(v)] = weight
                        graph[str(v)][str(u)] = weight
                else:
                    # Если вершины из разных кластеров – создаем ребро с меньшей вероятностью
                    if random.random() <= edge_probability_inter:
                        weight = random.randint(min_weight, max_weight)
                        graph[str(u)][str(v)] = weight
                        graph[str(v)][str(u)] = weight

        # Сохраняем распределение по кластерам для использования при отображении
        self.cluster_assignments = cluster_assignments

        return graph

    def display_positions(self, canvas_width, canvas_height, positions, min_distance=50):
        # Получаем центры кластеров в пределах области отображения
        centers = self.generate_cluster_centers(canvas_width, canvas_height, self.num_clusters)

        # Если распределение по кластерам уже было посчитано при генерации графа, используем его
        if hasattr(self, 'cluster_assignments'):
            cluster_assignments = self.cluster_assignments
        else:
            cluster_assignments = self.assign_clusters(len(positions), self.num_clusters)

        position_map = {}
        # Для размещения вершин внутри каждого кластера используем радиус меньше, чем при генерации ребер
        cluster_radius = self.cluster_radius * 0.5

        for i, cluster_id in enumerate(cluster_assignments):
            # Начальное случайное размещение внутри кластера
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, cluster_radius)
            x = centers[cluster_id][0] + distance * math.cos(angle)
            y = centers[cluster_id][1] + distance * math.sin(angle)

            # Проверка на минимальное расстояние от других узлов
            while self.check_overlap(x, y, position_map, min_distance):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, cluster_radius)
                x = centers[cluster_id][0] + distance * math.cos(angle)
                y = centers[cluster_id][1] + distance * math.sin(angle)

            position_map[str(i)] = (x, y)

        return position_map

    def check_overlap(self, x, y, position_map, min_distance):
        """
        Проверяет, не перекрывается ли текущая позиция с уже размещёнными узлами.
        """
        for (px, py) in position_map.values():
            if self.euclidean_distance((x, y), (px, py)) < min_distance:
                return True
        return False

    def generate_cluster_centers(self, width, height, num_clusters):
        """
        Размещаем центры кластеров равномерно по области.
        """
        centers = []
        angle_step = 2 * math.pi / num_clusters
        # Используем меньший радиус, чтобы кластеры не выходили за границы экрана
        center_radius = min(width, height) / 3

        for i in range(num_clusters):
            angle = i * angle_step
            cx = width / 2 + center_radius * math.cos(angle)
            cy = height / 2 + center_radius * math.sin(angle)
            centers.append((cx, cy))

        return centers

    def assign_clusters(self, num_vertices, num_clusters):
        """
        Равномерно распределяем вершины по кластерам.
        """
        clusters = []
        for cluster_id in range(num_clusters):
            clusters.extend([cluster_id] * (num_vertices // num_clusters))
        # Если остались вершины – распределяем их случайно
        while len(clusters) < num_vertices:
            clusters.append(random.randint(0, num_clusters - 1))
        random.shuffle(clusters)
        return clusters

    def euclidean_distance(self, p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
