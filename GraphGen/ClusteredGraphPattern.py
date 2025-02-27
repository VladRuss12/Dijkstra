import random
import math
import numpy as np
from GraphGen.GraphPattern import GraphPattern

class ClusteredGraphPattern(GraphPattern):
    def generate_graph(self, num_vertices, num_edges):
        graph = {str(i): {} for i in range(num_vertices)}
        for _ in range(num_edges):
            u = random.choice(list(graph.keys()))
            v = random.choice(list(graph.keys()))

            if u == v:
                continue  # Не добавляем рёбра от вершины к самой себе

            # Снижаем вероятность рёбер между кластерами
            if random.random() > 0.2:  # 30% вероятность создания рёбер между кластерами
                continue

            weight = random.randint(1, 10)
            graph[u][v] = weight
            graph[v][u] = weight  # Для неориентированного графа

        return graph

    def display_positions(self, canvas_width, canvas_height, positions):
        k = 3  # Количество кластеров
        positions = np.array(
            [[random.uniform(0, canvas_width), random.uniform(0, canvas_height)] for _ in range(len(positions))])
        centers = self.kmeans(positions, k)

        cluster_radius = 150  # Увеличиваем радиус кластера для уменьшения перекрытия узлов
        position_map = {}

        for i in range(len(positions)):
            closest_center = min(range(k), key=lambda j: self.euclidean_distance(positions[i], centers[j]))
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, cluster_radius)
            x = centers[closest_center][0] + distance * math.cos(angle)
            y = centers[closest_center][1] + distance * math.sin(angle)
            position_map[str(i)] = (x, y)

        return position_map

    def kmeans(self, positions, k, max_iter=100):
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

    def euclidean_distance(self, p1, p2):
        """Вычисляем евклидово расстояние между двумя точками (p1 и p2)"""
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
