import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .ui.main_window import Ui_MainWindow
from .model.graph import Graph

def getFilePath(path):
    """Constructs the file path based on the running environment."""
    if getattr(sys, 'frozen', False):  # PyInstaller bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level
    return os.path.join(base_path, path)

def loadIcon(path):
    file_path = getFilePath(path)

    if not os.path.exists(file_path):
        print(f"Icon file not found: {file_path}")
        return QIcon()

    return QIcon(file_path)

def loadStylesheet(path):
    file_path = getFilePath(path)

    if not os.path.exists(file_path):
        print(f"Stylesheet file not found: {file_path}")
        return ""  

    with open(file_path, "r") as file:
        stylesheet = file.read()

    return stylesheet


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(1400, 820)
        self.setStyleSheet(loadStylesheet("style/globals.css"))
        self.setWindowIcon(loadIcon("public/images/icon.webp"))
        self.setWindowTitle("Graph Illustrator by Julius Pahama")

        self.graph = Graph()
        self.ui.view.setScene(self.graph)

        self._setupButtonGroup()
        self._setupPathTable()
        self._setupConnections()
        
    def _setupButtonGroup(self):
        control_panel = self.ui.control_panel

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(control_panel.add_vertex_button)
        self.button_group.addButton(control_panel.add_edge_button)
        self.button_group.addButton(control_panel.delete_button)
        self.button_group.addButton(control_panel.edit_weight_button)
        self.button_group.addButton(control_panel.complement_button)
        self.button_group.setExclusive(True)
    
    def _setupPathTable(self):
        path_table = self.ui.info_panel.path_table

        horizontalHeaders = ["Start", "Goal", "Distance"]
        columns = len(horizontalHeaders)

        path_table.setColumnCount(columns)
        path_table.setHorizontalHeaderLabels(horizontalHeaders)
        path_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        path_table.verticalHeader().sectionClicked.connect(self.onTableRowClicked)

    def _setupConnections(self):
        control_panel = self.ui.control_panel
        control_panel.add_vertex_button.toggled.connect(self.setAddingVertex)
        control_panel.add_edge_button.toggled.connect(self.setAddingEdge)
        control_panel.delete_button.toggled.connect(self.setDeleting)
        control_panel.edit_weight_button.toggled.connect(self.setEditWeight)
        control_panel.id_type_combobox.currentIndexChanged.connect(self.setIdType)
        control_panel.clear_button.clicked.connect(self.clearGraph)
        control_panel.clear_edges_button.clicked.connect(self.onClearEdgesClicked)
        control_panel.tabs.currentChanged.connect(self.setGraphType)
        control_panel.complement_button.toggled.connect(self.onComplementToggled)
        control_panel.floyd_radio.toggled.connect(self.setFloyd)
        control_panel.dijkstra_radio.toggled.connect(self.setDijkstra)
        control_panel.prim_radio.toggled.connect(self.setPrim)
        control_panel.kruskal_radio.toggled.connect(self.setKruskal)
        control_panel.path_button.clicked.connect(self.onPathButtonClicked)
        control_panel.mcst_button.clicked.connect(self.onMCSTClicked)

        self.ui.view.tool.revert_button.clicked.connect(self.onRevertButtonClicked)
        self.ui.view.tool.done_button.clicked.connect(self.onDoneClicked)
        
        self.graph.graphChanged.connect(self._updateGraphListeners)

#-------------------------------- Slots ------------------------------------#
    def setAddingVertex(self, adding_vertex: bool):
        self.graph.clearSelection()
        self.graph.is_adding_vertex = adding_vertex
        if adding_vertex:
            self.graph.resetPaths()
            self.ui.view.tool.done_button.show()

    def setAddingEdge(self, adding_edge: bool):
        self.graph.clearSelection()
        self.graph.is_adding_edge = adding_edge
        if adding_edge:
            self.graph.resetPaths()
            self.ui.view.tool.done_button.show()
        elif self.graph.indicator_line in self.graph.items():
            self.graph.removeItem(self.graph.indicator_line)

    def setDeleting(self, deleting: bool):
        self.graph.clearSelection()
        self.graph.is_deleting = deleting
        if deleting:
            self.graph.resetPaths()
            self.ui.view.tool.done_button.show()

    def setEditWeight(self, editing: bool):
        self.graph.clearSelection()
        self.graph.is_editing_weight = editing
        if editing:
            self.graph.resetPaths()
            self.ui.view.tool.done_button.show()

    def setIdType(self, index: int):
        self.graph.clearSelection()
        if index == 0:
            self.graph.is_id_int = True
        else: 
            self.graph.is_id_int = False
        self.graph.emitSignal()
    
    def setGraphType(self, index: int):
        self._unCheckButtonGroup()
        self.graph.clearEdges()

        if index == 0:
            self.graph.setDirectedGraph(True)
        else:
            self.graph.setDirectedGraph(False)

    def setFloyd(self, is_floyd: bool):
        self._unCheckButtonGroup()
        self.graph.setFloyd(is_floyd)

    def setDijkstra(self, is_dijsktra: bool):
        self._unCheckButtonGroup()
        self.graph.setDijkstra(is_dijsktra)

    def setPrim(self, is_prim: bool):
        self._unCheckButtonGroup()
        self.graph.setPrim(is_prim)

    def setKruskal(self, is_kruskal: bool):
        self._unCheckButtonGroup()
        self.graph.setKruskal(is_kruskal)

    def onTableRowClicked(self, index: int):
        path_table = self.ui.info_panel.path_table
        vertices = self.graph.getVertices()
        start_item = path_table.item(index, 0)
        goal_item = path_table.item(index, 1)

        start_id = start_item.text()
        goal_id = goal_item.text()

        start_vertex = next((v for v in vertices if v.id[1] == start_id), None)
        goal_vertex = next((v for v in vertices if v.id[1] == goal_id), None)

        self.graph.showPath(start_vertex, goal_vertex)
        self.ui.view.tool.revert_button.show()

    def onDoneClicked(self):
        self._unCheckButtonGroup()
    
    def onMCSTClicked(self):
        self._unCheckButtonGroup()
        self.ui.view.tool.revert_button.show()
        self.graph.findMCST()
        self.graph.emitSignal()

    def onComplementToggled(self, is_toggled):
        self.graph.getComplement(is_toggled)
        if is_toggled:
            self.ui.view.tool.done_button.show()

    def clearGraph(self):
        self.graph.clear()

    def onPathButtonClicked(self):
        self.graph.findPath()
        self._updatePathTable()
        self._unCheckButtonGroup()

    def onRevertButtonClicked(self):
        self.graph.revert()
        self.ui.view.tool.revert_button.hide()
        self.ui.info_panel.path_table.clearSelection()

    def onClearEdgesClicked(self):
        self.graph.clearEdges()


#------------------- Signal Listeners ---------------------------------#
    def _updateGraphListeners(self):
        self._updateInfoPanel()

    def _updateControlPanel(self):
        mcst = self.graph.mcst
        control_panel = self.ui.control_panel
        control_panel.mcst_textbox.clear()
        if mcst:
            control_panel.mcst_textbox.setText(mcst)

    def _updateInfoPanel(self):
        graph = self.graph
        order = len(graph.getVertices())
        size = len(graph.getEdges())

        info_panel = self.ui.info_panel
        info_panel.size_box.setText(str(size))
        info_panel.order_box.setText(str(order))       
        self._updateVertexSet()
        self._updateEdgeSet()
        self._updateMatrix()
        self._updatePathTable()

    def _updateVertexSet(self):
        info_panel = self.ui.info_panel
        info_panel.vertex_set_box.clear()
        vertices = self.graph.getVertices()

        vertex_set = [str(vertex.id[1]) for vertex in vertices]
        vertex_set.sort()
        if vertex_set:
            info_panel.vertex_set_box.setPlainText("V(G) = {" + ', '.join(map(str, vertex_set)) + '}')

    def _updateEdgeSet(self):
        info_panel = self.ui.info_panel
        edges = self.graph.getEdges()
        info_panel.edge_set_box.clear()

        edge_set = []
        for edge in edges:
            start_id = edge.start_vertex.id[1]
            end_id = edge.end_vertex.id[1]
            edge_set.append(f"({start_id}, {end_id})")
        
        if edge_set:
            info_panel.edge_set_box.setPlainText("E(G) = {" + ', '.join(map(str, edge_set)) + '}')

    def _updateMatrix(self):
        table = self.ui.info_panel.adj_matrix_table
        table.clear()
        matrix = self.graph.adjacencyMatrix

        table.setRowCount(len(matrix))
        table.setColumnCount(len(matrix[0]) if matrix else 0)

        for rowIndex, row in enumerate(matrix):
            for columnIndex, value in enumerate(row):
                item = QTableWidgetItem(str(value))  
                table.setItem(rowIndex, columnIndex, item)
                table.setColumnWidth(columnIndex, 1)

    def _updatePathTable(self):
        path_table = self.ui.info_panel.path_table
        
        if self.graph.is_directed_graph:
            self.ui.info_panel.path_table_widget.show()
        else:
            self.ui.info_panel.path_table_widget.hide()
    
        # Clear the table first
        path_table.setRowCount(0)

        if not self.graph.getEdges():
            return

        vertices = self.graph.getVertices()

        # Get paths, distances, and vertices based on the algorithm
        if self.graph.is_using_dijkstra:
            paths = self.graph.dijkstra.paths
            distances = self.graph.dijkstra.distances
            start_vertex = vertices[self.graph.dijkstra.start_index]
            rows = len(vertices) - 1 if vertices else 0

        elif self.graph.is_using_floyd:
            paths = self.graph.floyd.paths
            distances = self.graph.floyd.distances
            rows = len(vertices) * (len(vertices) - 1)
            
        else:
            return

        # If paths are empty, there's nothing to display
        if not paths:
            return

        # Set row count and headers
        vertical_headers = ["Show Path"] * rows
        path_table.setRowCount(rows)
        path_table.setVerticalHeaderLabels(vertical_headers)

        # Populate the table with paths and distances
        rowIndex = 0
        if self.graph.is_using_dijkstra:
            rowIndex = self._seedPathTable(distances, rowIndex, start_vertex)
        elif self.graph.is_using_floyd:
            for start in vertices:
                rowIndex = self._seedPathTable(distances, rowIndex, start)

    def _seedPathTable(self, distances, rowIndex, start_vertex):
        vertices = self.graph.getVertices()
        path_table = self.ui.info_panel.path_table

        for goal_vertex in vertices:
            if start_vertex != goal_vertex:
                start_index = vertices.index(start_vertex)
                goal_index = vertices.index(goal_vertex)

                # Create table items
                start_item = QTableWidgetItem(start_vertex.id[1])
                start_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                goal_item = QTableWidgetItem(goal_vertex.id[1])
                goal_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                # Get the appropriate distance
                distance = (
                        distances[goal_index] if self.graph.is_using_dijkstra 
                        else distances[start_index][goal_index]
                    )
                distance_item = QTableWidgetItem(str(distance))
                distance_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                # Set items in the table
                path_table.setItem(rowIndex, 0, start_item)
                path_table.setItem(rowIndex, 1, goal_item)
                path_table.setItem(rowIndex, 2, distance_item)
                rowIndex += 1
        return rowIndex

    def _unCheckButtonGroup(self):
        self.ui.view.tool.done_button.hide()
        checked_button = self.button_group.checkedButton()

        if checked_button:
            self.button_group.setExclusive(False)
            checked_button.setChecked(False)
            self.button_group.setExclusive(True)



#----------------- Event Listeners ---------------------------------#
    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key_Escape:
            self._unCheckButtonGroup()
            self.ui.view.tool.done_button.hide()
        
        elif a0.key() == Qt.Key_Z and a0.modifiers() & Qt.ControlModifier:
            self.graph.undo()
        
        elif a0.key() == Qt.Key_Y and a0.modifiers() & Qt.ControlModifier:
            self.graph.redo()
        return super().keyPressEvent(a0)



#----------------------- main ----------------------------------------#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec_())
