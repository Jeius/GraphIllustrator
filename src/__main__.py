import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

from .ui.main_window import Ui_MainWindow
from .model.graph import Graph

def loadIcon(path):
    if getattr(sys, 'frozen', False):  # PyInstaller bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level

    file_path = os.path.join(base_path, path)

    if not os.path.exists(file_path):
        print(f"Icon file not found: {file_path}")
        return QIcon()  # Return a default icon if not found

    return QIcon(file_path)

def loadStylesheet(path):
    if getattr(sys, 'frozen', False):  # PyInstaller bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level

    file_path = os.path.join(base_path, path)

    if not os.path.exists(file_path):
        print(f"Stylesheet file not found: {file_path}")
        return ""  # Return an empty string if the file is missing

    with open(file_path, "r") as file:
        stylesheet = file.read()

    return stylesheet

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(1420, 860)
        self.setStyleSheet(loadStylesheet("style/globals.css"))
        self.setWindowIcon(loadIcon("public/images/icon.webp"))

        self.graph = Graph()
        self.ui.view.setScene(self.graph)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec_())
