import sys
from PySide6.QtWidgets import QApplication
from GUI.MainWindow import MainWindow  # Импортируем класс MainWindow, предполагая, что он в файле MainWindow.py

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем приложение
    main_window = MainWindow()  # Создаем окно приложения
    main_window.show()  # Показываем окно

    sys.exit(app.exec())  # Запускаем главный цикл обработки событий