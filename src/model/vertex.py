import string
from typing import List, Union
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsSceneMouseEvent
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPen, QColor, QBrush

class Vertex(QGraphicsEllipseItem):
    def __init__(self, id_index: int, diameter, parent):
        super().__init__(0, 0, diameter, diameter)

        from .edge import Edge
        from .graph import Graph
        self.edges: List[Edge] = []  # Stores the edges of this vertex
        self.id_index = id_index
        self.graph: Graph = parent
        
        self.setFlag(Vertex.ItemIsMovable, True)  # Make the item movable
        self.setFlag(Vertex.ItemIsSelectable, True)  # Allow the item to be selectable
        self.setFlag(Vertex.ItemSendsGeometryChanges, True)  # Notify of position changes
        self.setCursor(Qt.PointingHandCursor)  # Set cursor shape when hovering over the item
        self.setToolTip(f"Degree: {str(len(self.edges))}")
        self.setAcceptHoverEvents(True)
        self.setZValue(1)

        self.is_moving = False  # Flag to track dragging state
        self.is_highlighted = False
        self.is_hovered = False
        
        self.uppercase_alphabets = list(string.ascii_uppercase)
        self.id = self.createId(id_index)

        self.label = QGraphicsTextItem(self.id[1], self)
        font = QFont("Inter", 11, QFont.Bold) 
        self.label.setFont(font)  

        self.colors = {
            "route": QColor("#42ffd9"),
            "end": QColor("#FF6E64"),
            "start": QColor("#86f986")
        }

        self.graph.graphChanged.connect(self.updateLabel)

    def updateLabel(self):
        new_id = self.createId(self.id_index)

        if self.id != new_id:
            self.id = new_id
            self.label.setPlainText(self.id[1])
            self.graph.emitSignal()

        self_center = self.rect().center()
        text_center = self.label.boundingRect().center()
        center = QPointF(self_center - text_center)
        self.label.setPos(center)
        
    def getPosition(self):
        # Gets the position of the vertex in the scene
        return self.mapToScene(self.boundingRect().center())
    
    def addEdge(self, edge):
        self.edges.append(edge)

    def clearEdges(self):
        self.edges.clear()

    def setHighlight(self, is_highlight: bool, colorType:str = None):
        self.is_highlighted = is_highlight
        if is_highlight and colorType is not None:
            self.highlightColor = self.colors[colorType]

        self.update()

    def createId(self, index: int):
        if self.graph.is_id_int:
            return (index, str(index + 1))
        else:
            return (index, self.uppercase_alphabets[index])
    

#---------------------- Event Listeners ---------------------------------------------#    
    def mousePressEvent(self, event):
        # Override the mousePressEvent to allow dragging of the vertex
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)  # Change cursor to closed hand when dragging
            self.is_moving = True   # Set the dragging flag to true
            self.mousePressPos = event.scenePos()  # Capture the initial mouse position
            self.itemPressPos = self.pos()  # Capture the initial position of the ellipse

            if self.graph.is_deleting: 
                self.graph.removeItem(self)

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
         # Override the mouseMoveEvent to drag the vertex
        if self.is_moving:
            # Get the bounding rect of the item and the scene's width and height
            item_rect = self.boundingRect()
            scene = self.scene()
            scene_width = scene.width()
            scene_height = scene.height()

            # Constrain the item's position within the scene boundaries
            x_pos = self.x()
            y_pos = self.y()

            if x_pos < 0:
                self.setPos(0, y_pos)
            elif x_pos + item_rect.right() > scene_width:
                self.setPos(scene_width - item_rect.width(), y_pos)

            if y_pos < 0:
                self.setPos(x_pos, 0)
            elif y_pos + item_rect.bottom() > scene_height:
                self.setPos(x_pos, scene_height - item_rect.height())
            
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Change cursor back to open hand after dragging
            self.setCursor(Qt.PointingHandCursor)  
            # Set the dragging flag to false
            self.is_moving = False  
        return super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        degree = len(self.edges)
        self.setToolTip(f"Degree: {str(degree)}")
        self.is_hovered = True
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        return super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
            # This is an overriden paint to change the selection appearance of the vertex
            self.updateLabel()
            # Default pen and brush
            pen = QPen(Qt.black, 2)
            brush = QBrush(QColor("#275aa1"))

            # Check if the item is selected
            if self.isSelected() or self.is_hovered:
                # Set the brush for the selected state
                brush = QBrush(QColor("#92b6e7"))  # Lightgreen fill
            else:
                if self.is_highlighted:
                    brush = QBrush(self.highlightColor)

            # Apply the pen and brush
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(self.rect())