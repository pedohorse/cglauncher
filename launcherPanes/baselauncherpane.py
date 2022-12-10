# from PySide2.QtCore import *
# from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget


class BaseLauncherPane(QWidget):
	def __init__(self, parent=None):
		super(BaseLauncherPane, self).__init__(parent)

	def pane_header(self):
		"""
		information on the header for sider bar
		:return: ('text','icon location in resource file ')
		"""
		raise NotImplementedError("abstract method")

	def setActive(self, active):
		if active:
			self.show()
		else:
			self.hide()
