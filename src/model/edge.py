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

        self.setFlag(QGraphicsLineItem.ItemIsSelectable, True)  
        self.setCursor(Qt.PointingHandCursor)  
        self.setPen(QPen(Qt.black, 2))   # Set the edge color and thickness
        self.setAcceptHoverEvents(True)
        self.setZValue(0)
        
        self.is_highlighted = False
        self.is_hovered = False
        self.is_curve = False
        
        self._updatePath()
        self._addLabel()
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

    def _addLabel(self):
        self.label = QGraphicsEllipseItem(0, 0, 30, 30, self)
        self.label.setBrush(QColor("#8f8f8f"))
        self.label.setPen(QColor("#8f8f8f"))

        self.label_text = QGraphicsTextItem(self.label)
        self.label_text.setFont(QFont("Inter", 11, QFont.Bold))

    def _addArrowHead(self):
        self.arrow_head = QGraphicsPolygonItem(self)
        self.arrow_head.setFlag(QGraphicsPolygonItem.ItemSendsGeometryChanges, True)
        self._updateArrowHead()

    def _updateArrowHead(self, arrow_size=7):
        brush = QBrush(Qt.black)
        pen = QPen(Qt.black)
        if self.isSelected() or self.is_hovered:
            brush = QBrush(Qt.white)
            pen = QPen(Qt.white)
        elif self.is_highlighted:
            brush = QBrush(QColor("#42ffd9"))
            pen = QPen(QColor("#42ffd9"))
        self.arrow_head.setBrush(brush)
        self.arrow_head.setPen(pen)
    
        path = self.path()
        p1 = path.elementAt(path.elementCount() - 1)  # Last point in the path
        p1 = QPointF(p1.x, p1.y)

        # Get the second-to-last point to compute direction (approximate tangent)
        if path.elementCount() > 1:
            p0 = path.elementAt(path.elementCount() - 2)
            p0 = QPointF(p0.x, p0.y)
        else:
            p0 = p1  # If there is no previous point, use p1 (this is a degenerate case)

        # Compute the direction vector (tangent) at the endpoint
        direction = p1 - p0
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5

        # Avoid division by zero
        if length == 0:
            return [p1, p1, p1]

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
        def shape_in_scene_coordinates(item: QGraphicsItem):
            local_shape = item.shape()
            scene_shape = QPainterPath()

            # Map each point in the local shape to scene coordinates
            for i in range(local_shape.elementCount()):
                element = local_shape.elementAt(i)
                scene_point = item.mapToScene(QPointF(element.x, element.y))
                if i == 0:
                    scene_shape.moveTo(scene_point)
                else:
                    scene_shape.lineTo(scene_point)
            return scene_shape

        def find_intersection(path_item, ellipse_item):
            path_shape_scene = shape_in_scene_coordinates(path_item)
            ellipse_shape_scene = shape_in_scene_coordinates(ellipse_item)

            # Find intersection between the two shapes in scene coordinates
            intersection_path = ellipse_shape_scene.intersected(path_shape_scene)

            if not intersection_path.isEmpty():
                return intersection_path.boundingRect().center()
            else:
                return None

        def createPath(start, end, control_point):
            path = QPainterPath()
            path.moveTo(start)
            if self.is_curve:
                path.quadTo(control_point, end)
            else:
                path.lineTo(end)
            return path

        start = self.start_vertex.getPosition()
        end = self.end_vertex.getPosition()
        control_point = self.getControlPoint()

        path = createPath(start, end, control_point)
        path_item = QGraphicsPathItem()
        path_item.setPath(path)

        # Calculate intersection points with the ellipse boundaries
        start = find_intersection(path_item, self.start_vertex)
        end = find_intersection(path_item, self.end_vertex)

        shorten_by = 10
        if self.is_curve:
            line_to_start = QLineF(control_point, start)
            line_to_end = QLineF(control_point, end)

            start = line_to_start.pointAt(1 - shorten_by / line_to_start.length())
            end = line_to_end.pointAt(1 - shorten_by / line_to_end.length())
        else:
            line = QLineF(start, end)
            start = line.pointAt(shorten_by / line.length())
            end = line.pointAt(1 - shorten_by / line.length())
        
        path = createPath(start, end, control_point)
        self.setPath(path)

    def _updateLabel(self):    
        self_center = self.boundingRect().center()
        label_text_center = self.label_text.boundingRect().center()
        label_center = self.label.rect().center()

        if self.weight != math.inf:
            self.label_text.setPlainText(str(self.weight))
            self.label.setVisible(True)
        else:
            self.label.setVisible(False)

        text_pos = QPointF(label_center - label_text_center)
        label_pos = QPointF(self_center - label_center)
        
        if self.is_curve:
            label_pos = QPointF(self.getControlPoint() - label_center)

        self.label_text.setPos(text_pos)
        self.label.setPos(label_pos)

    def getControlPoint(self, offset=60):
        # Get the line's endpoints
        p1 = self.start_vertex.getPosition()
        p2 = self.end_vertex.getPosition()

        # Calculate the direction of the line
        direction = QPointF(p1.x() - p2.x(), p1.y() - p2.y())

        # Normalize the direction
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5
        if length == 0:
            return  # Avoid division by zero if the points are the same
        direction /= length

        midpoint = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)

        # Get the perpendicular direction (90 degrees)
        perpendicular = QPointF(-direction.y(), direction.x())

        # Calculate the position for the label (60 pixels away)
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
            self.showContextMenu(event.pos())

        if event.button() == Qt.LeftButton:
            if self.graph.is_deleting: 
                self.graph.removeItem(self)
            elif self.graph.is_editing_weight:
                self.showEditDialog()
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        self.is_hovered = True
        return super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        return super().hoverLeaveEvent(event)
    
    def paint(self, painter, option, widget=None):
        self._updatePath()
        self._updateLabel()

        if self.graph.is_directed_graph:
            self._updateArrowHead()

        pen = QPen(Qt.black, 2)  # Default color and thickness

        # Check if the item is selected or highlighted
        if self.isSelected() or self.is_hovered:
            pen = QPen(Qt.white, 2)  # White color if selected
        elif self.is_highlighted:
            pen = QPen(QColor("#42ffd9"), 3)  # Custom color when highlighted

        painter.setPen(pen)
        painter.drawPath(self.path())