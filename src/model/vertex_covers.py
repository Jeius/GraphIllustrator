from itertools import combinations
from math import isinf

class VertexCovers:
    def __init__(self, adjacency_matrix):
        """
        Initializes the graph with the given adjacency matrix.
        
        :param adjacency_matrix: 2D list or numpy array with `inf` for unconnected vertices 
                                 and `0` for self-connections.
        """
        self.adj_matrix = adjacency_matrix
        self.num_vertices = len(adjacency_matrix)
        self.edges = self._extract_edges()

    def _extract_edges(self):
        """
        Extracts edges from the adjacency matrix.
        
        :return: List of edges represented as tuples (u, v)
        """
        edges = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if not isinf(self.adj_matrix[i][j]):  # Edge exists if not `inf`
                    edges.append((i, j))
        return edges

    def is_vertex_cover(self, subset):
        """
        Checks if the given subset of vertices is a vertex cover.
        
        :param subset: List of vertices
        :return: True if subset is a vertex cover, False otherwise
        """
        covered_edges = set()
        for vertex in subset:
            for u, v in self.edges:
                if vertex == u or vertex == v:
                    covered_edges.add((u, v))
        return len(covered_edges) == len(self.edges)

    def get(self):
        """
        Finds all vertex covers of the graph.
        
        :return: List of vertex covers (each represented as a list of vertices)
        """
        vertex_covers = []
        vertices = range(self.num_vertices)

        # Check subsets of vertices of increasing size
        for size in range(1, self.num_vertices + 1):
            for subset in combinations(vertices, size):
                if self.is_vertex_cover(subset):
                    vertex_covers.append(list(subset))

        return vertex_covers


# Example usage
if __name__ == "__main__":
    adj_matrix = [
        [0, 1, 1, float('inf')],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [float('inf'), 1, 1, 0],
    ]

    graph = VertexCovers(adj_matrix)
    all_covers = graph.get()
    print("All Vertex Covers:")
    for cover in all_covers:
        print(cover)
