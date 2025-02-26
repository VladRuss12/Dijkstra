import random
import math
import numpy as np

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

    def euclidean_distance(self, p1, p2):
        """Вычисляем евклидово расстояние между двумя точками (p1 и p2)"""
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def kmeans(self, positions, k, max_iter=100):
        """Реализация алгоритма K-means"""
        centers = random.sample(list(positions), k)

        for _ in range(max_iter):
            clusters = {i: [] for i in range(k)}

            for i, point in enumerate(positions):
                distances = [self.euclidean_distance(point, center) for center in centers]
                closest_center = distances.index(min(distances))
                clusters[closest_center].append(i)

            new_centers = []
            for cluster in clusters.values():
                if cluster:
                    cluster_points = [positions[i] for i in cluster]
                    new_center = np.mean(cluster_points, axis=0)
                    new_centers.append(new_center)
                else:
                    new_centers.append(random.choice(positions))

            if np.allclose(new_centers, centers):
                break
            centers = new_centers

        return centers

    def display_positions(self, canvas_width, canvas_height):
        positions = np.array(
            [[random.uniform(0, canvas_width), random.uniform(0, canvas_height)] for _ in range(self.num_vertices)])

        k = min(self.num_vertices // 2, 10)
        centers = self.kmeans(positions, k)

        cluster_radius = 100
        self.positions = {}
        for i in range(self.num_vertices):
            closest_center = min(range(k), key=lambda j: self.euclidean_distance(positions[i], centers[j]))
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, cluster_radius)
            x = centers[closest_center][0] + distance * math.cos(angle)
            y = centers[closest_center][1] + distance * math.sin(angle)
            self.positions[str(i)] = (x, y)

        for u in self.graph:
            for v in self.graph[u]:
                if u != v:
                    u_pos = self.positions[u]
                    v_pos = self.positions[v]
                    if self.euclidean_distance(u_pos, v_pos) < cluster_radius:
                        weight = self.graph[u][v]
                        self.graph[u][v] = weight