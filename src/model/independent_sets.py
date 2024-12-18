import math


class IndependentSets:
    def __init__(self, adjacency_matrix):
        """
        Initializes the Graph with an adjacency matrix.

        Args:
            adjacency_matrix (list): A 2D list (matrix) representing the graph.
                                      matrix[i][j] = inf if there's no edge between node i and node j, otherwise some cost/weight.
        """
        self.graph = adjacency_matrix
        self.nodes = list(range(len(adjacency_matrix)))
        self.independent_sets = []

    def is_independent_set(self, candidate_set):
        """
        Checks if the candidate set is independent.

        Args:
            candidate_set (list): A list of vertices to check.

        Returns:
            bool: True if the set is independent, False otherwise.
        """
        for i in candidate_set:
            for j in candidate_set:
                if i != j and not math.isinf(self.graph[i][j]): 
                    return False
        return True

    def get(self):
        """
        Finds all maximal independent sets in the graph using a backtracking approach.

        Returns:
            list: A list of independent sets, each represented as a set of vertices.
        """
        def backtrack(node, current_set):
            # If we've processed all nodes
            if node >= len(self.nodes):
                self.independent_sets.append(set(current_set))
                return

            # Include the current node in the set
            current_set.append(self.nodes[node])
            if self.is_independent_set(current_set):
                backtrack(node + 1, current_set)
            current_set.pop()  # Backtrack

            # Exclude the current node and move forward
            backtrack(node + 1, current_set)

        self.independent_sets = []
        backtrack(0, [])
        return self.independent_sets
