from PyQt5.QtCore import QPointF

from .model import Command

class AddVertexCommand(Command):
    from ..model.graph import Graph
    from ..model.vertex import Vertex

    def __init__(self, graph: Graph, vertex: Vertex):
        self.graph = graph
        self.vertex = vertex

    def execute(self):
        if self.vertex not in self.graph.getVertices():
            self.graph.addItem(self.vertex)
            self.graph.clearSelection()
        self.graph.emitSignal()

    def undo(self):
        if self.vertex in self.graph.getVertices():
            self.graph.removeItem(self.vertex)
        self.graph.emitSignal()


class DeleteVertexCommand(Command):
    from ..model.graph import Graph
    from ..model.vertex import Vertex

    def __init__(self, graph: Graph, vertex: Vertex):
        from ..model.edge import Edge
        from ..model.vertex import Vertex

        self.graph = graph
        self.vertex = vertex
        # Store each neighbor and their edges that connect to the vertex being removed
        self.removed_edges: list[tuple[Vertex, list[Edge]]] = []

    def execute(self):
        # Collect all edges connected to this vertex and remove them from the graph
        for vertex_edge in self.vertex.edges.copy():
            neighbor = vertex_edge.getOpposite(self.vertex)

            # Track edges for each neighbor and remove from both vertices and the graph
            edges_to_be_removed = []
            for neighbor_edge in neighbor.edges.copy():
                if neighbor_edge.getOpposite(neighbor) == self.vertex:
                    edges_to_be_removed.append(neighbor_edge)
                    
                    neighbor_edge.setHighlight(False)
                    neighbor_edge.setSelected(False)

                    neighbor.removeEdge(neighbor_edge)
                    self.graph.removeItem(neighbor_edge)

            # Append removed edges for undo tracking
            self.removed_edges.append((neighbor, edges_to_be_removed))

        # Remove the vertex itself from the graph
        if self.vertex in self.graph.getVertices():
            self.vertex.setHighlight(False)
            self.vertex.setSelected(False)
            self.graph.removeItem(self.vertex)

        # Signal that the scene has changed
        self.graph.emitSignal()

    def undo(self):
        # Re-add the vertex to the graph
        if self.vertex not in self.graph.getVertices():
            self.graph.addItem(self.vertex)

        # Restore each previously removed edge
        for neighbor, edges in self.removed_edges:
            for edge in edges:
                if edge not in neighbor.edges:
                    neighbor.addEdge(edge)
                if edge not in self.vertex.edges:
                    self.vertex.addEdge(edge)
                if edge not in self.graph.getEdges():
                    self.graph.addItem(edge)

        # Signal that the scene has reverted
        self.graph.emitSignal()