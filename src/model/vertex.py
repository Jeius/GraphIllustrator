import string
from typing import List
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPen, QColor, QBrush

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.model import Graph, Edge

class Vertex(QGraphicsEllipseItem):
    def __init__(self, id_index: int, diameter, parent: 'Graph'):
        super().__init__(0, 0, diameter, diameter)
        self.edges: List['Edge'] = []  # Stores the edges of this vertex
        self.id_index = id_index
        self.graph = parent
        
        self.setFlag(Vertex.ItemIsMovable, True)  # Make the item movable
        self.setFlag(Vertex.ItemIsSelectable, True)  # Allow the item to be selectable
        self.setFlag(Vertex.ItemSendsGeometryChanges, True)  # Notify of position changes
        self.setCursor(Qt.PointingHandCursor)  # Set cursor shape when hovering over the item
        self.setToolTip(f"Degree: {str(len(self.edges))}")
        self.setAcceptHoverEvents(True)
        self.setZValue(5)

        self.is_moving = False  # Flag to track dragging state
        self.is_highlighted = False
        self.is_hovered = False
        
        self.uppercase_alphabets = list(string.ascii_uppercase)
        self.id = self.createId(id_index)

        self.label = QGraphicsTextItem(self.id[1], self)
        font = QFont("Inter", 11, QFont.Bold) 
        self.label.setFont(font)  

        self.highlight_colors = {
            "default": QColor("#42ffd9"),
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

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def clearEdges(self):
        self.edges.clear()

    def setHighlight(self, is_highlight: bool, colorType:str = None):
        self.is_highlighted = is_highlight
        if is_highlight:
            if colorType == None:
                self.highlightColor = self.highlight_colors["default"]
                return
            self.highlightColor = self.highlight_colors[colorType]

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
            self.graph.is_dragging = True
            self.mousePressPos = event.scenePos()  # Capture the initial mouse position
            self.itemPressPos = self.pos()  # Capture the initial position of the ellipse

            if self.graph.is_deleting: 
                self.graph.removeVertex(self)

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Set a high z-index for visibility while dragging
        self.setZValue(6)

        if self.is_moving:
            # Calculate the new position based on the mouse event
            new_position = self.mapToScene(event.pos())
            item_rect = self.boundingRect()
            scene = self.scene()
            scene_width = scene.width()
            scene_height = scene.height()

            # Calculate the allowed x and y positions within the scene boundaries
            x_pos = max(0, min(new_position.x(), scene_width - item_rect.width()))
            y_pos = max(0, min(new_position.y(), scene_height - item_rect.height()))

            # Check if the new position is within the scene boundaries
            if 0 <= new_position.x() <= scene_width - item_rect.width() and \
            0 <= new_position.y() <= scene_height - item_rect.height():
                # Update the position only if within bounds
                self.setPos(x_pos - item_rect.width() / 2, y_pos - item_rect.height() / 2)
                self.setSelected(False)
            else:
                # Do nothing to stop further dragging outside bounds
                return

        # Call the parent method to ensure other mouse move functionality is retained
        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        self.setZValue(5)
        if event.button() == Qt.LeftButton:
            # Change cursor back to open hand after dragging
            self.setCursor(Qt.PointingHandCursor)  
            # Set the dragging flag to false
            self.is_moving = False  
            self.graph.is_dragging = False
        return super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        degree = len(self.edges)
        self.setToolTip(f"Degree: {str(degree)}")
        self.is_hovered = True
        self.setZValue(6)
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        self.setZValue(5)
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