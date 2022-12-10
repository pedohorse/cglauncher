# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'projectDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_projectSelectionDialog(object):
    def setupUi(self, projectSelectionDialog):
        if not projectSelectionDialog.objectName():
            projectSelectionDialog.setObjectName(u"projectSelectionDialog")
        projectSelectionDialog.resize(669, 463)
        projectSelectionDialog.setModal(False)
        self.verticalLayout = QVBoxLayout(projectSelectionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainlLayout = QHBoxLayout()
        self.mainlLayout.setObjectName(u"mainlLayout")
        self.recentProjectsListView = QListView(projectSelectionDialog)
        self.recentProjectsListView.setObjectName(u"recentProjectsListView")
        self.recentProjectsListView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.recentProjectsListView.setAlternatingRowColors(True)

        self.mainlLayout.addWidget(self.recentProjectsListView)

        self.fileTreeView = QTreeView(projectSelectionDialog)
        self.fileTreeView.setObjectName(u"fileTreeView")
        self.fileTreeView.setContextMenuPolicy(Qt.CustomContextMenu)

        self.mainlLayout.addWidget(self.fileTreeView)

        self.mainlLayout.setStretch(0, 1)
        self.mainlLayout.setStretch(1, 4)

        self.verticalLayout.addLayout(self.mainlLayout)


        self.retranslateUi(projectSelectionDialog)

        QMetaObject.connectSlotsByName(projectSelectionDialog)
    # setupUi

    def retranslateUi(self, projectSelectionDialog):
        projectSelectionDialog.setWindowTitle(QCoreApplication.translate("projectSelectionDialog", u"Project Selector", None))
    # retranslateUi

