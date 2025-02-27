from abc import ABC, abstractmethod


# Абстрактный класс для генерации графа
class GraphPattern(ABC):
    @abstractmethod
    def generate_graph(self, num_vertices, num_edges):
        pass

    @abstractmethod
    def display_positions(self, canvas_width, canvas_height, positions):
        pass