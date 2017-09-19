from PySide.QtCore import *
from PySide.QtGui import *

import launcherPanes

from mainwindow_ui	import Ui_MainWindow

import launcherPanes

class LauncherWindow(QMainWindow):
	def __init__(self,parent=None):
		super(LauncherWindow,self).__init__(parent)

		self.__setupUI()
		self.setWindowTitle("launcher")

		for paneclass in launcherPanes.pluginClassList:
			pane=paneclass(self)
			paneName,paneIcon = pane.paneHeader()
			newheader=QRadioButton(self)
			newheader.setText(paneName)
			newheader.setIcon(QIcon(paneIcon))
			newheader.setIconSize(QSize(32,32))
			newheader.toggled.connect(pane.setActive)
			self.ui.buttonsLayout.addWidget(newheader)
			self.ui.horizontalLayout.addWidget(pane)
			pane.hide()
			if (self.ui.buttonsLayout.count() == 1): newheader.setChecked(True)

	def __setupUI(self):
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		self.setStyleSheet('')