from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QWidget

from ..model.graph import Graph
from ..ui.tool import Ui_Tool

class Workspace(QGraphicsView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)  

        self.tool = Ui_Tool(self)
        self.tool.move(0,0)
        self.tool.done_button.hide()
        self.tool.revert_button.hide()
        self.tool.setStyleSheet("background-color: transparent;")
        self.tool.done_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.tool.revert_button.setStyleSheet("""
            QPushButton {
                background-color: #545457;
                color: white;
                padding: 8px 24px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #70707c;
            }
        """)
        

    def setScene(self, scene: Graph):
        self.graph = scene
        self.graph.setSceneRect(0, 0, 1280, 840)
        return super().setScene(scene)
    
    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing, True)
        return super().paintEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.graph.is_adding_vertex: 
            click_position = event.pos()  
            scene_position = self.mapToScene(click_position)  
            
            self.graph.createVertex(scene_position) 
        elif event.button() == Qt.RightButton:  
            self.graph.clearSelection()

        return super().mousePressEvent(event)