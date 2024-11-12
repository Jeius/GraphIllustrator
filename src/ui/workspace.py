from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QWidget
from ..model.graph import Graph

class Workspace(QGraphicsView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)  
        

    def setScene(self, scene : Graph):
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