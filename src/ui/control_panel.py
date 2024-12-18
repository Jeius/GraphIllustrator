from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_ControlPanel(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        
    def setupUi(self, ControlPanel):
        if not ControlPanel.objectName():
            ControlPanel.setObjectName(u"ControlPanel")
        ControlPanel.resize(1133, 165)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ControlPanel.sizePolicy().hasHeightForWidth())
        ControlPanel.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(ControlPanel)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.add_box = QGroupBox(ControlPanel)
        self.add_box.setObjectName(u"add_box")
        self.gridLayout_3 = QGridLayout(self.add_box)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.id_type_label = QLabel(self.add_box)
        self.id_type_label.setObjectName(u"id_type_label")

        self.gridLayout_3.addWidget(self.id_type_label, 1, 0, 1, 1, Qt.AlignRight)

        self.id_type_combobox = QComboBox(self.add_box)
        self.id_type_combobox.addItem("")
        self.id_type_combobox.addItem("")
        self.id_type_combobox.setObjectName(u"id_type_combobox")
        self.id_type_combobox.setMinimumSize(QSize(80, 30))
        self.id_type_combobox.setAutoFillBackground(False)
        self.id_type_combobox.setFrame(True)

        self.gridLayout_3.addWidget(self.id_type_combobox, 1, 1, 1, 1)

        self.add_edge_button = QPushButton(self.add_box)
        self.add_edge_button.setObjectName(u"add_edge_button")
        self.add_edge_button.setMinimumSize(QSize(100, 30))
        self.add_edge_button.setMaximumSize(QSize(200, 16777215))
        self.add_edge_button.setCheckable(True)

        self.gridLayout_3.addWidget(self.add_edge_button, 0, 1, 1, 1)

        self.add_vertex_button = QPushButton(self.add_box)
        self.add_vertex_button.setObjectName(u"add_vertex_button")
        self.add_vertex_button.setMinimumSize(QSize(100, 30))
        self.add_vertex_button.setMaximumSize(QSize(200, 16777215))
        self.add_vertex_button.setCheckable(True)

        self.gridLayout_3.addWidget(self.add_vertex_button, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.add_box)

        self.line_3 = QFrame(ControlPanel)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.edit_box = QGroupBox(ControlPanel)
        self.edit_box.setObjectName(u"edit_box")
        self.gridLayout_6 = QGridLayout(self.edit_box)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.edit_weight_button = QPushButton(self.edit_box)
        self.edit_weight_button.setObjectName(u"edit_weight_button")
        self.edit_weight_button.setMinimumSize(QSize(80, 30))
        self.edit_weight_button.setMaximumSize(QSize(120, 16777215))
        self.edit_weight_button.setCheckable(True)

        self.gridLayout_6.addWidget(self.edit_weight_button, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.edit_box)

        self.line_5 = QFrame(ControlPanel)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.delete_box = QGroupBox(ControlPanel)
        self.delete_box.setObjectName(u"delete_box")
        self.gridLayout_5 = QGridLayout(self.delete_box)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.delete_button = QPushButton(self.delete_box)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setMinimumSize(QSize(80, 30))
        self.delete_button.setMaximumSize(QSize(120, 16777215))
        self.delete_button.setCheckable(True)

        self.gridLayout_5.addWidget(self.delete_button, 0, 0, 1, 1)

        self.clear_button = QPushButton(self.delete_box)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setMinimumSize(QSize(80, 30))
        self.clear_button.setMaximumSize(QSize(120, 16777215))
        self.clear_button.setStyleSheet(u"QPushButton {background-color: #bf3434; color: white; border: 1px solid #70707c; padding: 5px 12px; border-radius: 5px;} QPushButton:hover {background-color: #d44b4b;}")

        self.gridLayout_5.addWidget(self.clear_button, 2, 0, 1, 1)

        self.clear_edges_button = QPushButton(self.delete_box)
        self.clear_edges_button.setObjectName(u"clear_edges_button")
        self.clear_edges_button.setMinimumSize(QSize(80, 30))
        self.clear_edges_button.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_5.addWidget(self.clear_edges_button, 1, 0, 1, 1)

        self.clear_button.raise_()
        self.delete_button.raise_()
        self.clear_edges_button.raise_()

        self.horizontalLayout.addWidget(self.delete_box)

        self.line = QFrame(ControlPanel)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.tabs = QTabWidget(ControlPanel)
        self.tabs.setObjectName(u"tabs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy1)
        self.tabs.setMaximumSize(QSize(800, 16777215))
        self.tabs.setStyleSheet(u"QFrame { border-radius: 5px; background-color: #3b3b3d} QPushButton, QLineEdit {background-color: #2b2b2c; border-color: #70707c;} QPushButton:hover, QPushButton:checked { background-color: #545454;}")
        self.tabs.setMovable(True)
        self.directed_tab = QWidget()
        self.directed_tab.setObjectName(u"directed_tab")
        self.horizontalLayout_8 = QHBoxLayout(self.directed_tab)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.d_algorithm_box = QGroupBox(self.directed_tab)
        self.d_algorithm_box.setObjectName(u"d_algorithm_box")
        self.d_algorithm_box.setMinimumSize(QSize(100, 0))
        self.d_algorithm_box.setMaximumSize(QSize(288, 16777215))
        self.d_algorithm_box.setStyleSheet(u"")
        self.d_algorithm_box.setFlat(False)
        self.gridLayout_4 = QGridLayout(self.d_algorithm_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.dijkstra_radio = QRadioButton(self.d_algorithm_box)
        self.dijkstra_radio.setObjectName(u"dijkstra_radio")
        self.dijkstra_radio.setChecked(True)

        self.gridLayout_4.addWidget(self.dijkstra_radio, 0, 0, 1, 1)

        self.floyd_radio = QRadioButton(self.d_algorithm_box)
        self.floyd_radio.setObjectName(u"floyd_radio")
        self.floyd_radio.setChecked(False)

        self.gridLayout_4.addWidget(self.floyd_radio, 1, 0, 1, 1)


        self.horizontalLayout_8.addWidget(self.d_algorithm_box)

        self.path_finding_box = QGroupBox(self.directed_tab)
        self.path_finding_box.setObjectName(u"path_finding_box")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.path_finding_box.sizePolicy().hasHeightForWidth())
        self.path_finding_box.setSizePolicy(sizePolicy2)
        self.path_finding_box.setMaximumSize(QSize(160, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.path_finding_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.path_button = QPushButton(self.path_finding_box)
        self.path_button.setObjectName(u"path_button")
        sizePolicy.setHeightForWidth(self.path_button.sizePolicy().hasHeightForWidth())
        self.path_button.setSizePolicy(sizePolicy)
        self.path_button.setMinimumSize(QSize(0, 30))

        self.verticalLayout_2.addWidget(self.path_button)


        self.horizontalLayout_8.addWidget(self.path_finding_box)

        self.center_group = QGroupBox(self.directed_tab)
        self.center_group.setObjectName(u"center_group")
        self.center_group.setMaximumSize(QSize(160, 16777215))
        self.gridLayout_8 = QGridLayout(self.center_group)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.center_label = QLabel(self.center_group)
        self.center_label.setObjectName(u"center_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.center_label.sizePolicy().hasHeightForWidth())
        self.center_label.setSizePolicy(sizePolicy3)
        self.center_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.center_label, 0, 0, 1, 1)

        self.center_field = QLineEdit(self.center_group)
        self.center_field.setObjectName(u"center_field")
        sizePolicy.setHeightForWidth(self.center_field.sizePolicy().hasHeightForWidth())
        self.center_field.setSizePolicy(sizePolicy)
        self.center_field.setMinimumSize(QSize(0, 32))
        self.center_field.setMaximumSize(QSize(16777215, 16777215))
        self.center_field.setReadOnly(True)

        self.gridLayout_8.addWidget(self.center_field, 0, 1, 1, 1)

        self.find_center_button = QPushButton(self.center_group)
        self.find_center_button.setObjectName(u"find_center_button")
        self.find_center_button.setMinimumSize(QSize(0, 30))

        self.gridLayout_8.addWidget(self.find_center_button, 1, 0, 1, 2)


        self.horizontalLayout_8.addWidget(self.center_group)

        self.tabs.addTab(self.directed_tab, "")
        self.undirected_tab = QWidget()
        self.undirected_tab.setObjectName(u"undirected_tab")
        sizePolicy2.setHeightForWidth(self.undirected_tab.sizePolicy().hasHeightForWidth())
        self.undirected_tab.setSizePolicy(sizePolicy2)
        self.horizontalLayout_3 = QHBoxLayout(self.undirected_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ud_algorithm_box = QGroupBox(self.undirected_tab)
        self.ud_algorithm_box.setObjectName(u"ud_algorithm_box")
        self.ud_algorithm_box.setMinimumSize(QSize(100, 0))
        self.ud_algorithm_box.setMaximumSize(QSize(288, 16777215))
        self.gridLayout = QGridLayout(self.ud_algorithm_box)
        self.gridLayout.setObjectName(u"gridLayout")
        self.prim_radio = QRadioButton(self.ud_algorithm_box)
        self.prim_radio.setObjectName(u"prim_radio")
        self.prim_radio.setChecked(True)

        self.gridLayout.addWidget(self.prim_radio, 0, 0, 1, 1)

        self.kruskal_radio = QRadioButton(self.ud_algorithm_box)
        self.kruskal_radio.setObjectName(u"kruskal_radio")

        self.gridLayout.addWidget(self.kruskal_radio, 1, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.ud_algorithm_box)

        self.mcst_box = QGroupBox(self.undirected_tab)
        self.mcst_box.setObjectName(u"mcst_box")
        sizePolicy2.setHeightForWidth(self.mcst_box.sizePolicy().hasHeightForWidth())
        self.mcst_box.setSizePolicy(sizePolicy2)
        self.mcst_box.setMaximumSize(QSize(160, 16777215))
        self.gridLayout_2 = QGridLayout(self.mcst_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.mcst_button = QPushButton(self.mcst_box)
        self.mcst_button.setObjectName(u"mcst_button")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.mcst_button.sizePolicy().hasHeightForWidth())
        self.mcst_button.setSizePolicy(sizePolicy4)
        self.mcst_button.setMinimumSize(QSize(0, 30))
        self.mcst_button.setCheckable(True)

        self.gridLayout_2.addWidget(self.mcst_button, 1, 0, 1, 1, Qt.AlignVCenter)

        self.mcst_form = QWidget(self.mcst_box)
        self.mcst_form.setObjectName(u"mcst_form")
        self.horizontalLayout_2 = QHBoxLayout(self.mcst_form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.mcst_form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.mcst_textbox = QLineEdit(self.mcst_form)
        self.mcst_textbox.setObjectName(u"mcst_textbox")
        self.mcst_textbox.setMinimumSize(QSize(0, 32))

        self.horizontalLayout_2.addWidget(self.mcst_textbox)


        self.gridLayout_2.addWidget(self.mcst_form, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_3.addWidget(self.mcst_box)

        self.independent_group = QGroupBox(self.undirected_tab)
        self.independent_group.setObjectName(u"independent_group")
        self.independent_group.setMaximumSize(QSize(160, 16777215))
        self.gridLayout_7 = QGridLayout(self.independent_group)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.independence_num_label = QLabel(self.independent_group)
        self.independence_num_label.setObjectName(u"independence_num_label")
        self.independence_num_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.independence_num_label, 0, 0, 1, 1)

        self.independence_num_field = QLineEdit(self.independent_group)
        self.independence_num_field.setObjectName(u"independence_num_field")
        self.independence_num_field.setMinimumSize(QSize(0, 32))

        self.gridLayout_7.addWidget(self.independence_num_field, 0, 1, 1, 1)

        self.show_IS_button = QPushButton(self.independent_group)
        self.show_IS_button.setObjectName(u"show_IS_button")
        self.show_IS_button.setMinimumSize(QSize(0, 30))

        self.gridLayout_7.addWidget(self.show_IS_button, 1, 0, 1, 2)


        self.horizontalLayout_3.addWidget(self.independent_group)

        self.cover_group = QGroupBox(self.undirected_tab)
        self.cover_group.setObjectName(u"cover_group")
        self.cover_group.setMaximumSize(QSize(160, 16777215))
        self.gridLayout_9 = QGridLayout(self.cover_group)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.v_cover_button = QPushButton(self.cover_group)
        self.v_cover_button.setObjectName(u"v_cover_button")
        self.v_cover_button.setMinimumSize(QSize(0, 30))

        self.gridLayout_9.addWidget(self.v_cover_button, 1, 0, 1, 2)

        self.v_cover_field = QLineEdit(self.cover_group)
        self.v_cover_field.setObjectName(u"v_cover_field")
        self.v_cover_field.setMinimumSize(QSize(0, 32))

        self.gridLayout_9.addWidget(self.v_cover_field, 0, 1, 1, 1)

        self.v_cover_label = QLabel(self.cover_group)
        self.v_cover_label.setObjectName(u"v_cover_label")
        self.v_cover_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.v_cover_label, 0, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.cover_group)

        self.complement_box = QGroupBox(self.undirected_tab)
        self.complement_box.setObjectName(u"complement_box")
        sizePolicy2.setHeightForWidth(self.complement_box.sizePolicy().hasHeightForWidth())
        self.complement_box.setSizePolicy(sizePolicy2)
        self.complement_box.setMaximumSize(QSize(160, 16777215))
        self.verticalLayout = QVBoxLayout(self.complement_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.complement_button = QPushButton(self.complement_box)
        self.complement_button.setObjectName(u"complement_button")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.complement_button.sizePolicy().hasHeightForWidth())
        self.complement_button.setSizePolicy(sizePolicy5)
        self.complement_button.setMinimumSize(QSize(0, 30))
        self.complement_button.setCheckable(True)

        self.verticalLayout.addWidget(self.complement_button, 0, Qt.AlignHCenter)


        self.horizontalLayout_3.addWidget(self.complement_box)

        self.tabs.addTab(self.undirected_tab, "")

        self.horizontalLayout.addWidget(self.tabs)


        self.retranslateUi(ControlPanel)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ControlPanel)
    # setupUi

    def retranslateUi(self, ControlPanel):
        ControlPanel.setWindowTitle(QCoreApplication.translate("ControlPanel", u"ControlPanel", None))
        self.add_box.setTitle(QCoreApplication.translate("ControlPanel", u"Add", None))
        self.id_type_label.setText(QCoreApplication.translate("ControlPanel", u"Vertex ID type:", None))
        self.id_type_combobox.setItemText(0, QCoreApplication.translate("ControlPanel", u"Integer", None))
        self.id_type_combobox.setItemText(1, QCoreApplication.translate("ControlPanel", u"Character", None))

#if QT_CONFIG(whatsthis)
        self.id_type_combobox.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.add_edge_button.setText(QCoreApplication.translate("ControlPanel", u"Add Edge", None))
        self.add_vertex_button.setText(QCoreApplication.translate("ControlPanel", u"Add Vertex", None))
        self.edit_box.setTitle(QCoreApplication.translate("ControlPanel", u"Edit", None))
        self.edit_weight_button.setText(QCoreApplication.translate("ControlPanel", u"Edit Weight", None))
        self.delete_box.setTitle(QCoreApplication.translate("ControlPanel", u"Delete", None))
        self.delete_button.setText(QCoreApplication.translate("ControlPanel", u"Delete One", None))
        self.clear_button.setText(QCoreApplication.translate("ControlPanel", u"Clear All", None))
        self.clear_edges_button.setText(QCoreApplication.translate("ControlPanel", u"Clear Edges", None))
        self.d_algorithm_box.setTitle(QCoreApplication.translate("ControlPanel", u"Algorithms", None))
        self.dijkstra_radio.setText(QCoreApplication.translate("ControlPanel", u"Dijkstra", None))
        self.floyd_radio.setText(QCoreApplication.translate("ControlPanel", u"Floyd Warshal", None))
        self.path_finding_box.setTitle(QCoreApplication.translate("ControlPanel", u"Path Finding", None))
        self.path_button.setText(QCoreApplication.translate("ControlPanel", u"Find Path", None))
        self.center_group.setTitle(QCoreApplication.translate("ControlPanel", u"Graph Center", None))
        self.center_label.setText(QCoreApplication.translate("ControlPanel", u"Center", None))
        self.find_center_button.setText(QCoreApplication.translate("ControlPanel", u"Find Center", None))
        self.tabs.setTabText(self.tabs.indexOf(self.directed_tab), QCoreApplication.translate("ControlPanel", u"Directed Graph", None))
        self.ud_algorithm_box.setTitle(QCoreApplication.translate("ControlPanel", u"Algorithms", None))
        self.prim_radio.setText(QCoreApplication.translate("ControlPanel", u"Prim", None))
        self.kruskal_radio.setText(QCoreApplication.translate("ControlPanel", u"Kruskal", None))
        self.mcst_box.setTitle(QCoreApplication.translate("ControlPanel", u"Minimum Cost Spanning Tree", None))
        self.mcst_button.setText(QCoreApplication.translate("ControlPanel", u"Find MCST", None))
        self.label.setText(QCoreApplication.translate("ControlPanel", u"Minimum Cost", None))
        self.independent_group.setTitle(QCoreApplication.translate("ControlPanel", u"Independent Set (IS)", None))
        self.independence_num_label.setText(QCoreApplication.translate("ControlPanel", u"	\u03b1(G)", None))
        self.show_IS_button.setText(QCoreApplication.translate("ControlPanel", u"Find IS", None))
        self.cover_group.setTitle(QCoreApplication.translate("ControlPanel", u"Vertex Cover", None))
        self.v_cover_button.setText(QCoreApplication.translate("ControlPanel", u"Find Vertex Cover", None))
        self.v_cover_label.setText(QCoreApplication.translate("ControlPanel", u"	\u03b2(G)", None))
        self.complement_box.setTitle(QCoreApplication.translate("ControlPanel", u"Graph Complement", None))
        self.complement_button.setText(QCoreApplication.translate("ControlPanel", u"Show Complement", None))
        self.tabs.setTabText(self.tabs.indexOf(self.undirected_tab), QCoreApplication.translate("ControlPanel", u"Undirected Graph", None))
    # retranslateUi

