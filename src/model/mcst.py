import math
from PyQt5.QtCore import QTimer

from src.algorithm import Prim, Kruskal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .graph import Graph
    from .edge import Edge    
    from .vertex import Vertex


class MinimumCostSpanningTree():
    def __init__(self, graph):
        self.graph: Graph = graph
        self.prim = Prim()
        self.kruskal = Kruskal()
        self.vertices = []
        self.original_edges = []          # All original edges in the graph
        self.vertex_edges_backup = {}     # Dictionary to store original edges per vertex
        self.mcst_edges = []              # New edges created for the mcst
        self.total_cost = None

    def show(self):
        self.vertices = self.graph.getVertices()
        self.vertex_edges_backup = {vertex: list(vertex.edges) for vertex in self.vertices}
        self.original_edges = list(self.graph.getEdges())
        matrix = self.graph.adj_matrix
        selected_vertex = next((vertex for vertex in self.graph.selectedItems() if isinstance(vertex, Vertex)), None)

        if not selected_vertex:
            raise Exception("No starting vertex selected.")
        
        for vertex in self.vertices:
            if not vertex.edges:
                raise Exception("MCST cannot be formed. Not all vertices are connected.")
            
        for edge in self.original_edges:
            if edge.weight == math.inf:
                raise Exception("MCST cannot be formed. Not all edges have weight.")
            
        if len(self.original_edges) < len(self.vertices):
            raise Exception("Graph is already a spanning tree.")
        
        start = self.vertices.index(selected_vertex)

        if self.graph.is_using_prim:
            result: list[tuple[int, int, int]] = self.prim.MCST(matrix)
        elif self.graph.is_using_kruskal:
            result: list[tuple[int, int, int]] = self.kruskal.MCST(matrix)

        if not result:
            raise Exception("MCST cannot be formed. Invalid graph.")

        self.total_cost = 0

        for edge in self.graph.getEdges():
            edge.start_vertex.clearEdges()
            edge.end_vertex.clearEdges()
            self.graph.removeItem(edge)

        for result_edge in result:
            start, end, weight = result_edge
            start_vertex = self.vertices[start]
            end_vertex = self.vertices[end]
            edge = Edge(start_vertex, end_vertex, self.graph)
            edge.setWeight(weight)
            edge.setTransparent(True)
            duplicate_edge = self.graph.getDuplicate(edge)
            if not duplicate_edge:
                self.graph.addItem(edge)
                start_vertex.addEdge(edge)
                end_vertex.addEdge(edge)
                self.total_cost += weight
            else:
                start_vertex.addEdge(duplicate_edge)
                end_vertex.addEdge(duplicate_edge)
            
        self.graph.clearSelection()
        selected_vertex.setHighlight(True, "start")
        self.animate(selected_vertex)

    def revert(self):
        self.total_cost = None

        # Remove all mcst edges from the graph
        for edge in self.graph.getEdges():
            self.graph.removeItem(edge)

        # Restore each vertex's original edges
        for vertex, edges in self.vertex_edges_backup.items():
            vertex.edges = edges

        # Re-add the original edges to the graph
        for edge in self.original_edges:
            edge not in self.graph.items() and self.graph.addItem(edge)

        self.vertex_edges_backup.clear()
    
    def animate(self, vertex):
        edge_queue: list[tuple[Vertex, Edge]] = []
        visited_vertices = set()
        
        def enqueue_edges(vertex):
            # Check if edge is already part of any tuple in edge_queue
            queued_edges = [queued_edge for _, queued_edge in edge_queue]
            for edge in vertex.edges:
                opposite_vertex = edge.getOpposite(vertex)
                if edge not in queued_edges and opposite_vertex not in visited_vertices:
                    edge_queue.append((vertex, edge))
        
        def animate_next_edge():
            if not edge_queue:
                return  # All edges animated, stop recursion
            
            # Pop the next edge from the queue
            current_vertex, edge = edge_queue.pop(0)
            
            # Play animation for the edge
            start_point = current_vertex.getPosition()
            end_point = edge.getOpposite(current_vertex).getPosition()
            
            edge.play(start_point, end_point)  # Play animation on the edge
            
            # Add the end vertex to visited and enqueue its edges
            end_vertex = edge.getOpposite(current_vertex)
            visited_vertices.add(end_vertex)
            enqueue_edges(end_vertex)
            self.graph.emitSignal()
            
            # Wait for the current edge's animation to complete before animating the next
            QTimer.singleShot(edge.anim_duration, animate_next_edge)
            
        # Initialize queue and visited with the selected vertex
        enqueue_edges(vertex)
        visited_vertices.add(vertex)
        animate_next_edge()  # Start animation sequence