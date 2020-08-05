# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'houdini.ui',
# licensing of 'houdini.ui' applies.
#
# Created: Fri May 22 00:00:04 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_houdiniMenu(object):
    def setupUi(self, houdiniMenu):
        houdiniMenu.setObjectName("houdiniMenu")
        houdiniMenu.resize(715, 679)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(houdiniMenu.sizePolicy().hasHeightForWidth())
        houdiniMenu.setSizePolicy(sizePolicy)
        houdiniMenu.setMinimumSize(QtCore.QSize(100, 100))
        houdiniMenu.setBaseSize(QtCore.QSize(1024, 1024))
        self.verticalLayout = QtWidgets.QVBoxLayout(houdiniMenu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.paneVersionLabel = QtWidgets.QLabel(houdiniMenu)
        self.paneVersionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.paneVersionLabel.setObjectName("paneVersionLabel")
        self.gridLayout.addWidget(self.paneVersionLabel, 1, 2, 1, 1)
        self.paneLogo = QtWidgets.QLabel(houdiniMenu)
        self.paneLogo.setMinimumSize(QtCore.QSize(128, 128))
        self.paneLogo.setMaximumSize(QtCore.QSize(128, 128))
        self.paneLogo.setText("")
        self.paneLogo.setPixmap(QtGui.QPixmap(":/icons/houdini/houlogo.png"))
        self.paneLogo.setScaledContents(True)
        self.paneLogo.setObjectName("paneLogo")
        self.gridLayout.addWidget(self.paneLogo, 0, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.houVersionComboBox = QtWidgets.QComboBox(houdiniMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.houVersionComboBox.sizePolicy().hasHeightForWidth())
        self.houVersionComboBox.setSizePolicy(sizePolicy)
        self.houVersionComboBox.setMinimumSize(QtCore.QSize(128, 0))
        self.houVersionComboBox.setObjectName("houVersionComboBox")
        self.horizontalLayout_2.addWidget(self.houVersionComboBox)
        self.binNameComboBox = QtWidgets.QComboBox(houdiniMenu)
        self.binNameComboBox.setEditable(True)
        self.binNameComboBox.setObjectName("binNameComboBox")
        self.binNameComboBox.addItem("")
        self.binNameComboBox.addItem("")
        self.binNameComboBox.addItem("")
        self.binNameComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.binNameComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 1, 1, 1)
        self.houVersionLabel = QtWidgets.QLabel(houdiniMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.houVersionLabel.sizePolicy().hasHeightForWidth())
        self.houVersionLabel.setSizePolicy(sizePolicy)
        self.houVersionLabel.setObjectName("houVersionLabel")
        self.gridLayout.addWidget(self.houVersionLabel, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(houdiniMenu)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.configComboBox = QtWidgets.QComboBox(houdiniMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configComboBox.sizePolicy().hasHeightForWidth())
        self.configComboBox.setSizePolicy(sizePolicy)
        self.configComboBox.setObjectName("configComboBox")
        self.horizontalLayout_3.addWidget(self.configComboBox)
        self.newConfigPushButton = QtWidgets.QPushButton(houdiniMenu)
        self.newConfigPushButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.newConfigPushButton.setStyleSheet("QPushButton#newConfigPushButton{\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}")
        self.newConfigPushButton.setObjectName("newConfigPushButton")
        self.horizontalLayout_3.addWidget(self.newConfigPushButton)
        self.renameConfigPushButton = QtWidgets.QPushButton(houdiniMenu)
        self.renameConfigPushButton.setMaximumSize(QtCore.QSize(48, 16777215))
        self.renameConfigPushButton.setStyleSheet("QPushButton#renameConfigPushButton{\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}")
        self.renameConfigPushButton.setObjectName("renameConfigPushButton")
        self.horizontalLayout_3.addWidget(self.renameConfigPushButton)
        self.delConfigPushButton = QtWidgets.QPushButton(houdiniMenu)
        self.delConfigPushButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.delConfigPushButton.setStyleSheet("QPushButton#delConfigPushButton{\n"
"    padding-right: 5px;\n"
"    padding-left: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"}")
        self.delConfigPushButton.setObjectName("delConfigPushButton")
        self.horizontalLayout_3.addWidget(self.delConfigPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(4, 1)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.sceneFilesTreeView = QtWidgets.QTreeView(houdiniMenu)
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
        self.gridLayout.addWidget(self.sceneFilesTreeView, 6, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectPathLine = QtWidgets.QLineEdit(houdiniMenu)
        self.projectPathLine.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.projectPathLine.setFrame(True)
        self.projectPathLine.setObjectName("projectPathLine")
        self.horizontalLayout.addWidget(self.projectPathLine)
        self.projectPathPushButton = QtWidgets.QPushButton(houdiniMenu)
        self.projectPathPushButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.projectPathPushButton.setObjectName("projectPathPushButton")
        self.horizontalLayout.addWidget(self.projectPathPushButton)
        self.saveProjectPushButton = QtWidgets.QPushButton(houdiniMenu)
        self.saveProjectPushButton.setObjectName("saveProjectPushButton")
        self.horizontalLayout.addWidget(self.saveProjectPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.configLabel = QtWidgets.QLabel(houdiniMenu)
        self.configLabel.setObjectName("configLabel")
        self.gridLayout.addWidget(self.configLabel, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.launchPushButton = QtWidgets.QPushButton(houdiniMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launchPushButton.sizePolicy().hasHeightForWidth())
        self.launchPushButton.setSizePolicy(sizePolicy)
        self.launchPushButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.launchPushButton.setObjectName("launchPushButton")
        self.horizontalLayout_5.addWidget(self.launchPushButton)
        self.launchOptionsPushButton = QtWidgets.QPushButton(houdiniMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launchOptionsPushButton.sizePolicy().hasHeightForWidth())
        self.launchOptionsPushButton.setSizePolicy(sizePolicy)
        self.launchOptionsPushButton.setMaximumSize(QtCore.QSize(16, 16777215))
        self.launchOptionsPushButton.setText("v")
        self.launchOptionsPushButton.setObjectName("launchOptionsPushButton")
        self.horizontalLayout_5.addWidget(self.launchOptionsPushButton)
        self.horizontalLayout_5.setStretch(0, 1)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 1, 1, 1)
        self.commandLineArgsLineEdit = QtWidgets.QLineEdit(houdiniMenu)
        self.commandLineArgsLineEdit.setStyleSheet("QLineEdit\n"
"{\n"
"    background: rgba(0,0,0,64)\n"
"}")
        self.commandLineArgsLineEdit.setObjectName("commandLineArgsLineEdit")
        self.gridLayout.addWidget(self.commandLineArgsLineEdit, 4, 1, 1, 1)
        self.commandLineLabel = QtWidgets.QLabel(houdiniMenu)
        self.commandLineLabel.setObjectName("commandLineLabel")
        self.gridLayout.addWidget(self.commandLineLabel, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.label_2 = QtWidgets.QLabel(houdiniMenu)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.envTableView = QtWidgets.QTableView(houdiniMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.envTableView.sizePolicy().hasHeightForWidth())
        self.envTableView.setSizePolicy(sizePolicy)
        self.envTableView.setAlternatingRowColors(True)
        self.envTableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.envTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
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
        houdiniMenu.setWindowTitle(QtWidgets.QApplication.translate("houdiniMenu", "Form", None, -1))
        self.paneVersionLabel.setText(QtWidgets.QApplication.translate("houdiniMenu", "v 0.1", None, -1))
        self.binNameComboBox.setItemText(0, QtWidgets.QApplication.translate("houdiniMenu", "hmaster", None, -1))
        self.binNameComboBox.setItemText(1, QtWidgets.QApplication.translate("houdiniMenu", "houdinifx", None, -1))
        self.binNameComboBox.setItemText(2, QtWidgets.QApplication.translate("houdiniMenu", "houdini", None, -1))
        self.binNameComboBox.setItemText(3, QtWidgets.QApplication.translate("houdiniMenu", "houdinicore", None, -1))
        self.houVersionLabel.setText(QtWidgets.QApplication.translate("houdiniMenu", "Houdini Version:  ", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("houdiniMenu", "Proect Location:   ", None, -1))
        self.newConfigPushButton.setText(QtWidgets.QApplication.translate("houdiniMenu", "new", None, -1))
        self.renameConfigPushButton.setText(QtWidgets.QApplication.translate("houdiniMenu", "rename", None, -1))
        self.delConfigPushButton.setText(QtWidgets.QApplication.translate("houdiniMenu", "del", None, -1))
        self.projectPathPushButton.setText(QtWidgets.QApplication.translate("houdiniMenu", "...", None, -1))
        self.saveProjectPushButton.setText(QtWidgets.QApplication.translate("houdiniMenu", "save", None, -1))
        self.configLabel.setText(QtWidgets.QApplication.translate("houdiniMenu", "Configuration  :", None, -1))
        self.launchPushButton.setText(QtWidgets.QApplication.translate("houdiniMenu", "Launch!", None, -1))
        self.commandLineLabel.setText(QtWidgets.QApplication.translate("houdiniMenu", "Arguments:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("houdiniMenu", "environment variables", None, -1))
