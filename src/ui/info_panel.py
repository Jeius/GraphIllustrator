from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_InfoPanel(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, InfoPanel):
        if not InfoPanel.objectName():
            InfoPanel.setObjectName(u"InfoPanel")
        InfoPanel.resize(250, 729)
        InfoPanel.setMaximumSize(QSize(250, 16777215))
        self.gridLayout = QGridLayout(InfoPanel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.size_order_layout = QHBoxLayout()
        self.size_order_layout.setSpacing(5)
        self.size_order_layout.setObjectName(u"size_order_layout")
        self.size_label = QLabel(InfoPanel)
        self.size_label.setObjectName(u"size_label")

        self.size_order_layout.addWidget(self.size_label, 0, Qt.AlignRight)

        self.order_box = QLineEdit(InfoPanel)
        self.order_box.setObjectName(u"order_box")
        self.order_box.setMinimumSize(QSize(0, 32))
        self.order_box.setMaximumSize(QSize(100, 16777215))
        self.order_box.setReadOnly(True)

        self.size_order_layout.addWidget(self.order_box, 0, Qt.AlignLeft)

        self.h_spacer = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.size_order_layout.addItem(self.h_spacer)

        self.order_label = QLabel(InfoPanel)
        self.order_label.setObjectName(u"order_label")

        self.size_order_layout.addWidget(self.order_label)

        self.size_box = QLineEdit(InfoPanel)
        self.size_box.setObjectName(u"size_box")
        self.size_box.setMinimumSize(QSize(0, 32))
        self.size_box.setMaximumSize(QSize(100, 16777215))
        self.size_box.setReadOnly(True)

        self.size_order_layout.addWidget(self.size_box, 0, Qt.AlignRight)


        self.gridLayout.addLayout(self.size_order_layout, 0, 0, 1, 1)

        self.sets_grid = QWidget(InfoPanel)
        self.sets_grid.setObjectName(u"sets_grid")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sets_grid.sizePolicy().hasHeightForWidth())
        self.sets_grid.setSizePolicy(sizePolicy)
        self.sets_grid.setMaximumSize(QSize(16777215, 120))
        self.gridLayout_3 = QGridLayout(self.sets_grid)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.vertex_set_label = QLabel(self.sets_grid)
        self.vertex_set_label.setObjectName(u"vertex_set_label")

        self.gridLayout_3.addWidget(self.vertex_set_label, 7, 0, 1, 1)

        self.vertex_set_box = QLineEdit(self.sets_grid)
        self.vertex_set_box.setObjectName(u"vertex_set_box")
        self.vertex_set_box.setMinimumSize(QSize(0, 32))
        self.vertex_set_box.setReadOnly(True)

        self.gridLayout_3.addWidget(self.vertex_set_box, 7, 1, 1, 1)

        self.edge_set_box = QLineEdit(self.sets_grid)
        self.edge_set_box.setObjectName(u"edge_set_box")
        self.edge_set_box.setMinimumSize(QSize(0, 32))
        self.edge_set_box.setReadOnly(True)

        self.gridLayout_3.addWidget(self.edge_set_box, 8, 1, 1, 1)

        self.edge_set_label = QLabel(self.sets_grid)
        self.edge_set_label.setObjectName(u"edge_set_label")

        self.gridLayout_3.addWidget(self.edge_set_label, 8, 0, 1, 1)


        self.gridLayout.addWidget(self.sets_grid, 1, 0, 1, 1)

        self.line_2 = QFrame(InfoPanel)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)

        self.adj_matrix_widget = QWidget(InfoPanel)
        self.adj_matrix_widget.setObjectName(u"adj_matrix_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.adj_matrix_widget.sizePolicy().hasHeightForWidth())
        self.adj_matrix_widget.setSizePolicy(sizePolicy1)
        self.verticalLayout_7 = QVBoxLayout(self.adj_matrix_widget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 6)
        self.adj_matrix_label = QLabel(self.adj_matrix_widget)
        self.adj_matrix_label.setObjectName(u"adj_matrix_label")

        self.verticalLayout_7.addWidget(self.adj_matrix_label)

        self.adj_matrix_box = QPlainTextEdit(self.adj_matrix_widget)
        self.adj_matrix_box.setObjectName(u"adj_matrix_box")
        self.adj_matrix_box.setMinimumSize(QSize(0, 180))
        self.adj_matrix_box.setReadOnly(True)

        self.verticalLayout_7.addWidget(self.adj_matrix_box)


        self.gridLayout.addWidget(self.adj_matrix_widget, 3, 0, 1, 1)

        self.line_3 = QFrame(InfoPanel)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 4, 0, 1, 1)

        self.path_table_widget = QWidget(InfoPanel)
        self.path_table_widget.setObjectName(u"path_table_widget")
        self.verticalLayout_8 = QVBoxLayout(self.path_table_widget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.path_table_label = QLabel(self.path_table_widget)
        self.path_table_label.setObjectName(u"path_table_label")

        self.verticalLayout_8.addWidget(self.path_table_label)

        self.path_table = QTableView(self.path_table_widget)
        self.path_table.setObjectName(u"path_table")
        self.path_table.setMinimumSize(QSize(0, 220))

        self.verticalLayout_8.addWidget(self.path_table)


        self.gridLayout.addWidget(self.path_table_widget, 5, 0, 1, 1)


        self.retranslateUi(InfoPanel)

        QMetaObject.connectSlotsByName(InfoPanel)
    # setupUi

    def retranslateUi(self, InfoPanel):
        InfoPanel.setWindowTitle(QCoreApplication.translate("InfoPanel", u"Frame", None))
        self.size_label.setText(QCoreApplication.translate("InfoPanel", u"Size", None))
        self.order_label.setText(QCoreApplication.translate("InfoPanel", u"Order", None))
        self.vertex_set_label.setText(QCoreApplication.translate("InfoPanel", u"Vertex Set", None))
        self.edge_set_label.setText(QCoreApplication.translate("InfoPanel", u"Edge Set", None))
        self.adj_matrix_label.setText(QCoreApplication.translate("InfoPanel", u"Adjacency Matrix", None))
        self.path_table_label.setText(QCoreApplication.translate("InfoPanel", u"Path Table", None))
    # retranslateUi

