from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QWidget, QGraphicsLineItem

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
        from ..model.vertex import Vertex
        if event.button() == Qt.LeftButton: 
            click_position = event.pos()  
            scene_position = self.mapToScene(click_position)  

            if self.graph.is_adding_vertex:
                self.graph.createVertex(scene_position) 

        elif event.button() == Qt.RightButton:  
            self.graph.clearSelection()
            if self.graph.is_adding_edge:
               self.graph.indicator_line in self.graph.items() and \
                self.graph.removeItem(self.graph.indicator_line)

        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.graph.is_dragging:
            self.graph.indicator_line in self.graph.items() and \
                self.graph.removeItem(self.graph.indicator_line)
        
        if self.graph.is_adding_edge:
            # Calculate the new position based on the mouse event
            new_position = self.mapToScene(event.pos())
            scene = self.graph
            scene_width = scene.width()
            scene_height = scene.height()

            # Calculate the allowed x and y positions within the scene boundaries
            x_pos = max(0, min(new_position.x(), scene_width))
            y_pos = max(0, min(new_position.y(), scene_height))

            # Check if the new position is within the scene boundaries
            if 0 <= new_position.x() <= scene_width and 0 <= new_position.y() <= scene_height:
                # Update the position only if within bounds
                line = self.graph.indicator_line.line()
                line.setP2(QPointF(x_pos, y_pos))
                self.graph.indicator_line.setLine(line)
            else:
                # Do nothing to stop further dragging outside bounds
                return

        # Call the parent method to ensure other mouse move functionality is retained
        super().mouseMoveEvent(event)