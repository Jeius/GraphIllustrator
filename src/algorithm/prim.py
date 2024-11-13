import heapq
import math

class Prim():
    def getMCST(self, adj_matrix, start=0):
        """
        Prim's Algorithm for Minimum Spanning Tree using an adjacency matrix.
        
        :param adj_matrix: 2D list representing the adjacency matrix of the graph.
                        adj_matrix[i][j] is the weight of the edge between i and j,
                        or math.inf if no edge exists.
        :param start: Starting node for Prim's algorithm.
        :return: A list of edges (u, v, weight) that form the MST.
        """
        n = len(adj_matrix)
        mst_edges = []
        visited = [False] * n
        min_heap = [(0, start, start)]  # Initialize with (weight, from_node, to_node)
        
        while min_heap and len(mst_edges) < n - 1:
            weight, u, v = heapq.heappop(min_heap)
            
            if visited[v]:
                continue
            
            visited[v] = True
            if u != v:  # Avoid adding the starting point to itself
                mst_edges.append((u, v, weight))
            
            for neighbor in range(n):
                if not visited[neighbor] and adj_matrix[v][neighbor] != math.inf:
                    heapq.heappush(min_heap, (adj_matrix[v][neighbor], v, neighbor))
        
        return mst_edges

