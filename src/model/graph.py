import math
import string
from typing import List, Union
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

from .vertex import Vertex
from .edge import Edge
from ..algorithm.djisktra import Djisktra
from ..algorithm.floyd import FloydWarshall

class Graph(QtWidgets.QGraphicsScene):
    graphChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.selected_vertices: List[Vertex] = []   # List of the selected vertices
        self.adjacencyMatrix: list[list[float]] = []     # Adjacency matrix
        
        self.dijkstra = Djisktra()
        self.floyd = FloydWarshall()

        self.is_adding_vertex = False 
        self.is_adding_edge = False   
        self.is_using_dijkstra = True 
        self.is_using_floyd = False     
        self.is_using_prim = False
        self.is_using_kruskal = False
        self.is_directed_graph = True
        self.is_deleting = False
        self.is_editing_weight = False
        self.is_id_int = True

        self.selectionChanged.connect(self.onSelectionChanged)

#------------------------------ Creators ----------------------------------------------------------#
    def createVertex(self, scene_position: QtCore.QPointF):
        # Define the diameter of the circle
        diameter = 30
        radius = diameter / 2
        position = QtCore.QPointF(scene_position.x() - radius, scene_position.y() - radius)
        id = self.genIdIndex()
        vertex = Vertex(id, diameter, self)
        vertex.setPos(position) 
        self.addItem(vertex)

        self.emitSignal()
    
    def createAdjMatrix(self):
        vertices = self.getVertices()
        # Terminate the execution if there are no vertices
        size = len(vertices)
        if size == 0:
            return

        # Intiallize matrix with infinities
        self.adjacencyMatrix = [[math.inf for _ in range(size)] for _ in range(size)]  

        for vertex in vertices:
            for edge in vertex.edges:
                if vertex == edge.getStart():
                    start_index = edge.start_vertex.id[0]
                    end_index = edge.end_vertex.id[0]
                    
                    if edge.weight != math.inf:
                        if self.is_directed_graph:
                            self.adjacencyMatrix[start_index][end_index] = edge.weight
                        else:
                            self.adjacencyMatrix[start_index][end_index] = edge.weight
                            self.adjacencyMatrix[end_index][start_index] = edge.weight
            
                    self.adjacencyMatrix[start_index][start_index] = 0
                    self.adjacencyMatrix[end_index][end_index] = 0               

    def createEdge(self,):
        selected_items = self.selectedItems()
        selected_vertices = self.selected_vertices

        if len(selected_items) == 0:
            selected_vertices.clear()

        # Loop through all selected items in the scene
        for item in selected_items:
            if not isinstance(item, Vertex):
                continue

            vertex = item
            if len(selected_vertices) == 0:
                selected_vertices.append(vertex)
            else:
                start = selected_vertices.pop()
                end = vertex
                edge = Edge(start, end, self)

                duplicate_edge = self.getDuplicate(edge)

                if duplicate_edge: 
                        continue

                start.addEdge(edge)
                end.addEdge(edge)
                self.addItem(edge)

                if self.is_directed_graph:
                    self.setCurvedEdge(edge)   

                selected_vertices.append(vertex) 
        self.emitSignal()

    def genIdIndex(self):
        index = 0
        vertices = self.getVertices()

        if len(vertices) != 0:
            index = vertices[-1].id_index + 1

        return index


                
#--------------------------- Setters ------------------------------------------#
    def setHighlightItems(self, highlighting: bool, colorType: Union[str, None]):
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
        self.floyd.reset()
        self.clearSelection()
        self.setHighlightItems(False, None)
        self.is_using_floyd = is_floyd
        self.emitSignal()

    def setDijkstra(self, is_dijkstra: bool):
        self.dijkstra.reset()
        self.clearSelection()
        self.setHighlightItems(False, None)
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
        return vertices
    
    def getEdges(self):
        items = self.items()
        edges = [item for item in items if isinstance(item, Edge)]
        edges.reverse()
        return edges
    
    def getComplement(self):
        vertices = self.getVertices()
        edges = self.getEdges()
        for edge in edges:
            self.removeItem(edge)

        new_edges = []

        for vertex in vertices:
            neighbors = []
            for edge in vertex.edges:
                neighbor = edge.getOpposite(vertex)
                neighbors.append(neighbor)
            
            complement_vertices = [v for v in vertices if v not in neighbors and v != vertex]
            vertex.edges.clear()

            for complement_vertex in complement_vertices:
                complement_edge = Edge(vertex, complement_vertex, self)
                duplicate_edge = self.getDuplicate(complement_edge)

                if not duplicate_edge:
                    new_edges.append(complement_edge)
                    vertex.addEdge(complement_edge)
                else:
                    vertex.addEdge(duplicate_edge)
        
        for edge in new_edges:
            duplicate_edge = self.getDuplicate(edge)
            if not duplicate_edge:
                self.addItem(edge)
        
        self.emitSignal()

    def getDuplicate(self, new_edge: Edge):
        edges = self.getEdges()
        for edge in edges:
            if new_edge == edge:
                return edge 
        return None
    

#--------------------------- Delete ---------------------------------------------#
    def removeItem(self, item):
        self.dijkstra.reset()
        self.floyd.reset()

        edges = self.getEdges()

        if isinstance(item, Vertex):
            vertex = item
            for vertex_edge in item.edges:
                neighbor = vertex_edge.getOpposite(vertex)

                for neighbor_edge in neighbor.edges.copy():
                    # Get the opposite of the neighbor, this means that 
                    # the opposite will most likely be the vertex
                    neighbor_opposite = neighbor_edge.getOpposite(neighbor)

                    # Check if it is true, 
                    # then remove the edge in the neighbor's edges
                    if neighbor_opposite == vertex:
                        neighbor_edge in neighbor.edges and neighbor.edges.remove(neighbor_edge)
                        neighbor_edge in edges and super().removeItem(neighbor_edge)
            super().removeItem(vertex)

        elif isinstance(item, Edge):
            # Remove the edge in both endpoints
            edge = item
            start = edge.start_vertex
            end = edge.end_vertex
            
            edge in start.edges and start.edges.remove(edge)
            edge in end.edges and end.edges.remove(edge)
            edge in edges and super().removeItem(edge)
        
        self.emitSignal()

    def clear(self):
        self.adjacencyMatrix.clear()
        self.dijkstra.reset()
        self.floyd.reset()
        super().clear()
        self.emitSignal()
        
    def clearEdges(self):
        edges = self.getEdges()
        for edge in edges:
            edge.start_vertex.clearEdges()
            edge.end_vertex.clearEdges()
            self.removeItem(edge)
        self.dijkstra.reset()
        self.floyd.reset()
        self.emitSignal()




#----------------------------- Algorithms -------------------------------------------#
    def findPath(self):
        try:
            vertices = self.getVertices()
            matrix = self.adjacencyMatrix

            if self.is_using_floyd:
                self.floyd.findPath(matrix, vertices)
                self.clearSelection()

            elif self.is_using_dijkstra:
                for item in self.selectedItems():
                    start_vertex = item
                    if not isinstance(start_vertex, Vertex):
                        continue
                    self.dijkstra.findPath(start_vertex, matrix, vertices)
            
            self.setHighlightItems(False, None)
        except Exception as e:
            self._showErrorDialog(title="Invalid Graph", message="")



#----------------------------- Local Functions --------------------------------------#
    def _showErrorDialog(self, title: string, message: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

    def showPath(self, start: Union[Vertex, None], goal: Union[Vertex, None]):
        # Ensure start and goal are valid
        if not start or not goal:
            return
        
        # Unhighlight all items first
        self.setHighlightItems(False, None)
        self.clearSelection()

        # Highlight start and goal vertices
        goal.setHighlight(True, "end")
        start.setHighlight(True, "start")

        vertices = self.getVertices()

        try:
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

            # Highlight edges along the path
            while len(path) > 1:
                section_start: Vertex = vertices[path.pop(0)]
                section_end: Vertex = vertices[path[0]]
                edge = self.getDuplicate(Edge(section_start, section_end, self))

                if edge is None:
                    continue

                edge.setHighlight(True)
                if section_start != start:
                    section_start.setHighlight(True, "route")

        except Exception as e:
            self._showErrorDialog(title="Invalid Path", message="No path found.")

    def emitSignal(self):
        self.createAdjMatrix()
        self.graphChanged.emit()

    def onSelectionChanged(self):
        if self.is_adding_edge:
            self.createEdge()
