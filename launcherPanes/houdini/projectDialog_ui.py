# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'projectDialog.ui'
#
# Created: Tue Sep 19 21:42:28 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_projectSelectionDialog(object):
    def setupUi(self, projectSelectionDialog):
        projectSelectionDialog.setObjectName("projectSelectionDialog")
        projectSelectionDialog.resize(669, 463)
        projectSelectionDialog.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(projectSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainlLayout = QtGui.QHBoxLayout()
        self.mainlLayout.setObjectName("mainlLayout")
        self.recentProjectsListView = QtGui.QListView(projectSelectionDialog)
        self.recentProjectsListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.recentProjectsListView.setAlternatingRowColors(True)
        self.recentProjectsListView.setObjectName("recentProjectsListView")
        self.mainlLayout.addWidget(self.recentProjectsListView)
        self.fileTreeView = QtGui.QTreeView(projectSelectionDialog)
        self.fileTreeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.fileTreeView.setObjectName("fileTreeView")
        self.mainlLayout.addWidget(self.fileTreeView)
        self.mainlLayout.setStretch(0, 1)
        self.mainlLayout.setStretch(1, 4)
        self.verticalLayout.addLayout(self.mainlLayout)

        self.retranslateUi(projectSelectionDialog)
        QtCore.QMetaObject.connectSlotsByName(projectSelectionDialog)

    def retranslateUi(self, projectSelectionDialog):
        projectSelectionDialog.setWindowTitle(QtGui.QApplication.translate("projectSelectionDialog", "Project Selector", None, QtGui.QApplication.UnicodeUTF8))

