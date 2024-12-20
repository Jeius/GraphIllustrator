# Graph Illustrator

## An Interactive Tool for Graph Algorithms and Visualization

### An Activity by

### Julius P. Pahama in

### ITE112 - Algorithmic Graph Theory

Graph Illustrator is a Python-based tool that allows users to visually explore and interact with various graph algorithms, including Prim's, Kruskal's, Dijkstra's, and Floyd-Warshall algorithms. It supports both directed and undirected graphs and offers functionality to display the complement of a graph. Designed for educational purposes, this tool helps users better understand and visualize the workings of key graph algorithms through an intuitive graphical interface.

---

## Features

### Graph Algorithms

- **Prim's Algorithm**: Computes the Minimum Spanning Tree (MST) of a connected, undirected graph.
- **Kruskal's Algorithm**: Finds the MST using a greedy approach, based on edge sorting.
- **Dijkstra's Algorithm**: Determines the shortest paths from a single source vertex to all other vertices in a weighted graph.
- **Floyd-Warshall Algorithm**: Calculates the shortest paths between all pairs of vertices in a graph.
- **Graph Center**: Identifies the center of the graph by locating the vertex or vertices with the minimum eccentricity.
- **Independent Sets**: Determines sets of vertices where no two vertices are adjacent.
- **Vertex Covers**: Finds the minimum set of vertices that covers all edges in the graph.
- **Graph Complement**: Visualizes the complement of a graph, where edges are inverted between existing and non-existing connections.

### Directed and Undirected Graphs

Switch seamlessly between directed and undirected graph representations, with full algorithm support for each type.

### Interactive Interface

- Add and remove vertices and edges with ease.
- Execute algorithms visually for better understanding.
- Explore results interactively within the graphical interface.

---

## Installation and Setup

### Prerequisites

- Install **Miniconda** or **Anaconda** globally on your machine. Miniconda is recommended for its lightweight setup.

### Step-by-Step Guide

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Create and Activate Conda Environment**
   Use the provided `environment.yaml` file to create a new Conda environment:

   ```bash
   conda env create -f environment.yaml
   conda activate graph-illustrator
   ```

3. **Install Additional Dependencies (if necessary)**
   If new dependencies are added, update the environment:

   ```bash
   conda env update -f environment.yaml
   ```

4. **Run the Project**
   Start the application using the `run.bat` file:

   ```bash
   run.bat
   ```

5. **Build the Executable**
   Package the project into an executable using the `build.bat` file. PyInstaller is used for the build process:
   ```bash
   build.bat
   ```
   After building, the executable will be located in the `dist` folder.

---

## How to Use

1. Launch the application by running `run.bat`.
2. Use the graphical interface to:
   - Add or remove vertices and edges.
   - Select and execute graph algorithms from the available options.
   - Switch between directed and undirected graph representations.
3. Explore advanced features such as:
   - Finding the graph center.
   - Identifying independent sets and vertex covers.
   - Visualizing the graph's complement.

---

## Contributions

Contributions are welcome! If you would like to contribute:

- Submit a pull request.
- Report issues via the GitHub repository.

---

## License

This project is licensed under the [MIT License](LICENSE).
