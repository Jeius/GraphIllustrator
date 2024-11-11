from typing import List, Union
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPen, QColor, QBrush

class Vertex(QGraphicsEllipseItem):
    def __init__(self, id, x, y, width, height):
        from .edge import Edge
        self.edges: List[Edge] = []  # Stores the edges of this vertex
        self.is_moving = False  # Flag to track dragging state
        self.id = id  # Id for the label
        self.isHighlighted = False

        # Create a QGraphicsEllipseItem for the vertex
        super().__init__(x, y, width, height)

        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)  # Make the item movable
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)  # Allow the item to be selectable
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges, True)  # Notify of position changes
        self.setCursor(Qt.PointingHandCursor)  # Set cursor shape when hovering over the item
        self.setToolTip(f"Degree: {str(len(self.edges))}")  # Set the degree of this vertex as tooltip
        
        self.addLabel()     # Creates a text label inside the vertex

    def addLabel(self):
        # Create a QGraphicsTextItem for the label
        self.label = QGraphicsTextItem(str(self.id), self)
        font = QFont("Inter", 11, QFont.Bold)  # Set the font and size
        self.label.setFont(font)

        # Center the text within the ellipse
        rect = self.rect()
        text_rect = self.label.boundingRect()
        x = rect.width() / 2 - text_rect.width() / 2
        y = rect.height() / 2 - text_rect.height() / 2
        self.label.setPos(x, y)
    
    def getPosition(self):
        # Gets the position of the vertex in the scene
        return self.mapToScene(self.boundingRect().center())
    
    def addEdge(self, edge):
        # Add the new edge to the list of edges
        self.edges.append(edge)
        self.update() # Update the degree of the vertex

    def setHighlight(self, flag, colorIndex: Union[int, None]):
        colors = [QColor("#42ffd9"), QColor("#FF6E64")]
        self.isHighlighted = flag
        if flag and colorIndex is not None:
            self.highlightColor = colors[colorIndex]

    def update(self):
        self.setToolTip(f"Degree: {str(len(self.edges))}")
        self.addLabel()
        super().update()

    def paint(self, painter, option, widget=None):
        # This is an overriden paint to change the selection appearance of the vertex

        # Default pen and brush
        pen = QPen(Qt.black, 2)
        brush = QBrush(QColor("#3db93a"))

        # Check if the item is selected
        if self.isSelected():
            # Set the brush for the selected state
            brush = QBrush(QColor("#86f986"))  # Lightgreen fill
        else:
            if self.isHighlighted:
                brush = QBrush(self.highlightColor)

        # Apply the pen and brush
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(self.rect())
    
    def mousePressEvent(self, event):
        # Override the mousePressEvent to allow dragging of the vertex
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)  # Change cursor to closed hand when dragging
            self.is_moving = True   # Set the dragging flag to true
            self.mousePressPos = event.scenePos()  # Capture the initial mouse position
            self.itemPressPos = self.pos()  # Capture the initial position of the ellipse
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
         # Override the mouseMoveEvent to drag the vertex
        if self.is_moving:
            # Calculate the new position of the ellipse based on mouse movement
            new_position = self.itemPressPos + (event.scenePos() - self.mousePressPos)
            self.setPos(new_position) # Set the position of the vertex according to the new position
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.PointingHandCursor)  # Change cursor back to open hand after dragging
            self.is_moving = False  # Set the dragging flag to false
        super().mouseReleaseEvent(event)

    