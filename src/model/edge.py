import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Edge(QGraphicsPathItem):
    from .vertex import Vertex

    def __init__(self, start: Vertex, end: Vertex, parent):
        super().__init__()

        from .graph import Graph
        self.start_vertex = start
        self.end_vertex = end
        self.weight = math.inf
        self.graph: Graph = parent
        self.label = Label(str(self.weight), self)

        self.setFlag(QGraphicsLineItem.ItemIsSelectable, True)  
        self.setCursor(Qt.PointingHandCursor)  
        self.setPen(QPen(Qt.black, 2))  
        self.setAcceptHoverEvents(True)
        self.setZValue(0)
        
        self.is_highlighted = False
        self.is_hovered = False
        self.is_curve = False
        
        self._updatePath()
        if self.graph.is_directed_graph:
            self._addArrowHead()



#------------------------- Local Functions ------------------------------------#
    def __eq__(self, other_edge):
        # Check if two edges are equal according to vertex order
        if isinstance(other_edge, Edge):
            if self.graph.is_directed_graph:
                return (self.start_vertex == other_edge.start_vertex and 
                        self.end_vertex == other_edge.end_vertex)
            else:
                return (self.start_vertex == other_edge.start_vertex and 
                        self.end_vertex == other_edge.end_vertex) or (
                        self.start_vertex == other_edge.end_vertex and 
                        self.end_vertex == other_edge.start_vertex
                        )

    def _addArrowHead(self):
        self.arrow_head = QGraphicsPolygonItem(self)
        self.arrow_head.setFlag(QGraphicsPolygonItem.ItemSendsGeometryChanges, True)
        self._updateArrowHead()

    def _updateArrowHead(self, arrow_size=7):
        path = self.path()
        p1 = path.elementAt(path.elementCount() - 1)  # Last point in the path
        p1 = QPointF(p1.x, p1.y)

        # Get the second-to-last point to compute direction (approximate tangent)
        if path.elementCount() > 1:
            p0 = path.elementAt(path.elementCount() - 2)
            p0 = QPointF(p0.x, p0.y)
        else:
            p0 = p1  

        # Compute the direction vector (tangent) at the endpoint
        direction = p1 - p0
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5

        # Avoid division by zero
        if length <= 1:
            arrow_head_polygon = QPolygonF([p1, p1, p1])
            self.arrow_head.setPolygon(arrow_head_polygon)
            return 

        # Normalize the direction vector
        dx = direction.x() / length
        dy = direction.y() / length

        # Calculate the points for the arrowhead
        p2 = QPointF(
            p1.x() + arrow_size * (-dx) - arrow_size * dy,
            p1.y() + arrow_size * (-dy) + arrow_size * dx
        )
        p3 = QPointF(
            p1.x() + arrow_size * (-dx) + arrow_size * dy,
            p1.y() + arrow_size * (-dy) - arrow_size * dx
        )

        arrow_head_polygon = QPolygonF([p1, p2, p3])
        self.arrow_head.setPolygon(arrow_head_polygon)
        
    def _updatePath(self):
        start = self.start_vertex.getPosition()
        end = self.end_vertex.getPosition()
        control_point = self.getControlPoint()

        if start == end:
            return

        # Define offset in pixels
        offset = (self.start_vertex.rect().width() / 2) + 3

        # Adjusted start and end points
        start_adjusted = self._shortenPoint(start, end, offset)
        end_adjusted = self._shortenPoint(end, start, offset)

        path = QPainterPath(start_adjusted)
        if self.is_curve:
            path.quadTo(control_point, end_adjusted)
        else:
            path.lineTo(end_adjusted)

        self.setPath(path)


    def _shortenPoint(self, start, end, offset):
        # Calculate direction vector
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        
        # Calculate the distance
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalize the vector and apply the offset
        if distance > 0:
            dx = dx / distance * offset
            dy = dy / distance * offset
        return QPointF(start.x() + dx, start.y() + dy)

    def _updateLabel(self):    
        self_center = self.path().pointAtPercent(0.5)
        label_center = self.label.rect().center()

        if self.weight != math.inf:
            self.label.setText(str(self.weight))
            self.label.setVisible(True)
        else:
            self.label.setVisible(False)

        self.label.setPos(QPointF(self_center - label_center))

    def getControlPoint(self, offset=60):
        # Get the line's endpoints
        p1 = self.start_vertex.getPosition()
        p2 = self.end_vertex.getPosition()

        # Calculate the direction of the line
        direction = QPointF(p1.x() - p2.x(), p1.y() - p2.y())

        # Normalize the direction
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5
        if length <= 1:
            return  # Avoid division by zero if the points are the same
        direction /= length

        midpoint = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)

        # Get the perpendicular direction (90 degrees)
        perpendicular = QPointF(-direction.y(), direction.x())

        # Set the control point perpendicular distance (60 pixels away)
        return midpoint + perpendicular * offset
    


#------------------------------- Getters -----------------------------------#
    def getOpposite(self, vertex):
        # Return the neighbor of the vertex
        if vertex == self.start_vertex:
            return self.end_vertex
        else:
            return self.start_vertex

    def getStart(self):
        return self.start_vertex


    def showContextMenu(self, pos):
        # Create a context menu
        menu = QMenu()

        edit_action = menu.addAction("Edit Weight")
        edit_action.triggered.connect(self.showEditDialog)

        # Show the menu at the mouse position
        global_pos = self.mapToScene(pos).toPoint()
        menu.exec_(self.scene().views()[0].mapToGlobal(global_pos))




#-------------------------- Setters -----------------------------------------------------------#
    def showEditDialog(self):
        input_dialog = QInputDialog()
        input_dialog.setWindowTitle("Edge")
        input_dialog.setLabelText("Enter the new weight:")

        # Remove the question mark by disabling the ContextHelpButtonHint flag
        input_dialog.setWindowFlags(input_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        if input_dialog.exec_() == QDialog.Accepted:
            weight = input_dialog.textValue()
            self.weight = int(weight) if weight.isdigit() and int(weight) >= 0 else math.inf
            self._updateLabel()
            self.graph.emitSignal()

    def setHighlight(self, flag):
        self.is_highlighted = flag
        self.update()

    def setCurved(self, flag):
        self.is_curve = flag

#---------------------- Event Listeners ---------------------------------------------#    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # self.showContextMenu(event.pos())
            pass

        if event.button() == Qt.LeftButton:
            if self.graph.is_deleting: 
                self.graph.removeItem(self)
            elif self.graph.is_editing_weight:
                self.showEditDialog()
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        self.is_hovered = True
        self.setZValue(1)
        return super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        self.setZValue(0)
        return super().hoverLeaveEvent(event)
    
    def paint(self, painter, option, widget=None):
        self._updatePath()
        self._updateLabel()
        self.label.setHighlight()

        if self.graph.is_directed_graph:
            self._updateArrowHead()

        pen = QPen(Qt.black, 2)  # Default color and thickness
        brush = QBrush(Qt.black)

        # Check if the item is selected or highlighted
        if self.isSelected() or self.is_hovered:
            pen = QPen(Qt.white, 2)  
            brush = QBrush(Qt.white)
            self.label.setHighlight(QColor("white"))
        elif self.is_highlighted:
            pen = QPen(QColor("#42ffd9"), 3)  # Custom color when highlighted
            brush = QBrush(QColor("#42ffd9"))
            self.label.setHighlight(QColor("#42ffd9"))

        
        self.arrow_head.setBrush(brush)
        self.arrow_head.setPen(pen)
        painter.setPen(pen)
        painter.drawPath(self.path())





class Label(QGraphicsEllipseItem):
    def __init__(self, text: str, parent: Edge = None):
        super().__init__(0, 0, 30, 30, parent)
        self.setCursor(Qt.PointingHandCursor)  
        self.setBrush(QColor("#8f8f8f"))
        self.setPen(QColor("#8f8f8f"))

        self.text = QGraphicsTextItem(text, self)
        self.text.setFont(QFont("Inter", 10, QFont.Bold))
        self.default_text_color = QColor("black")
        self._update_text_pos()

    def _update_text_pos(self):
        text_center = self.text.boundingRect().center()
        self_center = self.rect().center()
        self.text.setPos(QPointF(self_center - text_center))
    
    def setText(self, text: str):
        self.text.setPlainText(text)
        self._update_text_pos()
    
    def setHighlight(self, color: QColor = None):
        self.text.setDefaultTextColor(self.default_text_color)
        if color:
            self.text.setDefaultTextColor(color)