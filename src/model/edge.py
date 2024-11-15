import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Edge(QGraphicsPathItem):
    from .vertex import Vertex

    COLORS = {
            "highlight": QColor("#42ffd9"),
            "default": QColor("black"),
            "selected": QColor("white"),
            "transparent": QColor("transparent")
        }
    
    def __init__(self, start: Vertex, end: Vertex, parent):
        super().__init__()

        from .graph import Graph
        self.start_vertex = start
        self.end_vertex = end
        self.weight = math.inf
        self.graph: Graph = parent
        self.default_pen = QPen(self.COLORS['default'], 2) 
        self.label = Label(str(self.weight), self)
        self.label.setZValue(2)

        self.setFlag(QGraphicsLineItem.ItemIsSelectable, True)  
        self.setCursor(Qt.PointingHandCursor)  
        self.setPen(self.default_pen)  
        self.setAcceptHoverEvents(True)
        self.setZValue(0)

        self.anim_path = QGraphicsPathItem(self)
        self.anim_path.setPen(QPen(self.COLORS['highlight'], 2))
        self.anim_path.setZValue(1)
        self.anim_path.hide()
        
        self.anim_start_pt = None
        self.anim_end_pt = None
        self.anim_duration = 1000
        self.timeline = QTimeLine(self.anim_duration, parent)
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.onFinish)

        self.is_highlighted = False
        self.is_hovered = False
        self.is_curve = False
        self.is_animating = False
        
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

        path = self.createPath(start, end, control_point)
        self.setPath(path)

    def createPath(self, start, end, control_point,):
        offset = (self.start_vertex.rect().width() / 2) + 3
        start_adjusted = self._shortenPoint(start, end, offset)
        end_adjusted = self._shortenPoint(end, start, offset)

        path = QPainterPath(start_adjusted)
        if self.is_curve:
            path.quadTo(control_point, end_adjusted)
        else:
            path.lineTo(end_adjusted)
        return path

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

    def setHighlight(self, is_highlight: bool):
        if is_highlight:
            self.default_pen = QPen(self.COLORS["highlight"], 2) 
            self.setZValue(1)
        else: 
            self.default_pen = QPen(self.COLORS["default"], 2)
            self.setZValue(0)

        self.setPen(self.default_pen)
        self.update()

    def setCurved(self, is_curve):
        self.is_curve = is_curve

    def setTransparent(self, is_transparent: bool):
        if is_transparent:
            self.default_pen = QPen(self.COLORS["transparent"], 2) 
            self.setZValue(1)
        else: 
            self.default_pen = QPen(self.COLORS["default"], 2)
            self.setZValue(0)

        self.setPen(self.default_pen)
        self.update()

    def on_selected(self):
        pen = QPen(self.COLORS["selected"], 2) 
        self.setPen(pen)

    def on_deselected(self):
        self.setPen(self.default_pen)
        


#---------------------- Event Listeners ---------------------------------------------#    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # self.showContextMenu(event.pos())
            pass

        if event.button() == Qt.LeftButton:
            if self.graph.is_deleting: 
                self.graph.removeEdge(self)
            elif self.graph.is_editing_weight:
                self.showEditDialog()
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        self.on_selected()
        self.setZValue(1)
        return super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        self.on_deselected()
        self.setZValue(0)
        return super().hoverLeaveEvent(event)
    
    def focusInEvent(self, event):
        self.on_selected()
        return super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        self.on_deselected()
        return super().focusOutEvent(event)

    
    def paint(self, painter, option, widget=None):
        self._updatePath()
        self._updateLabel()

        pen = self.pen()
        path = self.path()

        if self.graph.is_directed_graph:
            self._updateArrowHead()
            self.arrow_head.setBrush(pen.brush())
            self.arrow_head.setPen(pen)
        
        self.label.setHighlight(pen.color())
        painter.setPen(pen)
        painter.drawPath(path)
       
        

#----------------------- Animation ------------------------------------------------#
    def animate(self, progress: float):
        ctrl_point = self.getControlPoint()
        path = self.createPath(self.anim_start_pt, self.anim_end_pt, ctrl_point)

        dash_length = path.length() 
        dash_offset = dash_length * progress

        pen = self.anim_path.pen()
        pen.setDashPattern([dash_length, dash_length])
        pen.setDashOffset(dash_length- dash_offset)
        self.anim_path.setPen(pen)
        self.anim_path.setPath(path)

        if progress >= 0.5:
            self.setHighlight(True)

    def onFinish(self):
        self.anim_path.hide()
        self.setHighlight(True)

    def play(self, start: QPointF, end: QPointF):
        self.anim_path.show()
        self.anim_start_pt = start
        self.anim_end_pt = end
        self.timeline.start()

    def pause(self, is_paused: bool):
        self.timeline.setPaused(is_paused)

    def stop(self):
        self.is_animating = False
        self.timeline.stop()




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
    