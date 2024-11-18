from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.model import Graph, Edge    

class ComplementGraph():
    def __init__(self, graph):
        self.graph: Graph = graph
        self.vertices = []
        self.original_edges = []          # All original edges in the graph
        self.vertex_edges_backup = {}      # Dictionary to store original edges per vertex
        self.complement_edges = []         # New edges created for the complement

    def show(self):   
        self.vertices = self.graph.getVertices()
        self.original_edges  = self.graph.getEdges() 
        self.vertex_edges_backup = {vertex: list(vertex.edges) for vertex in self.vertices}

        # Remove all original edges from the graph
        for edge in self.original_edges:
            self.graph.removeItem(edge)

        # Create and store new complement edges
        new_edges = []

        for vertex in self.vertices:
            # Find neighbors of the vertex
            neighbors = [edge.getOpposite(vertex) for edge in vertex.edges]

            # Find vertices that are not neighbors to create complement edges
            complement_vertices = [v for v in self.vertices if v not in neighbors and v != vertex]
            
            # Clear the vertex's edges to prepare for complement edges
            vertex.edges.clear()

            for complement_vertex in complement_vertices:
                complement_edge = Edge(vertex, complement_vertex, self.graph)
                duplicate_edge = self.graph.getDuplicate(complement_edge)

                # If no duplicate edge, add the new complement edge
                if not duplicate_edge:
                    new_edges.append(complement_edge)
                    vertex.addEdge(complement_edge)
                else:
                    vertex.addEdge(duplicate_edge)

        # Add new complement edges to the graph and store them
        for edge in new_edges:
            duplicate_edge = self.graph.getDuplicate(edge)
            if not duplicate_edge:
                self.graph.addItem(edge)
                self.complement_edges.append(edge)

    def revert(self):
        # Remove all complement edges from the graph
        for edge in self.complement_edges:
            edge in self.graph.items() and self.graph.removeItem(edge)

        # Restore each vertex's original edges
        for vertex, edges in self.vertex_edges_backup.items():
            vertex.edges = edges

        # Re-add the original edges to the graph
        for edge in self.original_edges:
            edge not in self.graph.items() and self.graph.addItem(edge)

        # Clear stored complement edges to reset state
        self.complement_edges.clear()
        self.vertex_edges_backup.clear()
