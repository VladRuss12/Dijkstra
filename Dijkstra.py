import heapq


class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

    def find_shortest_path(self, start, end):
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0

        previous_vertices = {vertex: None for vertex in self.graph}

        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_vertex == end:
                break

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current_vertex = end
        while current_vertex is not None:
            path.append(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        path.reverse()

        return distances[end], path
