import random
import math
from typing import Dict, List, Tuple
from GraphGen.GraphPattern import GraphPattern


class ClusteredGraphPattern(GraphPattern):
    def __init__(self, inter_cluster_prob: float = 0.2):
        self.num_clusters = 3
        self.cluster_radius = 300
        self.inter_cluster_prob = inter_cluster_prob
        self.max_placement_attempts = 100

    def generate_graph(self, num_vertices: int, edge_probability: float,
                       min_weight: int, max_weight: int) -> Dict[str, Dict[str, int]]:
        # Динамическое определение количества кластеров
        self.num_clusters = max(2, int(math.sqrt(num_vertices)))

        # Автоматическая настройка радиуса кластера
        self.cluster_radius = self._calculate_base_radius(num_vertices)

        cluster_assignments = self.assign_clusters(num_vertices, self.num_clusters)
        graph = {str(i): {} for i in range(num_vertices)}

        edge_prob_inter = edge_probability * self.inter_cluster_prob

        # Оптимизированное создание рёбер
        for u in range(num_vertices):
            for v in range(u + 1, num_vertices):
                same_cluster = cluster_assignments[u] == cluster_assignments[v]
                prob = edge_probability if same_cluster else edge_prob_inter

                if random.random() <= prob:
                    weight = random.randint(min_weight, max_weight)
                    graph[str(u)][str(v)] = weight
                    graph[str(v)][str(u)] = weight

        self.cluster_assignments = cluster_assignments
        return graph

    def display_positions(self, canvas_width: float, canvas_height: float,
                          positions: List[str], min_distance: float = 30) -> Dict[str, Tuple[float, float]]:
        centers = self.generate_cluster_centers(canvas_width, canvas_height)
        cluster_assignments = self.cluster_assignments if hasattr(self, 'cluster_assignments') \
            else self.assign_clusters(len(positions), self.num_clusters)

        position_map = {}
        cluster_radius = self._calculate_display_radius(canvas_width, canvas_height)
        cluster_nodes = self._distribute_nodes_to_clusters(cluster_assignments)

        for cluster_id, nodes in cluster_nodes.items():
            cx, cy = centers[cluster_id]
            placed = []

            max_nodes = self._calculate_max_nodes(cluster_radius, min_distance)
            if len(nodes) > max_nodes:
                cluster_radius *= 1.2  # Автоматическое увеличение радиуса
                max_nodes = self._calculate_max_nodes(cluster_radius, min_distance)

            for node in nodes:
                x, y = self._place_node(cx, cy, cluster_radius, placed, min_distance)
                position_map[str(node)] = (x, y)
                placed.append((x, y))

        return position_map

    def _place_node(self, cx: float, cy: float, radius: float,
                    placed: List[Tuple[float, float]], min_dist: float) -> Tuple[float, float]:
        for _ in range(self.max_placement_attempts):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, radius)
            x = cx + distance * math.cos(angle)
            y = cy + distance * math.sin(angle)

            if not self._check_overlap(x, y, placed, min_dist):
                return (x, y)

        # Если не удалось разместить - возвращаем случайную позицию
        return (cx + random.uniform(-radius, radius),
                cy + random.uniform(-radius, radius))

    def _check_overlap(self, x: float, y: float,
                       placed: List[Tuple[float, float]], min_dist: float) -> bool:
        for (px, py) in placed:
            if math.hypot(x - px, y - py) < min_dist:
                return True
        return False

    def _calculate_base_radius(self, num_vertices: int) -> float:
        return 250 * math.sqrt(num_vertices / 50)

    def _calculate_display_radius(self, width: float, height: float) -> float:
        return min(width, height) / (self.num_clusters * 2)

    def _calculate_max_nodes(self, radius: float, min_dist: float) -> int:
        area = math.pi * radius ** 2
        node_area = math.pi * (min_dist / 2) ** 2
        return max(1, int(area / node_area))

    def _distribute_nodes_to_clusters(self, cluster_assignments: List[int]) -> Dict[int, List[int]]:
        clusters = {}
        for idx, cluster_id in enumerate(cluster_assignments):
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(idx)
        return clusters

    def generate_cluster_centers(self, width: float, height: float) -> List[Tuple[float, float]]:
        radius = min(width, height) * 0.35
        centers = []
        angle_step = 2 * math.pi / self.num_clusters

        for i in range(self.num_clusters):
            angle = i * angle_step + random.uniform(-0.1, 0.1)
            x = width / 2 + radius * math.cos(angle)
            y = height / 2 + radius * math.sin(angle)
            centers.append((x, y))

        return centers

    def assign_clusters(self, num_vertices: int, num_clusters: int) -> List[int]:
        base_size = num_vertices // num_clusters
        clusters = [base_size] * num_clusters

        # Распределение оставшихся вершин
        for i in range(num_vertices % num_clusters):
            clusters[i] += 1

        # Создание списка назначений
        cluster_assignments = []
        for cluster_id, size in enumerate(clusters):
            cluster_assignments.extend([cluster_id] * size)

        random.shuffle(cluster_assignments)
        return cluster_assignments