# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowbTnwnZ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from workspace import Workspace
from info_panel import Ui_InfoPanel
from control_panel import Ui_ControlPanel


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, MainWindow: QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(756, 690)
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
        self.cp_scroll_area.setStyleSheet(u"QScrollArea {\n"
"	border: none;\n"
"}")
        self.cp_scroll_area.setWidgetResizable(True)
        self.cp_scroll_area_content = QWidget()
        self.cp_scroll_area_content.setObjectName(u"cp_scroll_area_content")
        self.cp_scroll_area_content.setGeometry(QRect(0, 0, 738, 69))
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
        self.frame_2 = Ui_ControlPanel(self.cp_scroll_area_content)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_9.addWidget(self.frame_2)

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
        self.ip_scroll_area_content.setGeometry(QRect(0, 0, 69, 556))
        self.ip_scroll_area_content.setMinimumSize(QSize(0, 547))
        self.ip_scroll_area_content.setMaximumSize(QSize(250, 16777215))
        self.ip_scroll_area_content.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.ip_scroll_area_content)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = Ui_InfoPanel(self.ip_scroll_area_content)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 547))
        self.frame.setMaximumSize(QSize(250, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.frame)

        self.ip_scroll_area.setWidget(self.ip_scroll_area_content)

        self.horizontalLayout.addWidget(self.ip_scroll_area)

        self.view = Workspace(self.h_layout_widget)
        self.view.setObjectName(u"view")
        self.view.setMaximumSize(QSize(999999, 999999))
        self.view.setAutoFillBackground(False)

        self.horizontalLayout.addWidget(self.view)


        self.verticalLayout.addWidget(self.h_layout_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 756, 21))
        self.menu_add = QMenu(self.menubar)
        self.menu_add.setObjectName(u"menu_add")
        self.menu_edit = QMenu(self.menubar)
        self.menu_edit.setObjectName(u"menu_edit")
        self.menu_delete = QMenu(self.menubar)
        self.menu_delete.setObjectName(u"menu_delete")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_add.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_delete.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menu_add.setTitle(QCoreApplication.translate("MainWindow", u"Add", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menu_delete.setTitle(QCoreApplication.translate("MainWindow", u"Delete", None))
    # retranslateUi

