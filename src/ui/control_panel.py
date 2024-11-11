
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
        ControlPanel.resize(1016, 168)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ControlPanel.sizePolicy().hasHeightForWidth())
        ControlPanel.setSizePolicy(sizePolicy)
        ControlPanel.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(ControlPanel)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget(ControlPanel)
        self.tabs.setObjectName(u"tabs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy1)
        self.tabs.setMaximumSize(QSize(600, 16777215))
        self.tabs.setStyleSheet(u"QFrame {\n"
"	border-radius: 5px\n"
"}")
        self.tabs.setTabsClosable(False)
        self.tabs.setMovable(True)
        self.tabs.setTabBarAutoHide(False)
        self.directed_tab = QWidget()
        self.directed_tab.setObjectName(u"directed_tab")
        self.horizontalLayout_8 = QHBoxLayout(self.directed_tab)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.d_algorithm_box = QGroupBox(self.directed_tab)
        self.d_algorithm_box.setObjectName(u"d_algorithm_box")
        self.d_algorithm_box.setMinimumSize(QSize(250, 0))
        self.d_algorithm_box.setMaximumSize(QSize(300, 16777215))
        self.d_algorithm_box.setStyleSheet(u"")
        self.d_algorithm_box.setFlat(False)
        self.d_algorithm_layout = QVBoxLayout(self.d_algorithm_box)
        self.d_algorithm_layout.setSpacing(12)
        self.d_algorithm_layout.setObjectName(u"d_algorithm_layout")
        self.horizontalWidget = QWidget(self.d_algorithm_box)
        self.horizontalWidget.setObjectName(u"horizontalWidget")
        self.horizontalLayout_10 = QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.dijkstra_radio = QRadioButton(self.horizontalWidget)
        self.dijkstra_radio.setObjectName(u"dijkstra_radio")

        self.horizontalLayout_10.addWidget(self.dijkstra_radio, 0, Qt.AlignHCenter)

        self.floyd_radio = QRadioButton(self.horizontalWidget)
        self.floyd_radio.setObjectName(u"floyd_radio")

        self.horizontalLayout_10.addWidget(self.floyd_radio, 0, Qt.AlignHCenter)


        self.d_algorithm_layout.addWidget(self.horizontalWidget, 0, Qt.AlignVCenter)

        self.run_algo_d_button = QPushButton(self.d_algorithm_box)
        self.run_algo_d_button.setObjectName(u"run_algo_d_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.run_algo_d_button.sizePolicy().hasHeightForWidth())
        self.run_algo_d_button.setSizePolicy(sizePolicy2)
        self.run_algo_d_button.setMinimumSize(QSize(100, 25))

        self.d_algorithm_layout.addWidget(self.run_algo_d_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_8.addWidget(self.d_algorithm_box)

        self.tabs.addTab(self.directed_tab, "")
        self.undirected_tab = QWidget()
        self.undirected_tab.setObjectName(u"undirected_tab")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.undirected_tab.sizePolicy().hasHeightForWidth())
        self.undirected_tab.setSizePolicy(sizePolicy3)
        self.horizontalLayout_3 = QHBoxLayout(self.undirected_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ud_algorithm_box = QGroupBox(self.undirected_tab)
        self.ud_algorithm_box.setObjectName(u"ud_algorithm_box")
        self.ud_algorithm_box.setMinimumSize(QSize(250, 0))
        self.ud_algorithm_box.setMaximumSize(QSize(300, 16777215))
        self.ud_algorithm_box.setFlat(False)
        self.verticalLayout_13 = QVBoxLayout(self.ud_algorithm_box)
        self.verticalLayout_13.setSpacing(12)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalWidget_2 = QWidget(self.ud_algorithm_box)
        self.horizontalWidget_2.setObjectName(u"horizontalWidget_2")
        self.horizontalLayout_12 = QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.prim_radio = QRadioButton(self.horizontalWidget_2)
        self.buttonGroup_2 = QButtonGroup(ControlPanel)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.prim_radio)
        self.prim_radio.setObjectName(u"prim_radio")
        self.prim_radio.setChecked(True)

        self.horizontalLayout_12.addWidget(self.prim_radio, 0, Qt.AlignHCenter)

        self.kruskal_radio = QRadioButton(self.horizontalWidget_2)
        self.buttonGroup_2.addButton(self.kruskal_radio)
        self.kruskal_radio.setObjectName(u"kruskal_radio")

        self.horizontalLayout_12.addWidget(self.kruskal_radio, 0, Qt.AlignHCenter)


        self.verticalLayout_13.addWidget(self.horizontalWidget_2, 0, Qt.AlignVCenter)

        self.run_algo_ud_button = QPushButton(self.ud_algorithm_box)
        self.run_algo_ud_button.setObjectName(u"run_algo_ud_button")
        sizePolicy2.setHeightForWidth(self.run_algo_ud_button.sizePolicy().hasHeightForWidth())
        self.run_algo_ud_button.setSizePolicy(sizePolicy2)
        self.run_algo_ud_button.setMinimumSize(QSize(100, 25))

        self.verticalLayout_13.addWidget(self.run_algo_ud_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_3.addWidget(self.ud_algorithm_box)

        self.complement_box = QGroupBox(self.undirected_tab)
        self.complement_box.setObjectName(u"complement_box")
        self.verticalLayout_2 = QVBoxLayout(self.complement_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.complement_button = QPushButton(self.complement_box)
        self.complement_button.setObjectName(u"complement_button")
        self.complement_button.setMinimumSize(QSize(110, 0))
        self.complement_button.setMaximumSize(QSize(200, 16777215))
        self.complement_button.setCheckable(True)
        self.complement_button.setChecked(False)

        self.verticalLayout_2.addWidget(self.complement_button, 0, Qt.AlignHCenter)


        self.horizontalLayout_3.addWidget(self.complement_box)

        self.tabs.addTab(self.undirected_tab, "")

        self.horizontalLayout.addWidget(self.tabs)

        self.line_4 = QFrame(ControlPanel)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.add_box = QGroupBox(ControlPanel)
        self.add_box.setObjectName(u"add_box")
        self.add_box.setMaximumSize(QSize(400, 16777215))
        self.add_box.setFlat(True)
        self.add_box.setCheckable(False)
        self.gridLayout_3 = QGridLayout(self.add_box)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.id_type_label = QLabel(self.add_box)
        self.id_type_label.setObjectName(u"id_type_label")

        self.gridLayout_3.addWidget(self.id_type_label, 1, 0, 1, 1, Qt.AlignRight)

        self.add_edge_button = QPushButton(self.add_box)
        self.add_edge_button.setObjectName(u"add_edge_button")
        self.add_edge_button.setMinimumSize(QSize(100, 30))
        self.add_edge_button.setMaximumSize(QSize(200, 16777215))
        self.add_edge_button.setCheckable(True)
        self.add_edge_button.setAutoDefault(False)
        self.add_edge_button.setFlat(False)

        self.gridLayout_3.addWidget(self.add_edge_button, 0, 1, 1, 1)

        self.id_type_combobox = QComboBox(self.add_box)
        self.id_type_combobox.addItem("")
        self.id_type_combobox.addItem("")
        self.id_type_combobox.setObjectName(u"id_type_combobox")
        self.id_type_combobox.setMinimumSize(QSize(80, 30))
        self.id_type_combobox.setAutoFillBackground(False)
        self.id_type_combobox.setFrame(True)

        self.gridLayout_3.addWidget(self.id_type_combobox, 1, 1, 1, 1)

        self.add_vertex_button = QPushButton(self.add_box)
        self.add_vertex_button.setObjectName(u"add_vertex_button")
        self.add_vertex_button.setMinimumSize(QSize(100, 30))
        self.add_vertex_button.setMaximumSize(QSize(200, 16777215))
        self.add_vertex_button.setCheckable(True)
        self.add_vertex_button.setAutoDefault(False)
        self.add_vertex_button.setFlat(False)

        self.gridLayout_3.addWidget(self.add_vertex_button, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.add_box)

        self.line_3 = QFrame(ControlPanel)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.edit_box = QGroupBox(ControlPanel)
        self.edit_box.setObjectName(u"edit_box")
        self.edit_box.setMaximumSize(QSize(200, 16777215))
        self.edit_box.setFlat(True)
        self.verticalLayout_11 = QVBoxLayout(self.edit_box)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.edit_weight_button = QPushButton(self.edit_box)
        self.edit_weight_button.setObjectName(u"edit_weight_button")
        self.edit_weight_button.setMinimumSize(QSize(80, 30))
        self.edit_weight_button.setCheckable(True)

        self.verticalLayout_11.addWidget(self.edit_weight_button, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.edit_box)

        self.line_5 = QFrame(ControlPanel)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.delete_box = QGroupBox(ControlPanel)
        self.delete_box.setObjectName(u"delete_box")
        self.delete_box.setMaximumSize(QSize(200, 16777215))
        self.delete_box.setFlat(True)
        self.verticalLayout_12 = QVBoxLayout(self.delete_box)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.delete_button = QPushButton(self.delete_box)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setMinimumSize(QSize(80, 30))
        self.delete_button.setCheckable(True)

        self.verticalLayout_12.addWidget(self.delete_button, 0, Qt.AlignHCenter)

        self.clear_button = QPushButton(self.delete_box)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setMinimumSize(QSize(80, 30))

        self.verticalLayout_12.addWidget(self.clear_button, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.delete_box)

        self.line_10 = QFrame(ControlPanel)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.VLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_10)

        self.simulate_box = QGroupBox(ControlPanel)
        self.simulate_box.setObjectName(u"simulate_box")
        self.verticalLayout_9 = QVBoxLayout(self.simulate_box)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.play_button = QPushButton(self.simulate_box)
        self.play_button.setObjectName(u"play_button")
        sizePolicy2.setHeightForWidth(self.play_button.sizePolicy().hasHeightForWidth())
        self.play_button.setSizePolicy(sizePolicy2)
        self.play_button.setMinimumSize(QSize(60, 30))
        self.play_button.setCheckable(True)

        self.verticalLayout_9.addWidget(self.play_button, 0, Qt.AlignHCenter)

        self.pause_button = QPushButton(self.simulate_box)
        self.pause_button.setObjectName(u"pause_button")
        sizePolicy2.setHeightForWidth(self.pause_button.sizePolicy().hasHeightForWidth())
        self.pause_button.setSizePolicy(sizePolicy2)
        self.pause_button.setMinimumSize(QSize(60, 30))
        self.pause_button.setCheckable(True)

        self.verticalLayout_9.addWidget(self.pause_button, 0, Qt.AlignHCenter)

        self.stop_button = QPushButton(self.simulate_box)
        self.stop_button.setObjectName(u"stop_button")
        sizePolicy2.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy2)
        self.stop_button.setMinimumSize(QSize(60, 30))

        self.verticalLayout_9.addWidget(self.stop_button, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.simulate_box)


        self.retranslateUi(ControlPanel)

        self.tabs.setCurrentIndex(1)
        self.add_vertex_button.setDefault(False)


        QMetaObject.connectSlotsByName(ControlPanel)
    # setupUi

    def retranslateUi(self, ControlPanel):
        ControlPanel.setWindowTitle(QCoreApplication.translate("ControlPanel", u"Frame", None))
        self.d_algorithm_box.setTitle(QCoreApplication.translate("ControlPanel", u"Algorithms", None))
        self.dijkstra_radio.setText(QCoreApplication.translate("ControlPanel", u"Dijkstra", None))
        self.floyd_radio.setText(QCoreApplication.translate("ControlPanel", u"Floyd Warshal", None))
        self.run_algo_d_button.setText(QCoreApplication.translate("ControlPanel", u"Run Algorithm", None))
        self.tabs.setTabText(self.tabs.indexOf(self.directed_tab), QCoreApplication.translate("ControlPanel", u"Directed Graph", None))
        self.ud_algorithm_box.setTitle(QCoreApplication.translate("ControlPanel", u"Algorithms", None))
        self.prim_radio.setText(QCoreApplication.translate("ControlPanel", u"Prim", None))
        self.kruskal_radio.setText(QCoreApplication.translate("ControlPanel", u"Kruskal", None))
        self.run_algo_ud_button.setText(QCoreApplication.translate("ControlPanel", u"Run Algorithm", None))
        self.complement_box.setTitle(QCoreApplication.translate("ControlPanel", u"Graph Complement", None))
        self.complement_button.setText(QCoreApplication.translate("ControlPanel", u"Show Complement", None))
        self.tabs.setTabText(self.tabs.indexOf(self.undirected_tab), QCoreApplication.translate("ControlPanel", u"Undirected Graph", None))
        self.add_box.setTitle(QCoreApplication.translate("ControlPanel", u"Add", None))
        self.id_type_label.setText(QCoreApplication.translate("ControlPanel", u"Vertex ID type:", None))
        self.add_edge_button.setText(QCoreApplication.translate("ControlPanel", u"Add Edge", None))
        self.id_type_combobox.setItemText(0, QCoreApplication.translate("ControlPanel", u"Integer", None))
        self.id_type_combobox.setItemText(1, QCoreApplication.translate("ControlPanel", u"Character", None))

#if QT_CONFIG(whatsthis)
        self.id_type_combobox.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.id_type_combobox.setPlaceholderText("")
        self.add_vertex_button.setText(QCoreApplication.translate("ControlPanel", u"Add Vertex", None))
        self.edit_box.setTitle(QCoreApplication.translate("ControlPanel", u"Edit", None))
        self.edit_weight_button.setText(QCoreApplication.translate("ControlPanel", u"Edit Weight", None))
        self.delete_box.setTitle(QCoreApplication.translate("ControlPanel", u"Delete", None))
        self.delete_button.setText(QCoreApplication.translate("ControlPanel", u"Delete one", None))
        self.clear_button.setText(QCoreApplication.translate("ControlPanel", u"Clear graph", None))
        self.simulate_box.setTitle(QCoreApplication.translate("ControlPanel", u"Simulate", None))
        self.play_button.setText(QCoreApplication.translate("ControlPanel", u"Play", None))
        self.pause_button.setText(QCoreApplication.translate("ControlPanel", u"Pause", None))
        self.stop_button.setText(QCoreApplication.translate("ControlPanel", u"Stop", None))
    # retranslateUi

