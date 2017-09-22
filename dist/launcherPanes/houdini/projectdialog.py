import os

from PySide.QtCore import *
from PySide.QtGui import *

import projectDialog_ui

import json

from pprint import pprint


class ProjectListModel(QAbstractListModel):
	def __init__(self,parent):
		super(ProjectListModel,self).__init__(parent)
		self.__settingsfile = os.path.join(QDesktopServices.storageLocation(QDesktopServices.DataLocation), r'projectList')
		self.__data=[]
		try:
			with open(self.__settingsfile,"r") as f:
				self.__data=json.load(f)
		except:
			pass


	def addToList(self,projData):
		lastid=len(self.__data)
		if(len(projData)<2):raise RuntimeError("improper projData")
		self.beginInsertRows(QModelIndex(),lastid,lastid)
		try:#TODO: better keep all checks before try or we can end up endInsertRows with no actual rows added
			self.__data.append([projData[0],projData[1]])
		finally:
			self.endInsertRows()

			with open(self.__settingsfile,'w') as f:
				json.dump(self.__data,f)


	def removeRows(self,row,count,parent=None):
		if(parent is None):parent=QModelIndex()
		if(row>=len(self.__data)):return False
		if(row+count>len(self.__data)):count=len(self.__data)-row

		self.beginRemoveRows(parent,row,row+count-1)
		self.__data=self.__data[:row]+self.__data[row+count:]
		self.endRemoveRows()
		return True


####QAbstractListModel Overrides
	def data(self,index,role=Qt.DisplayRole):
		if(role==Qt.DisplayRole):
			return self.__data[index.row()][0]
		elif(role==Qt.UserRole):
			return self.__data[index.row()][1]
		return None

	def rowCount(self,index):
		return len(self.__data)



class ProjectDialog(QDialog):
	def __init__(self,parent=None):
		super(ProjectDialog,self).__init__(parent)

		self.__lastPath=''

		self.ui=projectDialog_ui.Ui_projectSelectionDialog()
		self.ui.setupUi(self)
		self.setWindowFlags(Qt.Popup)

		self.__fileModel=QFileSystemModel(self)
		self.__fileModel.setRootPath(QDir.currentPath())
		self.__fileModel.setFilter(QDir.AllDirs|QDir.NoDotAndDotDot)
		self.ui.fileTreeView.setModel(self.__fileModel)

		self.ui.fileTreeView.setColumnHidden(1, True)
		self.ui.fileTreeView.setColumnHidden(2, True)
		self.ui.fileTreeView.setColumnWidth(0, 400)

		#
		self.__recentProjectsModel=ProjectListModel(self)
		self.ui.recentProjectsListView.setModel(self.__recentProjectsModel)

		# signals
		self.ui.fileTreeView.customContextMenuRequested.connect(self.folderRightClicked)
		self.ui.recentProjectsListView.customContextMenuRequested.connect(self.folderRightClicked)

		self.ui.recentProjectsListView.doubleClicked.connect(self.recentProjectSelected)
		self.ui.fileTreeView.doubleClicked.connect(self.fileTreeSelected)

	def chosenPath(self):
		return self.__lastPath

	@Slot(QModelIndex)
	def recentProjectSelected(self,index):
		self.__lastPath=self.__recentProjectsModel.data(index,Qt.UserRole)
		self.accepted.emit()
		self.hide()

	@Slot(QModelIndex)
	def fileTreeSelected(self,index):
		self.__lastPath = self.__fileModel.filePath(index)
		self.accepted.emit()
		self.hide()

	@Slot(QPoint)
	def folderRightClicked(self,pos):
		#supposed to be connected to QAbstractView
		wid=self.sender()
		index=wid.indexAt(pos)
		if(index.isValid()):
			menu=QMenu("what to do",self)
			if(wid==self.ui.fileTreeView):
				action=menu.addAction("save folder to quick projects")
				action.setData([0,index])
			else:
				action = menu.addAction("show in right window")
				action.setData([11, index])
				action = menu.addAction("remove from list")
				action.setData([10, index])

			menu.triggered.connect(self.folderMenuTriggered)
			menu.popup(wid.mapToGlobal(pos))
			menu.aboutToHide.connect(menu.deleteLater)

	@Slot(QAction)
	def folderMenuTriggered(self,action):
		actionId=action.data()[0]
		if(actionId==0):
			index = action.data()[1]
			if(index.isValid()):
				filepath = self.ui.fileTreeView.model().filePath(index)
				filename = self.ui.fileTreeView.model().fileName(index)
				print(filepath)
				self.__recentProjectsModel.addToList([filename,filepath])
		elif(actionId==10):
			index = action.data()[1]
			if(index.isValid()):
				self.__recentProjectsModel.removeRow(index.row())
		elif (actionId == 11):
			index = action.data()[1]
			if (index.isValid()):
				filepath=self.__recentProjectsModel.data(index,Qt.UserRole)
				fileindex=self.__fileModel.index(filepath)
				if(fileindex.isValid()):
					self.ui.fileTreeView.setCurrentIndex(fileindex)
				else:
					pass
					#TODO: add here a warning dialogue with remove this shit option

		self.sender().deleteLater()


####QT overrides
	def changeEvent(self,event):
		super(ProjectDialog,self).changeEvent(event)
		if(self.isVisible() and event.type()==QEvent.ActivationChange and not self.isActiveWindow()):
			self.hide()
			event.accept()

#TESTING
if(__name__=='__main__'):
	import sys
	qapp = QApplication(sys.argv)
	qapp.setApplicationName("CGlauncher")
	settingspath=QDesktopServices.storageLocation(QDesktopServices.DataLocation)
	if(not os.path.exists(settingspath)):os.makedirs(settingspath)

	w = ProjectDialog()
	w.accepted.connect(lambda:pprint(w.chosenPath()))
	w.show()

	sys.exit(qapp.exec_())

