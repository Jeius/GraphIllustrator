from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .workspace import Workspace
from .info_panel import Ui_InfoPanel
from .control_panel import Ui_ControlPanel


class Ui_MainWindow():
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(631, 690)
        MainWindow.setMinimumSize(QSize(0, 50))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cp_scroll_area = QScrollArea(self.centralwidget)
        self.cp_scroll_area.setObjectName(u"cp_scroll_area")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cp_scroll_area.sizePolicy().hasHeightForWidth())
        self.cp_scroll_area.setSizePolicy(sizePolicy)
        self.cp_scroll_area.setMaximumSize(QSize(99999, 99999))
        self.cp_scroll_area.setWidgetResizable(True)
        self.cp_scroll_area_content = QWidget()
        self.cp_scroll_area_content.setObjectName(u"cp_scroll_area_content")
        self.cp_scroll_area_content.setGeometry(QRect(0, 0, 613, 69))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cp_scroll_area_content.sizePolicy().hasHeightForWidth())
        self.cp_scroll_area_content.setSizePolicy(sizePolicy1)
        self.cp_scroll_area_content.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_9 = QHBoxLayout(self.cp_scroll_area_content)
        self.horizontalLayout_9.setSpacing(12)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.control_panel = Ui_ControlPanel(self.cp_scroll_area_content)
        self.control_panel.setObjectName(u"frame_2")
        self.control_panel.setFrameShape(QFrame.StyledPanel)
        self.control_panel.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_9.addWidget(self.control_panel)

        self.cp_scroll_area.setWidget(self.cp_scroll_area_content)

        self.verticalLayout.addWidget(self.cp_scroll_area)

        self.h_layout_widget = QWidget(self.centralwidget)
        self.h_layout_widget.setObjectName(u"h_layout_widget")
        self.horizontalLayout = QHBoxLayout(self.h_layout_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.ip_scroll_area = QScrollArea(self.h_layout_widget)
        self.ip_scroll_area.setObjectName(u"ip_scroll_area")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ip_scroll_area.sizePolicy().hasHeightForWidth())
        self.ip_scroll_area.setSizePolicy(sizePolicy2)
        self.ip_scroll_area.setMaximumSize(QSize(16777215, 16777215))
        self.ip_scroll_area.setStyleSheet(u"QScrollArea {\n"
"    border: none; /* Removes any border from the scroll area */\n"
"}\n"
"\n"
"")
        self.ip_scroll_area.setWidgetResizable(True)
        self.ip_scroll_area_content = QWidget()
        self.ip_scroll_area_content.setObjectName(u"ip_scroll_area_content")
        self.ip_scroll_area_content.setGeometry(QRect(0, 0, 69, 577))
        self.ip_scroll_area_content.setMinimumSize(QSize(0, 547))
        self.ip_scroll_area_content.setMaximumSize(QSize(250, 16777215))
        self.ip_scroll_area_content.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.ip_scroll_area_content)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.info_panel = Ui_InfoPanel(self.ip_scroll_area_content)
        self.info_panel.setObjectName(u"frame")
        self.info_panel.setMinimumSize(QSize(0, 547))
        self.info_panel.setMaximumSize(QSize(250, 16777215))
        self.info_panel.setFrameShape(QFrame.StyledPanel)
        self.info_panel.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.info_panel, 0, 0, 1, 1)

        self.ip_scroll_area.setWidget(self.ip_scroll_area_content)

        self.horizontalLayout.addWidget(self.ip_scroll_area)

        self.view = Workspace(self.h_layout_widget)
        self.view.setObjectName(u"view")
        self.view.setMaximumSize(QSize(999999, 999999))
        self.view.setAutoFillBackground(False)

        self.horizontalLayout.addWidget(self.view)


        self.verticalLayout.addWidget(self.h_layout_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Graph Illustrator - Julius Pahama", None))
    # retranslateUi

