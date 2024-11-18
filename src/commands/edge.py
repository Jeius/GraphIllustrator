from .model import Command

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.model import Graph, Edge, Vertex


class AddEdgeCommand(Command):
    def __init__(self, graph, edge):
        self.graph: Graph = graph
        self.edge: Edge = edge
        self.start_vertex = self.edge.start_vertex
        self.end_vertex = self.edge.end_vertex
        

    def execute(self):
        self.edge not in self.start_vertex.edges and self.start_vertex.addEdge(self.edge)
        self.edge not in self.end_vertex.edges and self.end_vertex.addEdge(self.edge)
        self.edge not in self.graph.items() and self.graph.addItem(self.edge)
        self.graph.emitSignal()

    def undo(self):
        self.edge.setHighlight(False)
        self.edge.setSelected(False)
        self.edge in self.start_vertex.edges and self.start_vertex.removeEdge(self.edge)
        self.edge in self.end_vertex.edges and self.end_vertex.removeEdge(self.edge)
        self.edge in self.graph.items() and self.graph.removeItem(self.edge)
        self.graph.emitSignal()


class DeleteEdgeCommand(Command):
    def __init__(self, graph, edge):
        self.graph: Graph = graph
        self.edge: Edge = edge
        self.start_vertex = self.edge.start_vertex
        self.end_vertex = self.edge.end_vertex

    def execute(self):
        self.edge.setHighlight(False)
        self.edge.setSelected(False)
        self.edge in self.start_vertex.edges and self.start_vertex.removeEdge(self.edge)
        self.edge in self.end_vertex.edges and self.end_vertex.removeEdge(self.edge)
        self.edge in self.graph.items() and self.graph.removeItem(self.edge)
        self.graph.emitSignal()

    def undo(self):
        self.edge not in self.start_vertex.edges and self.start_vertex.addEdge(self.edge)
        self.edge not in self.end_vertex.edges and self.end_vertex.addEdge(self.edge)
        self.edge not in self.graph.items() and self.graph.addItem(self.edge)
        self.graph.emitSignal()


class ClearEdgesCommand(Command):
    def __init__(self, graph, edges):
        self.graph: Graph = graph
        self.edges: list[Edge] = edges
        # Store the removed edges along with their start and end vertices
        self.removed_edges: list[tuple[Edge, Vertex, Vertex]] = []

    def execute(self):
        # Clear edges and save their details for undo
        for edge in self.edges:
            start_vertex = edge.start_vertex
            end_vertex = edge.end_vertex
            self.removed_edges.append((edge, start_vertex, end_vertex))
            
            edge.setHighlight(False)
            edge.setSelected(False)
            
            # Remove the edge from both vertices and the graph
            edge in start_vertex.edges and start_vertex.removeEdge(edge)
            edge in end_vertex.edges and end_vertex.removeEdge(edge)
            edge in self.graph.items() and self.graph.removeItem(edge)
        
        self.graph.emitSignal()

    def undo(self):
        # Re-add the edges and connect them back to their vertices
        for edge, start_vertex, end_vertex in self.removed_edges:
            # Add edge back to each vertex
            edge not in start_vertex.edges and start_vertex.addEdge(edge)
            edge not in end_vertex.edges and end_vertex.addEdge(edge)
            
            # Add the edge back to the scene/graph
            edge not in self.graph.items() and self.graph.addItem(edge)
        
        self.graph.emitSignal()
