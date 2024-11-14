
import math


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


class Kruskal():

    def MCST(self, adj_matrix):
        """
        Kruskal's Algorithm for Minimum Spanning Tree using an adjacency matrix.
        
        :param adj_matrix: 2D list representing the adjacency matrix of the graph.
                        adj_matrix[i][j] is the weight of the edge between i and j,
                        or math.inf if no edge exists.
        :return: A list of edges (u, v, weight) that form the MST.
        """
        n = len(adj_matrix)
        edges = []
        
        # Convert adjacency matrix to edge list
        for i in range(n):
            for j in range(i + 1, n):  # Avoid duplicate edges by only iterating j > i
                if adj_matrix[i][j] != math.inf:
                    edges.append((adj_matrix[i][j], i, j))
        
        # Sort edges by weight
        edges.sort()
        uf = UnionFind(n)
        mst_edges = []
        
        for weight, u, v in edges:
            if uf.find(u) != uf.find(v):
                uf.union(u, v)
                mst_edges.append((u, v, weight))
        
        return mst_edges