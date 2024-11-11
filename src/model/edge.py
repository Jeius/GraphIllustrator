import math
from PyQt5 import QtCore, QtGui, QtWidgets

class Edge(QtWidgets.QGraphicsPathItem):
    from .vertex import Vertex

    def __init__(self, start: Vertex, end: Vertex):
        super().__init__()
        self.start_vertex = start
        self.end_vertex = end
        self.weight = math.inf
        self.isHighlighted = False
        self.isCurve = False

        self.setFlag(QtWidgets.QGraphicsLineItem.ItemIsSelectable, True)  
        self.setCursor(QtCore.Qt.PointingHandCursor)  
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2))   # Set the edge color and thickness
        self._updatePath()
        self._addLabel()
        self._addArrowHead()

    def __eq__(self, other_edge):
        # Check if two edges are equal according to vertex order
        if isinstance(other_edge, Edge):
            return (self.start_vertex == other_edge.start_vertex and self.end_vertex == other_edge.end_vertex)

    def getOpposite(self, vertex):
        # Return the neighbor of the vertex
        if vertex == self.start_vertex:
            return self.end_vertex
        else:
            return self.start_vertex

    def getStart(self):
        return self.start_vertex

    def paint(self, painter, option, widget=None):
        self._updatePath()
        self._updateLabel(self.weightLabel)
        self._updateArrowHead()
        pen = QtGui.QPen(QtCore.Qt.black, 2)  # Default color and thickness

        # Check if the item is selected or highlighted
        if self.isSelected():
            pen = QtGui.QPen(QtCore.Qt.white, 2)  # White color if selected
        elif self.isHighlighted:
            pen = QtGui.QPen(QtGui.QColor("#42ffd9"), 4)  # Custom color when highlighted

        painter.setPen(pen)
        painter.drawPath(self.path())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.showContextMenu(event.pos())
        super().mousePressEvent(event)

    def showContextMenu(self, pos):
        # Create a context menu
        menu = QtWidgets.QMenu()

        edit_action = menu.addAction("Edit Weight")
        edit_action.triggered.connect(self.editWeight)

        # Show the menu at the mouse position
        global_pos = self.mapToScene(pos).toPoint()
        menu.exec_(self.scene().views()[0].mapToGlobal(global_pos))

    def editWeight(self):
        input_dialog = QtWidgets.QInputDialog()
        input_dialog.setWindowTitle("Edge")
        input_dialog.setLabelText("Enter the new weight:")

        # Remove the question mark by disabling the ContextHelpButtonHint flag
        input_dialog.setWindowFlags(input_dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        if input_dialog.exec_() == QtWidgets.QDialog.Accepted:
            weight = input_dialog.textValue()
            self.weight = int(weight) if weight.isdigit() and int(weight) >= 0 else math.inf
            self._addLabel()

    def _addLabel(self):
        self.weightLabel = QtWidgets.QGraphicsTextItem(self)
        self.weightLabel.setFont(QtGui.QFont("Inter", 11, QtGui.QFont.Bold))
        self.weightLabel.adjustSize()  # Adjust size to fit the text
       
        if self.weight != math.inf:
            self.weightLabel.setPlainText(str(self.weight))
            self._updateLabel(self.weightLabel)
            self.weightLabel.setVisible(True)
        else:
            self.weightLabel.setVisible(False)

    def _addArrowHead(self):
        self.arrow_head = QtWidgets.QGraphicsPolygonItem(self)
        self.arrow_head.setFlag(QtWidgets.QGraphicsPolygonItem.ItemSendsGeometryChanges, True)
        self._updateArrowHead()

    def _updateArrowHead(self, arrow_size=7):
        brush = QtGui.QBrush(QtCore.Qt.black)
        pen = QtGui.QPen(QtCore.Qt.black)
        if self.isSelected():
            brush = QtGui.QBrush(QtCore.Qt.white)
            pen = QtGui.QPen(QtCore.Qt.white)
        elif self.isHighlighted:
            brush = QtGui.QBrush(QtGui.QColor("#42ffd9"))
            pen = QtGui.QPen(QtGui.QColor("#42ffd9"))
        self.arrow_head.setBrush(brush)
        self.arrow_head.setPen(pen)
    
        path = self.path()
        p1 = path.elementAt(path.elementCount() - 1)  # Last point in the path
        p1 = QtCore.QPointF(p1.x, p1.y)

        # Get the second-to-last point to compute direction (approximate tangent)
        if path.elementCount() > 1:
            p0 = path.elementAt(path.elementCount() - 2)
            p0 = QtCore.QPointF(p0.x, p0.y)
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
        p2 = QtCore.QPointF(
            p1.x() + arrow_size * (-dx) - arrow_size * dy,
            p1.y() + arrow_size * (-dy) + arrow_size * dx
        )
        p3 = QtCore.QPointF(
            p1.x() + arrow_size * (-dx) + arrow_size * dy,
            p1.y() + arrow_size * (-dy) - arrow_size * dx
        )

        arrow_head_polygon = QtGui.QPolygonF([p1, p2, p3])
        self.arrow_head.setPolygon(arrow_head_polygon)
        
    def _updatePath(self):
        def shape_in_scene_coordinates(item: QtWidgets.QGraphicsItem):
            local_shape = item.shape()
            scene_shape = QtGui.QPainterPath()

            # Map each point in the local shape to scene coordinates
            for i in range(local_shape.elementCount()):
                element = local_shape.elementAt(i)
                scene_point = item.mapToScene(QtCore.QPointF(element.x, element.y))
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
            path = QtGui.QPainterPath()
            path.moveTo(start)
            if self.isCurve:
                path.quadTo(control_point, end)
            else:
                path.lineTo(end)
            return path

        start = self.start_vertex.getPosition()
        end = self.end_vertex.getPosition()
        control_point = self.getControlPoint()

        path = createPath(start, end, control_point)
        path_item = QtWidgets.QGraphicsPathItem()
        path_item.setPath(path)

        # Calculate intersection points with the ellipse boundaries
        start = find_intersection(path_item, self.start_vertex)
        end = find_intersection(path_item, self.end_vertex)

        shorten_by = 10
        if self.isCurve:
            line_to_start = QtCore.QLineF(control_point, start)
            line_to_end = QtCore.QLineF(control_point, end)

            start = line_to_start.pointAt(1 - shorten_by / line_to_start.length())
            end = line_to_end.pointAt(1 - shorten_by / line_to_end.length())
        else:
            line = QtCore.QLineF(start, end)
            start = line.pointAt(shorten_by / line.length())
            end = line.pointAt(1 - shorten_by / line.length())
        
        path = createPath(start, end, control_point)
        self.setPath(path)

    def _updateLabel(self, label: QtWidgets.QGraphicsTextItem):
        label_position = None
        if self.isCurve:
            label_position = self.getControlPoint()
        else: 
            label_position = self.getControlPoint(15)
        center = QtCore.QPointF(label_position - label.boundingRect().center())
        label.setPos(center)

    def getControlPoint(self, offset=60):
        # Get the line's endpoints
        p1 = self.start_vertex.getPosition()
        p2 = self.end_vertex.getPosition()

        # Calculate the direction of the line
        direction = QtCore.QPointF(p1.x() - p2.x(), p1.y() - p2.y())

        # Normalize the direction
        length = (direction.x() ** 2 + direction.y() ** 2) ** 0.5
        if length == 0:
            return  # Avoid division by zero if the points are the same
        direction /= length

        midpoint = QtCore.QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)

        # Get the perpendicular direction (90 degrees)
        perpendicular = QtCore.QPointF(-direction.y(), direction.x())

        # Calculate the position for the label (60 pixels away)
        return midpoint + perpendicular * offset
        
    def setHighlight(self, flag):
        self.isHighlighted = flag

    def setCurved(self, flag):
        self.isCurve = flag

    def update(self):
        self._addLabel()
        self._addArrowHead()
        self._updatePath()
        super().update()


        