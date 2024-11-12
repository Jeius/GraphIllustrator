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
    graphChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.vertices: List[Vertex] = []  # List of the vertices
        self.selected_vertices: List[Vertex] = []   # List of the selected vertices
        self.edges: List[Edge] = []     # List of edges
        self.adjacencyMatrix: list[list[float]] = []     # Adjacency matrix
        
        self.djisktra = Djisktra(self.vertices)
        self.floyd = FloydWarshall(self.vertices)

        self.is_adding_vertex = False  # Flag to enable adding vertex
        self.is_adding_edge = False    # Flag to enable adding edge
        self.is_using_dijkstra = False  # Flag to enable djisktra algorithm
        self.is_using_floyd = False     # Flag to enable floyd algorithm
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
        self.vertices.append(vertex)
        self.addItem(vertex)

        self.emitSignal()
    
    def createAdjMatrix(self):
        # Terminate the execution if there are no vertices
        size = len(self.vertices)
        if size == 0:
            return

        # Intiallize matrix with zeros
        self.adjacencyMatrix = [[math.inf for _ in range(size)] for _ in range(size)]  

        # Create a dictionary of index values with the vertex ids as keys
        idToIndex = {vertex.id: index for index, vertex in enumerate(self.vertices)}

        for vertex in self.vertices:
            for edge in vertex.edges:
                if vertex == edge.getStart():
                    indexA = idToIndex[edge.start_vertex.id]
                    indexB = idToIndex[edge.end_vertex.id]
                    
                    if edge.weight != math.inf:
                        self.adjacencyMatrix[indexA][indexB] = edge.weight
            
                    self.adjacencyMatrix[indexA][indexA] = 0
                    self.adjacencyMatrix[indexB][indexB] = 0               

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
            index = vertices[0].id_index + 1

        return index

    def delete(self):
        # Delete the selected items from the graph
        # Iterate from the vertices if the selected item is a vertex
        for vertex in self.vertices.copy():  # Iterate from a copy
            if vertex.isSelected():
                # Remove from the list of vertices
                self.vertices.remove(vertex) 
                
                # Also remove the edges from its neighbor that was connected 
                # to the vertex
                for vertex_edge in vertex.edges:
                    neighbor = vertex_edge.getOpposite(vertex)

                    for neighbor_edge in neighbor.edges.copy():
                        # Get the opposite of the neighbor, this means that 
                        # the opposite will most likely be the vertex
                        neighbor_opposite = neighbor_edge.getOpposite(neighbor)

                        # Check if it is true, 
                        # then remove the edge in the neighbor's edges
                        if neighbor_opposite == vertex:
                            neighbor_edge in neighbor.edges and neighbor.edges.remove(neighbor_edge)
                            neighbor_edge in self.edges and self.edges.remove(neighbor_edge)
                            del neighbor_edge   # Deleting the edge to save memory
            del vertex  # Deleting the vertex to save memory

        # Iterate from the edges if the selected item is an edge
        for edge in self.edges.copy(): # Iterate from a copy
            if edge.isSelected():
                # Remove the edge in both endpoints
                edge in edge.start_vertex.edges and edge.start_vertex.edges.remove(edge)
                edge in edge.end_vertex.edges and edge.end_vertex.edges.remove(edge)
                self.edges.remove(edge)
                del edge


                
#--------------------------- Setters ------------------------------------------#
    def setHighlightItems(self, highlighting: bool):
        for edge in self.edges:
            edge.setHighlight(highlighting)
        for vertex in self.vertices:
            vertex.setHighlight(highlighting, None)

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

#--------------------------- Getters ------------------------------------------#
    def getVertices(self):
        items = self.items()
        return [item for item in items if isinstance(item, Vertex)]
    
    def getEdges(self):
        items = self.items()
        return [item for item in items if isinstance(item, Edge)]
    
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
        super().clear()
        self.adjacencyMatrix.clear()
        self.is_adding_edge = False
        self.is_adding_vertex = False
        self.is_using_dijkstra = False
        self.emitSignal()
        
    def clearEdges(self):
        edges = self.getEdges()
        for edge in edges:
            edge.start_vertex.clearEdges()
            edge.end_vertex.clearEdges()
            self.removeItem(edge)
        self.emitSignal()




#----------------------------- Algorithms -------------------------------------------#
    def useDjisktra(self):
        if self.is_using_dijkstra:
            for item in self.selectedItems():
                if isinstance(item, Vertex):
                    self.djisktra.findPath(item, self.adjacencyMatrix)

    def useFloyd(self):
        if self.is_using_floyd:
            self.floyd.findPath(self.adjacencyMatrix)




#----------------------------- Local Functions --------------------------------------#
    def _showInvalid(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setWindowTitle("Invalid Path")
        msg_box.setText("No path found.")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()

    def showPath(self, start: Union[Vertex, None], goal: Union[Vertex, None]):
        # Unhighlight all items first
        self.setHighlightItems(False)

        # Ensure start and goal are valid
        if not start or not goal:
            return

        # Highlight start and goal vertices
        goal.setHighlight(True, 1)
        start.setHighlight(True, 0)

        try:
            paths = None

            # Get paths based on algorithm choice
            if self.is_using_floyd:
                paths = self.floyd.paths
            elif self.is_using_dijkstra:
                paths = self.djisktra.paths

            if not paths:
                return

            # Retrieve path from start to goal
            if self.is_using_floyd:
                path = list(paths[(self.vertices.index(start), self.vertices.index(goal))])
            elif self.is_using_dijkstra:
                path = list(paths[self.vertices.index(goal)])

            # Highlight edges along the path
            while len(path) > 1:
                start = self.vertices[path.pop(0)]
                end = self.vertices[path[0]]
                edge = self.getDuplicate(Edge(start, end))
                if edge is not None:
                    edge.setHighlight(True)
        except Exception as e:
            self._showInvalid()

        for item in self.items():
            item.update()

    def emitSignal(self):
        self.update()
        self.graphChanged.emit(self)

    def onSelectionChanged(self):
        if self.is_adding_edge:
            self.createEdge()

    def update(self):
        self.createAdjMatrix()
        return super().update()