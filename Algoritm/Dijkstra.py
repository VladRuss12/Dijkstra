import heapq
from typing import Dict, Tuple, List, Optional


class Dijkstra:
    @staticmethod
    def find_shortest_path(graph: Dict[str, Dict[str, int]],
                           start: str,
                           end: str) -> Tuple[Optional[List[str]], int]:
        distances = {node: float('inf') for node in graph}
        previous = {node: None for node in graph}
        distances[start] = 0

        priority_queue = [(0, start)]

        while priority_queue:
            current_dist, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                break

            if current_dist > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node].items():
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        if distances[end] == float('inf'):
            return None, -1

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]

        return path[::-1], distances[end]