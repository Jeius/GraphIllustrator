from .model import Command

class AddEdgeCommand(Command):
    from ..model.vertex import Vertex
    from ..model.edge import Edge
    from ..model.graph import Graph

    def __init__(self, graph: Graph, edge: Edge):
        self.graph = graph
        self.start_vertex = edge.start_vertex
        self.end_vertex = edge.end_vertex
        self.edge = edge

    def execute(self):
        # Add the edge to the vertices
        self.start_vertex.addEdge(self.edge)
        self.end_vertex.addEdge(self.edge)
        self.graph.addItem(self.edge)
        
        self.graph.emitSignal()

    def undo(self):
        self.start_vertex.removeEdge(self.edge)
        self.end_vertex.removeEdge(self.edge)
        self.graph.removeItem(self.edge)
        self.graph.emitSignal()


class DeleteEdgeCommand(Command):
    from ..model.vertex import Vertex
    from ..model.edge import Edge
    from ..model.graph import Graph

    def __init__(self, graph: Graph, edge: Edge):
        self.graph = graph
        self.start_vertex = edge.start_vertex
        self.end_vertex = edge.end_vertex
        self.edge = edge

    def execute(self):
        # Add the edge to the vertices
        self.edge in self.start_vertex.edges and self.start_vertex.removeEdge(self.edge)
        self.edge in self.end_vertex.edges and self.end_vertex.removeEdge(self.edge)
        self.edge in self.graph.getEdges() and self.graph.removeItem(self.edge)
        self.graph.emitSignal()

    def undo(self):
        self.edge not in self.start_vertex.edges and self.start_vertex.addEdge(self.edge)
        self.edge not in self.end_vertex.edges and self.end_vertex.addEdge(self.edge)
        self.edge not in self.graph.getEdges() and self.graph.addItem(self.edge)
        self.graph.emitSignal()