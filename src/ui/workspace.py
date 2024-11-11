from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QWidget

class Workspace(QGraphicsView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setStyleSheet("background-color: #8f8f8f")
        self.setRenderHint(QPainter.Antialiasing)  