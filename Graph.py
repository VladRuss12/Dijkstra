import random
import math
import numpy as np


class Graph:
    def __init__(self, num_vertices, graph_type, min_weight, max_weight):
        self.num_vertices = num_vertices
        self.graph_type = graph_type
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.num_clusters = max(1, num_vertices // 6)  # Количество кластеров зависит от числа узлов
        self.graph = {str(i): {} for i in range(num_vertices)}
        self.positions = {}

    def generate_graph(self, num_edges):
        added_edges = set()
        for _ in range(num_edges):
            u, v = random.sample(self.graph.keys(), 2)  # Выбираем две разные вершины
            if (u, v) in added_edges or (v, u) in added_edges:
                continue
            weight = random.randint(self.min_weight, self.max_weight)
            if self.graph_type == 1:
                self.graph[u][v] = weight
            else:
                self.graph[u][v] = weight
                self.graph[v][u] = weight
            added_edges.add((u, v))

    def k_means(self, data, k):
        """Алгоритм k-means для кластеризации"""
        centroids = random.sample(data, k)  # Случайные центроиды
        prev_centroids = None
        clusters = {i: [] for i in range(k)}

        while centroids != prev_centroids:
            prev_centroids = centroids.copy()
            clusters = {i: [] for i in range(k)}

            for point in data:
                distances = [self.distance(point, centroid) for centroid in centroids]
                closest_centroid = distances.index(min(distances))
                clusters[closest_centroid].append(point)

            centroids = []
            for i in range(k):
                if clusters[i]:
                    centroids.append(np.mean(clusters[i], axis=0))
                else:
                    centroids.append(random.choice(data))  # Новый случайный центр

        return centroids, clusters

    def distance(self, point1, point2):
        return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))

    def display_positions(self, canvas_width, canvas_height):
        positions = {}
        data = [[random.uniform(0, canvas_width), random.uniform(0, canvas_height)] for _ in self.graph.keys()]

        centroids, clusters = self.k_means(data, self.num_clusters)

        for vertex, point in zip(self.graph.keys(), data):
            for cluster_id, cluster_points in clusters.items():
                if point in cluster_points:
                    positions[vertex] = list(centroids[cluster_id])  # Привязываем вершину к своему кластеру
                    break

        self.positions = positions

    def get_positions(self):
        return self.positions
