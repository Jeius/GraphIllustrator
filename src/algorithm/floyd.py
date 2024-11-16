import math

class FloydWarshall:
    from ..model.vertex import Vertex

    def __init__(self) -> None:
        self.paths = {}
        self.distances = []

    def findPath(self, adjacencyMatrix: list[list[float]]):
        if not adjacencyMatrix:
            raise Exception("No edges found. Please add edges!")


        n = len(adjacencyMatrix)
        # Initialize the distance and predecessor matrices
        d = [[math.inf] * n for _ in range(n)]
        predecessors = [[None] * n for _ in range(n)]

        # Step 1: Initialize distance and predecessor matrices
        for i in range(n):
            for j in range(n):
                if i == j:
                    d[i][j] = 0
                elif adjacencyMatrix[i][j] < math.inf:
                    d[i][j] = adjacencyMatrix[i][j]
                    predecessors[i][j] = i  # The predecessor of j is i

        # Step 2: Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        predecessors[i][j] = predecessors[k][j]

        # Step 3: Build paths from predecessor matrix
        self.paths = self._buildPaths(predecessors, n)
        self.distances = d
        return self.paths

    def _buildPaths(self, predecessors: list[list[int]], n: int):
        paths = {}
        
        for i in range(n):
            for j in range(n):
                if i != j and predecessors[i][j] is not None:
                    path = []
                    current = j
                    visited = set()  # Track visited nodes to prevent infinite loops

                    # Backtrack from j to i using predecessors
                    while current is not None and current != i:
                        # Check if we've already visited this vertex to avoid circular paths
                        if current in visited:
                            break 
                        visited.add(current)

                        # Insert the current vertex to the path
                        path.insert(0, current)  
                        current = predecessors[i][current]

                    if current == i:
                        path.insert(0, i)  # Insert the start node at the beginning
                        paths[(i, j)] = path  # Store the path from i to j

        return paths

    def reset(self):
        self.paths.clear()
        self.distances.clear()
