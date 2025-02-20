import tkinter as tk

class GraphGUI(tk.Tk):
    def __init__(self, graph_class, dijkstra_class):
        super().__init__()

        self.graph = None
        self.dijkstra = None
        self.graph_class = graph_class
        self.dijkstra_class = dijkstra_class

        self.title("Граф и Алгоритм Дейкстры")

        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canvas.pack()

        # Элементы управления
        self.create_widgets()

        # Список для хранения ссылок на подсвеченные линии
        self.highlighted_lines = []

    def create_widgets(self):
        self.num_vertices_label = tk.Label(self, text="Количество вершин:")
        self.num_vertices_label.pack()

        self.num_vertices_entry = tk.Entry(self)
        self.num_vertices_entry.pack()

        self.num_edges_label = tk.Label(self, text="Количество рёбер:")
        self.num_edges_label.pack()

        self.num_edges_entry = tk.Entry(self)
        self.num_edges_entry.pack()

        self.min_weight_label = tk.Label(self, text="Минимальный вес рёбер:")
        self.min_weight_label.pack()

        self.min_weight_entry = tk.Entry(self)
        self.min_weight_entry.pack()

        self.max_weight_label = tk.Label(self, text="Максимальный вес рёбер:")
        self.max_weight_label.pack()

        self.max_weight_entry = tk.Entry(self)
        self.max_weight_entry.pack()

        self.generate_button = tk.Button(self, text="Сгенерировать граф", command=self.generate_graph)
        self.generate_button.pack()

        self.start_label = tk.Label(self, text="Начальная вершина:")
        self.start_label.pack()

        self.start_entry = tk.Entry(self)
        self.start_entry.pack()

        self.end_label = tk.Label(self, text="Конечная вершина:")
        self.end_label.pack()

        self.end_entry = tk.Entry(self)
        self.end_entry.pack()

        self.find_path_button = tk.Button(self, text="Найти кратчайший путь", command=self.find_shortest_path)
        self.find_path_button.pack()

    def generate_graph(self):
        # Получение данных от пользователя
        try:
            num_vertices = int(self.num_vertices_entry.get())
            num_edges = int(self.num_edges_entry.get())
            min_weight = int(self.min_weight_entry.get())
            max_weight = int(self.max_weight_entry.get())
        except ValueError:
            return

        # Генерация графа
        self.graph = self.graph_class(num_vertices, 2, min_weight, max_weight)
        self.graph.generate_graph(num_edges)
        self.graph.display_positions(600, 600)

        self.dijkstra = self.dijkstra_class(self.graph.graph)

        # Очистка Canvas
        self.canvas.delete("all")

        # Отображение вершин и рёбер
        for vertex, (x, y) in self.graph.positions.items():
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
            self.canvas.create_text(x, y, text=vertex)

        for vertex, neighbors in self.graph.graph.items():
            x1, y1 = self.graph.positions[vertex]
            for neighbor, weight in neighbors.items():
                x2, y2 = self.graph.positions[neighbor]
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_text(mid_x, mid_y, text=str(weight), font=("Arial", 8))

    def find_shortest_path(self):
        # Очистка предыдущих подсвеченных рёбер
        for line in self.highlighted_lines:
            self.canvas.delete(line)
        self.highlighted_lines = []  # Очищаем список подсвеченных линий

        # Получение вершин для поиска пути
        start_vertex = self.start_entry.get()
        end_vertex = self.end_entry.get()

        if not self.graph or start_vertex not in self.graph.graph or end_vertex not in self.graph.graph:
            return

        # Находим кратчайший путь
        distance, path = self.dijkstra.find_shortest_path(start_vertex, end_vertex)

        # Отображаем путь на Canvas
        for i in range(len(path) - 1):
            start_pos = self.graph.positions[path[i]]
            end_pos = self.graph.positions[path[i + 1]]
            line = self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], fill="red", width=3)
            self.highlighted_lines.append(line)  # Добавляем линию в список

        print(f"Кратчайший путь от {start_vertex} до {end_vertex}: {path}")
        print(f"Длина пути: {distance}")
