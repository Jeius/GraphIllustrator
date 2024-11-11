import sys
from PyQt5.QtWidgets import QApplication
from lib.load_icon import loadIcon
from lib.load_stylesheet import loadStylesheet
from ui.main_window import Ui_MainWindow


class MyApp():
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.resize(1420, 820)
        self.ui.setWindowTitle("Graph Illustrator by Julius Pahama")
        self.ui.setStyleSheet(loadStylesheet("style/globals.css"))
        self.ui.setWindowIcon(loadIcon("icon.webp"))
        self.ui.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyApp()
    
    app.exec_()