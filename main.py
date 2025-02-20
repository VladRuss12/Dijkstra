from Dijkstra import Dijkstra
from Graph import Graph
from GraphGUI import GraphGUI


class Main:
    def __init__(self):
        self.app = GraphGUI(Graph, Dijkstra)

    def run(self):
        self.app.mainloop()

# Запуск приложения через класс Main
if __name__ == "__main__":
    main_app = Main()
    main_app.run()
