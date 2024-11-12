import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .ui.main_window import Ui_MainWindow
from .model.graph import Graph

def loadIcon(path):
    if getattr(sys, 'frozen', False):  # PyInstaller bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level

    file_path = os.path.join(base_path, path)

    if not os.path.exists(file_path):
        print(f"Icon file not found: {file_path}")
        return QIcon()  # Return a default icon if not found

    return QIcon(file_path)

def loadStylesheet(path):
    if getattr(sys, 'frozen', False):  # PyInstaller bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Move up one level

    file_path = os.path.join(base_path, path)

    if not os.path.exists(file_path):
        print(f"Stylesheet file not found: {file_path}")
        return ""  # Return an empty string if the file is missing

    with open(file_path, "r") as file:
        stylesheet = file.read()

    return stylesheet

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(1420, 860)
        self.setStyleSheet(loadStylesheet("style/globals.css"))
        self.setWindowIcon(loadIcon("public/images/icon.webp"))

        self.graph = Graph()
        self.ui.view.setScene(self.graph)

        self.createButtonGroup()
        self.connectSignals()

    def createButtonGroup(self):
        control_panel = self.ui.control_panel

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(control_panel.add_vertex_button)
        self.button_group.addButton(control_panel.add_edge_button)
        self.button_group.addButton(control_panel.delete_button)
        self.button_group.addButton(control_panel.edit_weight_button)
        self.button_group.setExclusive(True)
    
    def connectSignals(self):
        control_panel = self.ui.control_panel
        control_panel.add_vertex_button.toggled.connect(self.setAddingVertex)
        control_panel.add_edge_button.toggled.connect(self.setAddingEdge)
        control_panel.delete_button.toggled.connect(self.setDeleting)
        control_panel.edit_weight_button.toggled.connect(self.setEditWeight)
        control_panel.id_type_combobox.currentIndexChanged.connect(self.setIdType)
        control_panel.clear_button.clicked.connect(self.clearGraph)
        control_panel.tabs.currentChanged.connect(self.setGraphType)
        control_panel.complement_button.clicked.connect(self.getComplement)

        self.graph.graphChanged.connect(self.updateGraphListeners)

    def setAddingVertex(self, adding_vertex: bool):
        self.graph.clearSelection()
        self.graph.is_adding_vertex = adding_vertex

    def setAddingEdge(self, adding_edge: bool):
        self.graph.clearSelection()
        self.graph.is_adding_edge = adding_edge

    def setDeleting(self, deleting: bool):
        self.graph.clearSelection()
        self.graph.is_deleting = deleting

    def setEditWeight(self, editing: bool):
        self.graph.clearSelection()
        self.graph.is_editing_weight = editing

    def setIdType(self, index: int):
        self.graph.clearSelection()
        if index == 0:
            self.graph.is_id_int = True
        else: 
            self.graph.is_id_int = False
        self.graph.emitSignal()
    
    def setGraphType(self, index: int):
        self.unCheckButtonGroup()
        self.graph.clearEdges()

        if index == 0:
            self.graph.setDirectedGraph(True)
        else:
            self.graph.setDirectedGraph(False)

    def getComplement(self):
        self.unCheckButtonGroup()
        self.graph.getComplement()

    def clearGraph(self):
        self.graph.clear()

    def updateGraphListeners(self, graph: Graph):
        self.updateInfoPanel(graph)

    def updateInfoPanel(self, graph: Graph):
        order = len(graph.getVertices())
        size = len(graph.getEdges())
        adj_matrix = graph.adjacencyMatrix

        info_panel = self.ui.info_panel
        info_panel.size_box.setText(str(size))
        info_panel.order_box.setText(str(order))       
        self._updateVertexSet()
        self._updateEdgeSet()

    def _updateVertexSet(self):
        info_panel = self.ui.info_panel
        vertices = self.graph.getVertices()
        vertex_set = []

        for vertex in vertices:
            vertex_set.append(str(vertex.id[1]))

        vertex_set.reverse()
        info_panel.vertex_set_box.clear()
        info_panel.vertex_set_box.setText("V(G) = {" + ', '.join(map(str, vertex_set)) + '}')

    def _updateEdgeSet(self):
        info_panel = self.ui.info_panel
        edges = self.graph.getEdges()
        edge_set = []

        for edge in edges:
            vertexA_id = edge.start_vertex.id[1]
            vertexB_id = edge.end_vertex.id[1]
            edge_set.append(f"({vertexA_id}, {vertexB_id})")

        edge_set.reverse()
        info_panel.edge_set_box.clear()
        info_panel.edge_set_box.setText("E(G) = {" + ', '.join(map(str, edge_set)) + '}')

    def unCheckButtonGroup(self):
        checked_button = self.button_group.checkedButton()

        if checked_button:
            self.button_group.setExclusive(False)
            checked_button.setChecked(False)
            self.button_group.setExclusive(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.unCheckButtonGroup()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec_())
