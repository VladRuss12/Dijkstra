from abc import ABC, abstractmethod


# Абстрактный класс для генерации графа
class GraphPattern(ABC):
    @abstractmethod
    def generate_graph(self, num_vertices, max_weight, min_weight, edge_probability):
        pass

    @abstractmethod
    def display_positions(self, canvas_width, canvas_height, positions):
        pass