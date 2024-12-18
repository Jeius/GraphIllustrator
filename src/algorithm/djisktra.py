import math

class Djisktra():
    def __init__(self) -> None:
        self.paths = {}
        self.distances = []
        self.start_index = 0

    def run(self, adjacencyMatrix: list[list[float]], start_index: int):
        if len(adjacencyMatrix) == 0:
            raise Exception("No edges found. Please add edges!")
        
        self.start_index = start_index

        n = len(adjacencyMatrix)
        s = set()  # Processed vertices
        d = [math.inf] * n  # Distance array, initialize to infinity
        d[start_index] = 0  # Distance to the start vertex is 0
        predecessors = [None] * n  # Track predecessors to reconstruct paths

        # Step 2: Initialize D array with distances from start
        for i in range(n):
            d[i] = adjacencyMatrix[start_index][i] if i != start_index else 0
            if adjacencyMatrix[start_index][i] < math.inf:
                predecessors[i] = start_index  # Direct connection to start

        s.add(start_index)  # Step 7: Add start vertex to S

        # Repeat for all vertices
        for _ in range(n - 1):
            # Step 8: Find w in V - S such that D[w] is minimum
            w = self._minDistanceVertex(d, s)

            if w is None:
                break  # No more vertices to process

            s.add(w)  # Step 7: Add w to S

            # Step 9: For each v in V - S, update D[v]
            for v in range(n):
                if v not in s:
                    new_dist = d[w] + adjacencyMatrix[w][v]
                    if new_dist < d[v]:
                        d[v] = new_dist
                        predecessors[v] = w  # Update predecessor of v

        # Build paths from predecessors array
        self.paths = self._buildPath(predecessors, start_index)
        self.distances = d
        return self.paths

    def _minDistanceVertex(self, D, S):
        min_distance = math.inf
        min_vertex = None
        for i in range(len(D)):
            if i not in S and D[i] < min_distance:
                min_distance = D[i]
                min_vertex = i
        return min_vertex

    def _buildPath(self, predecessors: list[int], startIndex: int):
        paths = {}
        for v in range(len(predecessors)):
            path = []
            current = v
            visited = set()  # To track visited nodes

            # Backtrack from v to start_id using predecessors
            while current is not None:
                # Check for circular reference
                if current in visited:
                    break
                visited.add(current)

                path.insert(0, current)
                current = predecessors[current]

            if path and path[0] == startIndex:  # Only add the path if it starts at the source
                paths[v] = path
        return paths
    
    def reset(self):
        self.paths.clear()
        self.distances.clear()