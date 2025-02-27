from GraphGen.GraphPattern import GraphPattern
class Graph:
    def __init__(self, num_vertices, graph_type, min_weight, max_weight, pattern: GraphPattern):
        self.num_vertices = num_vertices
        self.graph_type = graph_type
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.pattern = pattern
        self.graph = {}
        self.positions = {}

    def generate_graph(self, num_edges):
        self.graph = self.pattern.generate_graph(self.num_vertices, num_edges)

    def display_positions(self, canvas_width, canvas_height):
        self.positions = self.pattern.display_positions(canvas_width, canvas_height, self.graph)

    def get_graph(self):
        return self.graph

    def get_positions(self):
        return self.positions
