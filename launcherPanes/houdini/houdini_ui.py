# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'houdini.ui'
#
# Created: Sat Nov 25 14:50:29 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_houdiniMenu(object):
    def setupUi(self, houdiniMenu):
        houdiniMenu.setObjectName("houdiniMenu")
        houdiniMenu.resize(715, 679)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(houdiniMenu.sizePolicy().hasHeightForWidth())
        houdiniMenu.setSizePolicy(sizePolicy)
        houdiniMenu.setMinimumSize(QtCore.QSize(100, 100))
        houdiniMenu.setBaseSize(QtCore.QSize(1024, 1024))
        self.verticalLayout = QtGui.QVBoxLayout(houdiniMenu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.sceneFilesTreeView = QtGui.QTreeView(houdiniMenu)
        self.sceneFilesTreeView.setStyleSheet("QTreeView{\n"
"    background-color: rgba(0,0,0,0)\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"            stop: 0.0 rgba(58, 58, 58, 128), \n"
"            stop: 1.0 rgba(38, 38, 38, 128) );\n"
"}\n"
"\n"
"QHeaderView\n"
"{\n"
"    background: rgba(0,0,0,0)\n"
"}")
        self.sceneFilesTreeView.setLineWidth(1)
        self.sceneFilesTreeView.setSortingEnabled(True)
        self.sceneFilesTreeView.setObjectName("sceneFilesTreeView")
        self.gridLayout.addWidget(self.sceneFilesTreeView, 5, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectPathLine = QtGui.QLineEdit(houdiniMenu)
        self.projectPathLine.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.projectPathLine.setFrame(True)
        self.projectPathLine.setObjectName("projectPathLine")
        self.horizontalLayout.addWidget(self.projectPathLine)
        self.projectPathPushButton = QtGui.QPushButton(houdiniMenu)
        self.projectPathPushButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.projectPathPushButton.setObjectName("projectPathPushButton")
        self.horizontalLayout.addWidget(self.projectPathPushButton)
        self.saveProjectPushButton = QtGui.QPushButton(houdiniMenu)
        self.saveProjectPushButton.setObjectName("saveProjectPushButton")
        self.horizontalLayout.addWidget(self.saveProjectPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.paneVersionLabel = QtGui.QLabel(houdiniMenu)
        self.paneVersionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.paneVersionLabel.setObjectName("paneVersionLabel")
        self.gridLayout.addWidget(self.paneVersionLabel, 1, 2, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.houVersionComboBox = QtGui.QComboBox(houdiniMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.houVersionComboBox.sizePolicy().hasHeightForWidth())
        self.houVersionComboBox.setSizePolicy(sizePolicy)
        self.houVersionComboBox.setMinimumSize(QtCore.QSize(128, 0))
        self.houVersionComboBox.setObjectName("houVersionComboBox")
        self.horizontalLayout_2.addWidget(self.houVersionComboBox)
        self.binNameComboBox = QtGui.QComboBox(houdiniMenu)
        self.binNameComboBox.setEditable(True)
        self.binNameComboBox.setObjectName("binNameComboBox")
        self.binNameComboBox.addItem("")
        self.binNameComboBox.addItem("")
        self.binNameComboBox.addItem("")
        self.binNameComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.binNameComboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)
        self.paneLogo = QtGui.QLabel(houdiniMenu)
        self.paneLogo.setMinimumSize(QtCore.QSize(128, 128))
        self.paneLogo.setMaximumSize(QtCore.QSize(128, 128))
        self.paneLogo.setText("")
        self.paneLogo.setPixmap(QtGui.QPixmap(":/icons/houdini/houlogo.png"))
        self.paneLogo.setScaledContents(True)
        self.paneLogo.setObjectName("paneLogo")
        self.gridLayout.addWidget(self.paneLogo, 0, 2, 1, 1)
        self.launchPushButton = QtGui.QPushButton(houdiniMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launchPushButton.sizePolicy().hasHeightForWidth())
        self.launchPushButton.setSizePolicy(sizePolicy)
        self.launchPushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.launchPushButton.setObjectName("launchPushButton")
        self.gridLayout.addWidget(self.launchPushButton, 0, 1, 1, 1)
        self.label = QtGui.QLabel(houdiniMenu)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.houVersionLabel = QtGui.QLabel(houdiniMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.houVersionLabel.sizePolicy().hasHeightForWidth())
        self.houVersionLabel.setSizePolicy(sizePolicy)
        self.houVersionLabel.setObjectName("houVersionLabel")
        self.gridLayout.addWidget(self.houVersionLabel, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.configComboBox = QtGui.QComboBox(houdiniMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configComboBox.sizePolicy().hasHeightForWidth())
        self.configComboBox.setSizePolicy(sizePolicy)
        self.configComboBox.setObjectName("configComboBox")
        self.horizontalLayout_3.addWidget(self.configComboBox)
        self.newConfigPushButton = QtGui.QPushButton(houdiniMenu)
        self.newConfigPushButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.newConfigPushButton.setStyleSheet("QPushButton#newConfigPushButton{\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}")
        self.newConfigPushButton.setObjectName("newConfigPushButton")
        self.horizontalLayout_3.addWidget(self.newConfigPushButton)
        self.renameConfigPushButton = QtGui.QPushButton(houdiniMenu)
        self.renameConfigPushButton.setMaximumSize(QtCore.QSize(48, 16777215))
        self.renameConfigPushButton.setStyleSheet("QPushButton#renameConfigPushButton{\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}")
        self.renameConfigPushButton.setObjectName("renameConfigPushButton")
        self.horizontalLayout_3.addWidget(self.renameConfigPushButton)
        self.delConfigPushButton = QtGui.QPushButton(houdiniMenu)
        self.delConfigPushButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.delConfigPushButton.setStyleSheet("QPushButton#delConfigPushButton{\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}")
        self.delConfigPushButton.setObjectName("delConfigPushButton")
        self.horizontalLayout_3.addWidget(self.delConfigPushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(4, 1)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.configLabel = QtGui.QLabel(houdiniMenu)
        self.configLabel.setObjectName("configLabel")
        self.gridLayout.addWidget(self.configLabel, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.label_2 = QtGui.QLabel(houdiniMenu)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.envTableView = QtGui.QTableView(houdiniMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.envTableView.sizePolicy().hasHeightForWidth())
        self.envTableView.setSizePolicy(sizePolicy)
        self.envTableView.setAlternatingRowColors(True)
        self.envTableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.envTableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.envTableView.setCornerButtonEnabled(False)
        self.envTableView.setObjectName("envTableView")
        self.envTableView.horizontalHeader().setVisible(True)
        self.envTableView.horizontalHeader().setStretchLastSection(True)
        self.envTableView.verticalHeader().setVisible(True)
        self.envTableView.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.envTableView)

        self.retranslateUi(houdiniMenu)
        QtCore.QMetaObject.connectSlotsByName(houdiniMenu)

    def retranslateUi(self, houdiniMenu):
        houdiniMenu.setWindowTitle(QtGui.QApplication.translate("houdiniMenu", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.projectPathPushButton.setText(QtGui.QApplication.translate("houdiniMenu", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveProjectPushButton.setText(QtGui.QApplication.translate("houdiniMenu", "save", None, QtGui.QApplication.UnicodeUTF8))
        self.paneVersionLabel.setText(QtGui.QApplication.translate("houdiniMenu", "v 0.1", None, QtGui.QApplication.UnicodeUTF8))
        self.binNameComboBox.setItemText(0, QtGui.QApplication.translate("houdiniMenu", "hmaster", None, QtGui.QApplication.UnicodeUTF8))
        self.binNameComboBox.setItemText(1, QtGui.QApplication.translate("houdiniMenu", "houdinifx", None, QtGui.QApplication.UnicodeUTF8))
        self.binNameComboBox.setItemText(2, QtGui.QApplication.translate("houdiniMenu", "houdini", None, QtGui.QApplication.UnicodeUTF8))
        self.binNameComboBox.setItemText(3, QtGui.QApplication.translate("houdiniMenu", "houdinicore", None, QtGui.QApplication.UnicodeUTF8))
        self.launchPushButton.setText(QtGui.QApplication.translate("houdiniMenu", "Launch!", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("houdiniMenu", "Proect Location:   ", None, QtGui.QApplication.UnicodeUTF8))
        self.houVersionLabel.setText(QtGui.QApplication.translate("houdiniMenu", "Houdini Version:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.newConfigPushButton.setText(QtGui.QApplication.translate("houdiniMenu", "new", None, QtGui.QApplication.UnicodeUTF8))
        self.renameConfigPushButton.setText(QtGui.QApplication.translate("houdiniMenu", "rename", None, QtGui.QApplication.UnicodeUTF8))
        self.delConfigPushButton.setText(QtGui.QApplication.translate("houdiniMenu", "del", None, QtGui.QApplication.UnicodeUTF8))
        self.configLabel.setText(QtGui.QApplication.translate("houdiniMenu", "Configuration  :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("houdiniMenu", "environment variables", None, QtGui.QApplication.UnicodeUTF8))

import houdini_rc
import houdini_rc
