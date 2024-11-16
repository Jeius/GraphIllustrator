import math
import string
from typing import List
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen



from ..commands.model import Command

from .vertex import Vertex
from .edge import Edge
from ..algorithm.djisktra import Djisktra
from ..algorithm.floyd import FloydWarshall

class Graph(QGraphicsScene):
    DIAMETER = 30
    graphChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        from .complement import ComplementGraph
        from .mcst import MinimumCostSpanningTree

        self.selected_vertices: List[Vertex] = []   # List of the selected vertices
        self.adjacencyMatrix: list[list[float]] = []     # Adjacency matrix
        
        self.dijkstra = Djisktra()
        self.floyd = FloydWarshall()
        self.indicator_line = QGraphicsLineItem()
        self.indicator_line.setPen(QPen(Qt.black, 2))
        self.complement_graph = ComplementGraph(self)
        self.mcst_graph = MinimumCostSpanningTree(self)

        self.is_adding_vertex = False 
        self.is_adding_edge = False   
        self.is_using_dijkstra = True 
        self.is_using_floyd = False     
        self.is_using_prim = True
        self.is_using_kruskal = False
        self.is_directed_graph = True
        self.is_deleting = False
        self.is_editing_weight = False
        self.is_id_int = True
        self.is_setting_up = True
        self.mcst_total_cost: int = None
        self.is_dragging = False

        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []

        self.selectionChanged.connect(self.onSelectionChanged)


#------------------------------ Creators ----------------------------------------------------------#
    def createVertex(self, position: QPointF):
        diameter = self.DIAMETER
        id = self.genIdIndex()  
        vertex = Vertex(id, diameter, self)
        radius = diameter / 2
        adjusted_position = QPointF(position.x() - radius, position.y() - radius)
        vertex.setPos(adjusted_position)

        from ..commands.vertex import AddVertexCommand
        command = AddVertexCommand(self, vertex)
        self.perform_action(command)
    
    def createAdjMatrix(self):
        vertices = self.getVertices()
        # Terminate the execution if there are no vertices
        
        if not self.getEdges():
            self.adjacencyMatrix.clear()
            return

        n = len(vertices)
        # Intiallize matrix with infinities
        self.adjacencyMatrix = [[math.inf for _ in range(n)] for _ in range(n)]  

        for vertex in vertices:
            for edge in vertex.edges:
                if vertex == edge.getStart():
                    start_index = vertices.index(vertex)
                    end_index = vertices.index(edge.getOpposite(vertex))
                    
                    if edge.weight != math.inf:
                        if self.is_directed_graph:
                            self.adjacencyMatrix[start_index][end_index] = edge.weight
                        else:
                            self.adjacencyMatrix[start_index][end_index] = edge.weight
                            self.adjacencyMatrix[end_index][start_index] = edge.weight
            
                    self.adjacencyMatrix[start_index][start_index] = 0
                    self.adjacencyMatrix[end_index][end_index] = 0               

    def createEdge(self,):
        line = self.indicator_line.line()
        selected_vertex = next((vertex for vertex in self.selectedItems() if isinstance(vertex, Vertex)), None)
        if not selected_vertex:
            self.selected_vertices.clear()
            if self.indicator_line in self.items():
                self.removeItem(self.indicator_line)
            return
        
        if self.indicator_line not in self.items():
            self.addItem(self.indicator_line)

        if not self.selected_vertices:
            self.selected_vertices.append(selected_vertex)
            line.setP1(selected_vertex.getPosition())
            line.setP2(selected_vertex.getPosition())
            self.indicator_line.setLine(line)
        else:
            start = self.selected_vertices.pop()
            end = selected_vertex
            
            line.setP1(end.getPosition())
            self.indicator_line.setLine(line)

            edge = Edge(start, end, self)
            duplicate_edge = self.getDuplicate(edge)
            if duplicate_edge:
                self.clearSelection()
                return

            from ..commands.edge import AddEdgeCommand
            command = AddEdgeCommand(self, edge)
            self.perform_action(command)
            self.selected_vertices.append(end) 
                    
    def genIdIndex(self):
        index = 0
        vertices = self.getVertices()

        if len(vertices) != 0:
            index = vertices[-1].id_index + 1

        return index


                
#--------------------------- Setters ------------------------------------------#
    def setHighlightItems(self, highlighting: bool, colorType:str = None):
        for edge in self.getEdges():
            edge.setHighlight(highlighting)
        for vertex in self.getVertices():
            vertex.setHighlight(highlighting, colorType)

    def setDirectedGraph(self, is_directed: bool):
        self.is_directed_graph = is_directed
        self.emitSignal()

    def setCurvedEdge(self, edge:Edge):
        start = edge.getStart()
        end = edge.getOpposite(start)
        opposite_edge = Edge(end, start, self)
        duplicate_edge = self.getDuplicate(opposite_edge)

        if duplicate_edge:
            edge.setCurved(True)
            duplicate_edge.setCurved(True)
        else:
            edge.setCurved(False) 

    def setFloyd(self, is_floyd: bool):
        self.resetPaths()
        self.clearSelection()
        self.setHighlightItems(False)
        self.is_using_floyd = is_floyd
        self.emitSignal()

    def setDijkstra(self, is_dijkstra: bool):
        self.dijkstra.reset()
        self.clearSelection()
        self.setHighlightItems(False)
        self.is_using_dijkstra = is_dijkstra
        self.emitSignal()

    def setPrim(self, is_prim: bool):
        self.is_using_prim = is_prim
        self.emitSignal()

    def setKruskal(self, is_kruskal: bool):
        self.is_using_kruskal = is_kruskal
        self.emitSignal()



#--------------------------- Getters ------------------------------------------#
    def getVertices(self):
        items = self.items()
        vertices = [item for item in items if isinstance(item, Vertex)]
        vertices.reverse()
        vertices.sort(key=lambda vertex: vertex.id[0])
        return vertices
    
    def getEdges(self):
        items = self.items()
        edges = [item for item in items if isinstance(item, Edge)]
        edges.reverse()
        return edges
    
    def getComplement(self, is_complement):
        if is_complement:
            self.complement_graph.show()
        else:
            self.complement_graph.revert()
        self.undo_stack.clear()
        self.emitSignal()

    def getDuplicate(self, new_edge: Edge):
        edges = self.getEdges()
        for edge in edges:
            if new_edge == edge:
                return edge 
    



#--------------------------- Delete ---------------------------------------------#
    def removeVertex(self, vertex: Vertex):
        self.resetPaths()
        from ..commands.vertex import DeleteVertexCommand
        command = DeleteVertexCommand(self, vertex)
        self.perform_action(command)

    def removeEdge(self, edge: Edge):
        self.resetPaths()
        from ..commands.edge import DeleteEdgeCommand
        command = DeleteEdgeCommand(self, edge)
        self.perform_action(command)

    def revert(self):
        self.setHighlightItems(False)
        self.mcst_total_cost = None
        self.emitSignal()

    def clear(self):
        confirmation = self._showConfirmDialog("Confirm Clear", "This action is irreversable, do you want to proceed?")
        if confirmation == QMessageBox.Yes:
            self.resetPaths()
            self.undo_stack.clear()
            super().clear()
            self.emitSignal()
        
    def clearEdges(self):
        self.resetPaths()
        from ..commands.edge import ClearEdgesCommand
        edges = self.getEdges()
        command = ClearEdgesCommand(self, edges)
        self.perform_action(command)




#----------------------------- Algorithms -------------------------------------------#
    def findPath(self):
        try:
            self.undo_stack.clear()
            
            matrix = self.adjacencyMatrix

            if self.is_using_floyd:
                self.floyd.findPath(matrix)
                self.clearSelection()

            elif self.is_using_dijkstra:
                vertices = self.getVertices()
                selected_vertex = next((vertex for vertex in self.selectedItems() if isinstance(vertex, Vertex)), None)

                if not selected_vertex:
                    raise Exception("No starting vertex selected")
                
                start_index = vertices.index(selected_vertex)
                self.dijkstra.findPath(matrix, start_index)
                
        except Exception as e:
            self._showErrorDialog("Invalid Action", str(e))

    def findMCST(self, is_finding_mcst):
        self.undo_stack.clear()
        if is_finding_mcst:
            self.mcst_graph.show()
        else:
            self.mcst_graph.revert()
        self.emitSignal()
        



#----------------------------- Local Functions --------------------------------------#
    def _showErrorDialog(self, title: str, message: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def _showConfirmDialog(self, title: str, message: str):
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Warning)
        confirm_box.setWindowTitle(title)
        confirm_box.setText(message)
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        return confirm_box.exec_()

    def showPath(self, start:Vertex = None, goal:Vertex = None):
        # Ensure start and goal are valid
        if not start or not goal:
            return
        
        # Unhighlight all items first
        self.setHighlightItems(False)
        self.clearSelection()

        vertices = self.getVertices()

        # Get paths based on algorithm choice
        if self.is_using_floyd:
            paths = self.floyd.paths
        elif self.is_using_dijkstra:
            paths = self.dijkstra.paths

        if not paths:
            return

        # Retrieve path from start to goal
        if self.is_using_floyd:
            path = list(paths[(vertices.index(start), vertices.index(goal))])
        elif self.is_using_dijkstra:
            path = list(paths[vertices.index(goal)])

        path_edges: list[Edge] = []

        while len(path) > 1:
            section_start: Vertex = vertices[path.pop(0)]
            section_end: Vertex = vertices[path[0]]
            edge = self.getDuplicate(Edge(section_start, section_end, self)) # Get the original edge
            if edge is None:
                continue

            path_edges.append(edge)
        
        def animatePath(vertex: Vertex):
            if vertex == start:
                vertex.setHighlight(True, "start")
            elif vertex == goal:
                vertex.setHighlight(True, "end")
            else:
                vertex.setSelected(True)

            for edge in vertex.edges:
                if edge in path_edges:
                    path_edges.remove(edge)
                    start_point = vertex.getPosition()
                    end_point = edge.getOpposite(vertex).getPosition()
                    edge.play(start_point, end_point)
                    next = edge.getOpposite(vertex)
                    QTimer.singleShot(edge.anim_duration, lambda: animatePath(next))
                    
        animatePath(start)


    def resetPaths(self):
        self.floyd.reset()
        self.dijkstra.reset()

    def emitSignal(self):
        self.createAdjMatrix()
        self._updateEdges()
        self.mcst_total_cost = self.mcst_graph.total_cost
        self.graphChanged.emit()

    def onSelectionChanged(self):
        if self.is_adding_edge:
            self.createEdge()

    def _updateEdges(self):
        edges = self.getEdges()
        for edge in edges:
            # Set as curved if the graph is directed
            if self.is_directed_graph:
                self.setCurvedEdge(edge)

    def perform_action(self, command: Command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear() 

    def undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)