from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Tool(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        
    def setupUi(self, Tool):
        if not Tool.objectName():
            Tool.setObjectName(u"Tool")
        Tool.resize(197, 63)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Tool.sizePolicy().hasHeightForWidth())
        Tool.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Tool)
        self.gridLayout.setObjectName(u"gridLayout")
        self.done_button = QPushButton(Tool)
        self.done_button.setObjectName(u"done_button")

        self.gridLayout.addWidget(self.done_button, 0, 0, 1, 1, Qt.AlignLeft)

        self.revert_button = QPushButton(Tool)
        self.revert_button.setObjectName(u"revert_button")

        self.gridLayout.addWidget(self.revert_button, 0, 1, 1, 1, Qt.AlignLeft)


        self.retranslateUi(Tool)

        QMetaObject.connectSlotsByName(Tool)
    # setupUi

    def retranslateUi(self, Tool):
        Tool.setWindowTitle(QCoreApplication.translate("Tool", u"Frame", None))
        self.done_button.setText(QCoreApplication.translate("Tool", u"Done", None))
        self.revert_button.setText(QCoreApplication.translate("Tool", u"Revert", None))
    # retranslateUi

