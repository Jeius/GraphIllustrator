# Graph Illustrator

### An Activity of

### Julius P. Pahama in

### ITE112 - Algorithmic Graph Theory

Graph Illustrator is a Python-based tool that allows you to visually explore and interact with graph algorithms, including Prim's, Kruskal's, Dijkstra's, and Floyd-Warshall algorithms. It supports directed and undirected graphs and provides functionality for displaying the complement of a graph. This tool is designed to help users better understand and visualize the workings of key graph algorithms in a graphical interface.

## Features

### Graph Algorithms:

- **Prim's Algorithm**: Computes the Minimum Spanning Tree (MST) of a connected, undirected graph.
- **Kruskal's Algorithm**: Another approach to finding the Minimum Spanning Tree, based on edge sorting.
- **Dijkstra's Algorithm**: Finds the shortest paths from a single source vertex to all other vertices in a weighted graph.
- **Floyd-Warshall Algorithm**: Computes the shortest paths between all pairs of vertices in a graph.
- **Graph Center**: Identifies the center of the graph by finding the vertex or vertices with minimum eccentricity.
- **Independent Sets**: Determines sets of vertices such that no two vertices are adjacent.
- **Vertex Covers**: Finds the minimum set of vertices that covers all edges in the graph.
- **Graph Complement**: Easily visualize the complement of a given graph, where edges are flipped between existing and non-existing connections.

### Directed and Undirected Graphs:

Switch between directed and undirected graph representations with full support for the corresponding algorithms.

### Interactive Interface:

The tool provides a graphical interface to interact with the graph, add/remove vertices and edges, and run the algorithms visually.

## Installation and Setup

### Prerequisites

- Install **Miniconda** or **Anaconda** globally on your machine. Miniconda is recommended for its lightweight setup.

### Step-by-Step Guide

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Create and Activate Conda Environment:**
   Create a new Conda environment using the `environment.yaml` file provided:

   ```bash
   conda env create -f environment.yaml
   conda activate graph-illustrator
   ```

3. **Install Additional Dependencies (if necessary):**
   If new dependencies are added to the project:

   ```bash
   conda env update -f environment.yaml
   ```

4. **Run the Project:**
   Use the `run.bat` file to start the application:

   ```bash
   run.bat
   ```

5. **Build the Executable:**
   To build the project into an executable, use the `build.bat` file. This uses PyInstaller to package the application:
   ```bash
   build.bat
   ```
   After building, the executable can be found in the `dist` folder.

## How to Use

1. Launch the application by running `run.bat`.
2. Use the graphical interface to add or remove vertices and edges.
3. Select and execute graph algorithms from the available options.
4. Switch between directed and undirected graphs as needed.
5. Explore advanced features like finding graph centers, independent sets, and vertex covers.
6. Visualize the complement of the graph for better understanding of connections.

## Contributions

Contributions are welcome! Please feel free to submit a pull request or report issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
