from GraphGen.GraphPattern import GraphPattern
class Graph:
    def __init__(self, num_vertices, min_weight, max_weight, pattern: GraphPattern, edge_probability):
        self.num_vertices = num_vertices
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.pattern = pattern
        self.edge_probability = edge_probability  # Вероятность ребра между вершинами
        self.graph = {}
        self.positions = {}

    def generate_graph(self):
        # Используем паттерн для генерации графа, передаём только кол-во вершин и вероятность
        self.graph = self.pattern.generate_graph(self.num_vertices, self.edge_probability,  self.min_weight,  self.max_weight)

    def display_positions(self, canvas_width, canvas_height):
        if not hasattr(self, 'positions') or len(self.positions) == 0:
            self.positions = self.pattern.display_positions(
                canvas_width,
                canvas_height,
                [str(i) for i in range(self.num_vertices)]
            )
        self.positions = self.pattern.display_positions(canvas_width, canvas_height, self.graph)

    def get_graph(self):
        return self.graph

    def get_positions(self):
        return self.positions

    @property
    def is_generated(self):
        return bool(self.graph) and bool(self.positions)