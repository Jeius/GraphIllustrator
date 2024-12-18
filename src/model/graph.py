import math
import sys, os
from typing import List, TYPE_CHECKING
from PyQt5.QtCore import pyqtSignal, Qt, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem, QMessageBox
from PyQt5.QtGui import QPen, QIcon


from src.algorithm import Djisktra, FloydWarshall
from src.commands import AddEdgeCommand, AddVertexCommand, ClearEdgesCommand, DeleteEdgeCommand, DeleteVertexCommand

if TYPE_CHECKING:
    from src.model import Vertex, Edge
    from src.commands import Command

def getFilePath(path):
    """Constructs the file path based on the running environment."""
    if getattr(sys, 'frozen', False):  # PyInstaller bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level
    return os.path.join(base_path, path)

def loadIcon(path):
    file_path = getFilePath(path)

    if not os.path.exists(file_path):
        print(f"Icon file not found: {file_path}")
        return QIcon()

    return QIcon(file_path)


class Graph(QGraphicsScene):
    DIAMETER = 30
    graphChanged = pyqtSignal()

    def __init__(self):
        from src.model import ComplementGraph, MinimumCostSpanningTree

        super().__init__()
        self.selected_vertices: List['Vertex'] = []   # List of the selected vertices
        self.adj_matrix: list[list[float]] = []     # Adjacency matrix
        
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

        self.undo_stack: list['Command'] = []
        self.redo_stack: list['Command'] = []

        self.selectionChanged.connect(self.onSelectionChanged)


#------------------------------ Creators ----------------------------------------------------------#
    def createVertex(self, position: QPointF):
        from src.model import Vertex
        diameter = self.DIAMETER
        id = self.genNextId()  
        vertex = Vertex(id, diameter, self)
        radius = diameter / 2
        adjusted_position = QPointF(position.x() - radius, position.y() - radius)
        vertex.setPos(adjusted_position)

        command = AddVertexCommand(self, vertex)
        self.perform_action(command)
    
    def createAdjMatrix(self):
        vertices = self.getVertices()
        
        if not self.getEdges():
            self.adj_matrix.clear()
            return

        number_of_vertices = len(vertices)
        # Intiallize matrix with infinities
        self.adj_matrix = [[math.inf for _ in range(number_of_vertices)] for _ in range(number_of_vertices)]  

        for vertex in vertices:
            for edge in vertex.edges:
                if vertex == edge.getStart():
                    start_index = vertices.index(vertex)
                    end_index = vertices.index(edge.getOpposite(vertex))
                    
                    if edge.weight != math.inf:
                        if self.is_directed_graph:
                            self.adj_matrix[start_index][end_index] = edge.weight
                        else:
                            self.adj_matrix[start_index][end_index] = edge.weight
                            self.adj_matrix[end_index][start_index] = edge.weight
            
                    self.adj_matrix[start_index][start_index] = 0
                    self.adj_matrix[end_index][end_index] = 0               

    def createEdge(self):
        selected_vertex = self._getSelectedVertex()
        if not selected_vertex:
            self._clearIndicatorLine()
            return
        
        if self.indicator_line not in self.items():
            self.addItem(self.indicator_line)

        if not self.selected_vertices:
            self._initializeEdgeLine(selected_vertex)
        else:
            self._finalizeEdge(selected_vertex)
                
    def genNextId(self):
        """Generate the next ID index for a new vertex."""
        vertices = self.getVertices()
        return vertices[-1].id_index + 1 if vertices else 0


                
#--------------------------- Setters ------------------------------------------#
    def setHighlightItems(self, highlighting: bool, colorType:str = None):
        for edge in self.getEdges():
            edge.setHighlight(highlighting)
        for vertex in self.getVertices():
            vertex.setHighlight(highlighting, colorType)

    def setDirectedGraph(self, is_directed: bool):
        self.is_directed_graph = is_directed
        self.emitSignal()

    def setCurvedEdge(self, edge:'Edge'):
        from src.model import Edge
        start = edge.getStart()
        end = edge.getOpposite(start)
        opposite_edge = Edge(end, start, self)
        duplicate_edge = self.getDuplicate(opposite_edge)

        if duplicate_edge:
            edge.setCurved(True)
            duplicate_edge.setCurved(True)
        else:
            edge.setCurved(False) 

    def setAlgorithm(self, algorithm_name: str, enable: bool):
        """Generic method to set the algorithm mode by name."""
        self.resetPaths()
        self.clearSelection()
        self.setHighlightItems(False)

        algorithms = {
            "floyd": "is_using_floyd",
            "dijkstra": "is_using_dijkstra",
            "prim": "is_using_prim",
            "kruskal": "is_using_kruskal",
        }
        
        # Disable all algorithms
        if self.is_directed_graph:
            setattr(self, algorithms['floyd'], False)
            setattr(self, algorithms['dijkstra'], False)
        else:
            setattr(self, algorithms['prim'], False)
            setattr(self, algorithms['kruskal'], False)
        
        # Enable the specified algorithm
        if algorithm_name in algorithms:
            setattr(self, algorithms[algorithm_name], enable)
            self.emitSignal()



#--------------------------- Getters ------------------------------------------#
    def getVertices(self):
        from src.model import Vertex
        items = self.items()
        vertices = [item for item in items if isinstance(item, Vertex)]
        vertices.reverse()
        vertices.sort(key=lambda vertex: vertex.id[0])
        return vertices
    
    def getEdges(self):
        from src.model import Edge
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

    def getDuplicate(self, new_edge: 'Edge'):
        edges = self.getEdges()
        for edge in edges:
            if new_edge == edge:
                return edge 
    



#--------------------------- Delete ---------------------------------------------#
    def removeVertex(self, vertex: 'Vertex'):
        self.resetPaths()
        command = DeleteVertexCommand(self, vertex)
        self.perform_action(command)

    def removeEdge(self, edge: 'Edge'):
        self.resetPaths()
        command = DeleteEdgeCommand(self, edge)
        self.perform_action(command)

    def revert(self):
        self.clearSelection()
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
        edges = self.getEdges()
        command = ClearEdgesCommand(self, edges)
        self.perform_action(command)




#----------------------------- Algorithms -------------------------------------------#
    def findPath(self):
        try:
            self.undo_stack.clear()
            
            matrix = self.adj_matrix
            vertices = self.getVertices()

            for vertex in vertices:
                if not vertex.edges:
                    raise Exception("Not all vertices are connected.")
            
            for edge in self.getEdges():
                if edge.weight == math.inf:
                    raise Exception("Not all edges have weight.")

            if self.is_using_floyd:
                self.floyd.run(matrix)
                self.clearSelection()

            elif self.is_using_dijkstra:
                selected_vertex = self._getSelectedVertex()

                if not selected_vertex:
                    raise Exception("No starting vertex selected")
                
                start_index = vertices.index(selected_vertex)
                self.dijkstra.run(matrix, start_index)
                
        except Exception as e:
            self._showErrorDialog("Path Finding Failed", str(e))

    def findMCST(self, is_finding_mcst):
        self.undo_stack.clear()
        if is_finding_mcst:
            self.mcst_graph.show()
        else:
            self.mcst_graph.revert()
        self.emitSignal()
        
    def findGraphCenter(self):
        """
        Computes eccentricities based on maximum values in each column
        and determines the center of the graph.
        """
        try:
            vertices = self.getVertices()
            if len(vertices) == 1:
                raise Exception('Add atleast 3 vertices with edges')
            
            for v in vertices:
                if not v.edges:
                    raise Exception('An isolated vertex is found. Cannot find graph center on a disconnected graph.')
            
            self.floyd.run(self.adj_matrix)
            dist = self.floyd.distances

            eccentricities: list[int] = []
            size = len(dist)
            for j in range(size):
                ecc = max([dist[i][j] for i in range(size)])
                eccentricities.append(ecc)

            center = min(eccentricities)
            center_vertex = vertices[eccentricities.index(center)]
            vertices_with_ecc = [(vertices[i], eccentricities[i]) for i in range(len(eccentricities))]
            
            return (vertices_with_ecc, center_vertex)
        except Exception as e:
            self._showErrorDialog("Operation Failed", str(e))

    def findIndependentSets(self):
        from src.model import IndependentSets
        try:
            independent_set = IndependentSets(self.adj_matrix)
            result = independent_set.get()
            print(result)
            vertices = self.getVertices()
            IS_vertices: list[list['Vertex']] = []
            independence_num = len(vertices)
            for set in result:
                if not set:
                    continue
                
                converted = [vertices[i] for i in set]
                IS_vertices.append(converted)
                independence_num = max(len(ind_set) for ind_set in IS_vertices)

            if len(result) == 1:
                IS_vertices.append(vertices)
            
            return (IS_vertices, independence_num)

        except Exception as e:
            self._showErrorDialog("Operation Failed", str(e))



#----------------------------- Local Functions --------------------------------------#
    def _showErrorDialog(self, title: str, message: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setWindowIcon(loadIcon("favicon.ico"))
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def _showConfirmDialog(self, title: str, message: str):
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Warning)
        confirm_box.setWindowTitle(title)
        confirm_box.setWindowIcon(loadIcon("favicon.ico"))
        confirm_box.setText(message)
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        return confirm_box.exec_()
    
    def _getSelectedVertex(self):
        """Retrieve the selected vertex if available."""
        from src.model import Vertex
        return next((vertex for vertex in self.selectedItems() if isinstance(vertex, Vertex)), None)

    def _clearIndicatorLine(self):
        """Clear selected vertices and indicator line."""
        self.selected_vertices.clear()
        if self.indicator_line in self.items():
            self.removeItem(self.indicator_line)

    def _initializeEdgeLine(self, selected_vertex: 'Vertex'):
        """Initialize the edge line with the starting vertex."""
        line = self.indicator_line.line()
        self.selected_vertices.append(selected_vertex)
        line.setP1(selected_vertex.getPosition())
        line.setP2(selected_vertex.getPosition())
        self.indicator_line.setLine(line)

    def _finalizeEdge(self, selected_vertex: 'Vertex'):
        """Finalize edge creation and add it to the scene."""
        from src.model import Edge

        start = self.selected_vertices.pop()
        end = selected_vertex
        line = self.indicator_line.line()
        line.setP1(end.getPosition())
        self.indicator_line.setLine(line)

        edge = Edge(start, end, self)
        if self.getDuplicate(edge):
            self.clearSelection()
            return

        command = AddEdgeCommand(self, edge)
        self.perform_action(command)
        self.selected_vertices.append(end)


    def showPath(self, start:'Vertex' = None, goal:'Vertex' = None):
        from src.model import Edge
        # Ensure start and goal are valid
        if not start or not goal:
            return
        
        vertices = self.getVertices()

        # Get paths based on algorithm choice
        if self.is_using_floyd:
            paths = self.floyd.paths
        elif self.is_using_dijkstra:
            paths = self.dijkstra.paths

        if not paths:
            return

        # Unhighlight all items first
        self.setHighlightItems(False)
        self.clearSelection()

        # Retrieve path from start to goal
        try:
            if self.is_using_floyd:
                path = list(paths[(vertices.index(start), vertices.index(goal))])
            elif self.is_using_dijkstra:
                path = list(paths[vertices.index(goal)])
        except:
            raise Exception("No path found.")

        path_edges: list['Edge'] = []

        while len(path) > 1:
            section_start: 'Vertex' = vertices[path.pop(0)]
            section_end: 'Vertex' = vertices[path[0]]
            edge = self.getDuplicate(Edge(section_start, section_end, self))
            if edge is None:
                continue

            path_edges.append(edge)
        
        def animatePath(vertex: 'Vertex'):
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

    def perform_action(self, command: 'Command'):
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