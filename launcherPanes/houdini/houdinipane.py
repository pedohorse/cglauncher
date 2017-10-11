import os
import subprocess

from PySide.QtCore import *
from PySide.QtGui import *

# import json
import re

from ..baselauncherpane import BaseLauncherPane
import houdini_ui
import houdini_rc

from project import *
import houutils

import projectdialog

from pprint import pprint


class HoudiniConfig(QObject):
	# signals
	newVersionsDetected = Signal()

	def __init__(self, parent=None):
		super(HoudiniConfig, self).__init__(parent)

		self.__houdinies = {}
		self.rescan()

	def rescan(self):
		overs = set(self.__houdinies.keys())
		self.__houdinies = houutils.locateHoudinies()
		if (set(self.__houdinies.keys()) != overs): self.newVersionsDetected.emit()

	def allVersions(self):
		return self.__houdinies

	def getClosestVersion(self, ver=()):
		return houutils.getClosestVersion(ver, self.allVersions())

	def getClosestVersionPath(self, ver=()):
		return self.allVersions()[self.getClosestVersion(ver)]


class HoudiniPane(BaseLauncherPane):
	def __init__(self, parent=None):
		super(HoudiniPane, self).__init__(parent)
		self.__blockUICallbacks = False
		self.__projectPathChangedInProgress = False
		self.__project = None

		self.ui = houdini_ui.Ui_houdiniMenu()

		self.ui.setupUi(self)
		#extra background layout
		self.ui.bkgProjectLabel=QLabel("launcher",self)
		self.ui.bkgProjectLabel.setObjectName("bkgProjectLabel")
		self.ui.bkgProjectLabel.setStyleSheet('QLabel#bkgProjectLabel{font-size: 128px; color: rgb(64,64,64);}')
		self.ui.bkgProjectLabel.move(190,180)
		#self.bkgProjectLabel.setAlignment(Qt.AlignVCenter|Qt.AlignRight)
		self.ui.bkgProjectLabel.adjustSize()
		self.ui.bkgProjectLabel.lower()

		self.__sceneFileModel=QFileSystemModel(self)
		self.__sceneFileModel.setNameFilters(["*.hip","*.hipnc"])
		#self.__sceneFileModel.setFilter(QDir.Files | QDir.Dirs | QDir.NoDotAndDotDot)
		self.__sceneFileModel.setNameFilterDisables(False)
		self.ui.sceneFilesTreeView.doubleClicked.connect(self.sceneFileTreeDoubleClicked)


		# self.ui.envTableView.setModel(EnvTableModel())
		# self.ui.envTableView.verticalHeader().setMovable(True)
		# self.ui.envTableView.horizontalHeader().setStretchLastSection(True)
		# self.ui.envTableView.verticalHeader().setStretchLastSection(False)

		self.__projectDialog=projectdialog.ProjectDialog('houdini',self)
		self.__projectDialog.accepted.connect(self.projectDialogSelected)

		self.__houconf = HoudiniConfig()
		self.ui.houVersionComboBox.clear()
		for ver in self.__houconf.allVersions().keys():
			self.ui.houVersionComboBox.addItem('.'.join((str(x) for x in ver)), ver)

		# for default project add default config
		# there should be no name collisions, cuz we r adding to the empty default project
		if (len(self.__houconf.allVersions()) == 0):
			# houdini not found
			self.setEnabled(False)
			return

		# setup signals
		self.ui.configComboBox.currentIndexChanged[str].connect(self.configSelected)
		self.ui.houVersionComboBox.currentIndexChanged[int].connect(self.uiHouVerChanged)
		self.ui.binNameComboBox.editTextChanged.connect(self.binaryChanged)
		self.ui.newConfigPushButton.clicked.connect(self.newConfigButtonPressed)
		self.ui.renameConfigPushButton.clicked.connect(self.renameConfigButtonPressed)
		self.ui.delConfigPushButton.clicked.connect(self.configRemoveButtonPressed)
		self.ui.launchPushButton.clicked.connect(self.launchButtonPressed)

		self.ui.projectPathLine.editingFinished.connect(self.projectPathChanged)
		self.ui.saveProjectPushButton.clicked.connect(self.saveProjectButtonPressed)

		self.ui.projectPathPushButton.clicked.connect(self.selectProjectClicked)

		# set default project
		self.__settingspath = QDesktopServices.storageLocation(QDesktopServices.DataLocation)
		defProject = Project(os.path.join(self.__settingspath,'default.project')) #TODO: he's not deleted when project's changed, and yet we dont keep a ref to it
		if(len(defProject.configs())==0):
			defProject.addConfig(ProjectConfig('default', self.__houconf.getClosestVersion()))
			defProject.sync()
		self.setProject(defProject)

	def setProject(self, project):
		# disconnect old project
		print("\n\n-----------------\n--NEW-PROJECT----\n-----------------")
		if (self.__project is not None):
			try:
				self.__project.configAdded.disconnect(self.configAdded)  #
				self.__project.configRemoved.disconnect(self.configRemoved)  #
			# TOTO:figure out why disconnect sometimes doesnt work
			except Exception as e:
				print("Pane: strange error during disconnecting: %s"%e.message)
			#self.__project.deleteLater()
		self.setConfig(None)
		self.__project = project

		self.ui.configComboBox.clear()
		self.ui.sceneFilesTreeView.setModel(None)
		if (self.__project is not None):
			self.ui.configComboBox.addItems([conf for conf in self.__project.configs()])

			self.__project.configAdded.connect(self.configAdded)
			self.__project.configRemoved.connect(self.configRemoved)

			#now set some ui
			filename = self.__project.filename()
			self.ui.bkgProjectLabel.setText(os.path.basename(os.path.normpath(os.path.dirname(filename))))
			self.ui.bkgProjectLabel.adjustSize()
			index =self.__sceneFileModel.setRootPath(os.path.dirname(filename))
			self.ui.sceneFilesTreeView.setModel(self.__sceneFileModel)
			self.ui.sceneFilesTreeView.setRootIndex(index)
			self.ui.sceneFilesTreeView.setColumnHidden(2, True)
			self.ui.sceneFilesTreeView.setColumnWidth(0, 256)
			self.ui.sceneFilesTreeView.setColumnWidth(1, 64)

	def setConfig(self, config):  # all UI is driven by model callbacks after config is set
		'''
		set UI to show config
		:param config: ProjectConfig or None
		:return:
		'''
		oldState = self.__blockUICallbacks
		self.__blockUICallbacks = True
		try:
			# setting down
			oldconfig=self.ui.envTableView.model()
			if(oldconfig is not None):
				oldconfig.otherDataChanged.disconnect(self.otherDataFromConfig)

			self.ui.envTableView.setModel(None)
			# setting up
			if (config is not None):
				config.otherDataChanged.connect(self.otherDataFromConfig)
				self.otherDataFromConfig(config.allOtherData())

				self.ui.envTableView.setModel(config)
		except Exception as e:
			print("shit happened: %s = %s" % (str(type(e)), str(e.message)))
		finally:
			self.__blockUICallbacks = oldState

	# UI callbacks

	def launch(self, extraattribs=None):
		conf = self.__project.config(self.ui.configComboBox.currentText())
		if (conf is None):
			print("failed to obtain config")
			return

		filepath = self.__houconf.getClosestVersionPath(conf.houVer())
		binname=self.ui.binNameComboBox.currentText()
		filename=None
		try:
			filenamecandidates=[x for x in os.listdir(os.path.join(filepath, 'bin')) if os.path.splitext(x)[0]==binname]
			if(len(filenamecandidates)==0):raise RuntimeError('no binary found')
			elif(len(filenamecandidates)>1):raise RuntimeError('multiple matching files to launch found')
			filename=filenamecandidates[0]
		except Exception as e:
			print("HoudiniPane: launch failed: %s"%e.message)
			return
		filepath = os.path.join(filepath, 'bin', filename)
		# now set env
		env = os.environ.copy()
		envtokendict={'PWD':os.path.dirname(self.__project.filename())}
		for i in xrange(conf.rowCount() - 1):
			name = conf.data(conf.index(i, 0))
			val = conf.data(conf.index(i, 1))
			if (name == ''): continue
			val = re.sub(r'\[(\S+)\]',lambda match:envtokendict[match.group(1)] if match.group(1) in envtokendict else '',val)
			env[str(name)] = str(val) #just so no unicode
		print(filepath)
		pprint(env)
		if(extraattribs is not None):
			assert isinstance(extraattribs,tuple) or isinstance(extraattribs,list), 'extra attributes must be either list or tuple'
			filepath=[filepath]+list(extraattribs)
		print(filepath)
		subprocess.Popen(filepath, stdin=None, stdout=None, stderr=None, env=env)#, cwd=os.path.dirname(filepath))

	@Slot()
	def sceneFileTreeDoubleClicked(self,index):
		try:
			filepath=self.__sceneFileModel.filePath(index)
		except:
			print("internal error")
			return
		self.launch([filepath])

	@Slot()
	def launchButtonPressed(self):
		self.launch()

	@Slot()
	def projectDialogSelected(self):
		self.ui.projectPathLine.setText(self.__projectDialog.chosenPath())
		self.projectPathChanged()

	# Model-to-UI callbacks
	@Slot()
	def otherDataFromConfig(self, dictdata):
		self.__blockUICallbacks = True
		# if u want any UI-to-model callbacks to happen - think twice and modify model directly
		try:
			keys = dictdata.keys()
			if ('ver' in keys):
				data = dictdata['ver']
				# houfound = False
				for i in xrange(self.ui.houVersionComboBox.count()):
					if (data == tuple(self.ui.houVersionComboBox.itemData(i))):
						self.ui.houVersionComboBox.setCurrentIndex(i)
						# houfound = True
						break
					# if (not houfound): return
			if ('binary' in keys):
				data = dictdata['binary']
				self.ui.binNameComboBox.setEditText(data)
			if('name' in keys):
				data = dictdata['name']
				self.ui.configComboBox.setItemText(self.ui.configComboBox.currentIndex(),data)
		finally:
			self.__blockUICallbacks = False

	@Slot()
	def configAdded(self, config):
		self.ui.configComboBox.addItem(config.name())
		self.ui.configComboBox.setCurrentIndex(self.ui.configComboBox.count() - 1)

	@Slot(str)
	def configRemoved(self, confName):
		id = self.ui.configComboBox.findText(confName)
		if (id < 0): return
		self.ui.configComboBox.removeItem(id)


#####UI-to-model callbacks
	@Slot(str)
	def configSelected(self, text):
		if (self.__blockUICallbacks): return
		self.setConfig(self.__project.config(text))

	@Slot()
	def projectPathChanged(self):
		'''
		:param value:
		:return:
		'''
		if (self.__projectPathChangedInProgress): return
		self.__projectPathChangedInProgress = True
		try:
			value = self.ui.projectPathLine.text()
			self.ui.projectPathLine.clearFocus()
			gooddir = os.path.isdir(value) and os.path.exists(value)
			self.ui.saveProjectPushButton.setEnabled(gooddir or value=='')
			if (gooddir):
				if(self.__project.syncNeeded()):
					button=QMessageBox.question(self, 'unsaved changes', 'what to do?', buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
					if(button==QMessageBox.Save):
						self.__project.sync()
					elif(button==QMessageBox.Cancel):
						self.ui.projectPathLine.setText(os.path.dirname(self.__project.filename()))
						return

				projectfile = os.path.join(value, 'houdini.project')
				if (os.path.isfile(projectfile)):
					self.setProject(Project(projectfile))
				else:
					button=QMessageBox.question(self,'no project found','copy current project in this location?',buttons=QMessageBox.Yes|QMessageBox.RestoreDefaults|QMessageBox.Cancel)
					if(button==QMessageBox.Yes):
						self.__project.setFilename(projectfile)
						self.__project.sync()
					elif(button==QMessageBox.RestoreDefaults):
						newproj=Project(os.path.join(self.__settingspath, 'default.project'))
						newproj.setFilename(projectfile)
						self.setProject(newproj)
					else:
						self.ui.projectPathLine.setText(os.path.dirname(self.__project.filename()))
						return
			elif(value==''):
				self.setProject(Project(os.path.join(self.__settingspath, 'default.project')))
			else:
				self.ui.projectPathLine.setText(os.path.dirname(self.__project.filename()))
				return
		finally:
			self.__projectPathChangedInProgress = False

	@Slot(int)
	def uiHouVerChanged(self, id):
		if (self.__blockUICallbacks): return
		conf = self.__project.config(self.ui.configComboBox.currentText())
		conf.setOtherData('ver', tuple(self.ui.houVersionComboBox.itemData(id)))

	@Slot(str)
	def binaryChanged(self, text):
		if (self.__blockUICallbacks): return
		conf = self.__project.config(self.ui.configComboBox.currentText())
		conf.setOtherData('binary', text)

#	# Buttons Callbacks
	@Slot()
	def selectProjectClicked(self):
		self.__projectDialog.move(QCursor.pos())
		self.__projectDialog.show()


	@Slot()
	def newConfigButtonPressed(self):
		if (self.__blockUICallbacks): return
		name, good = QInputDialog.getText(self, 'new config', 'enter unique name')
		if (not good): return
		self.__project.addConfig(ProjectConfig(name, tuple(self.ui.houVersionComboBox.itemData(self.ui.houVersionComboBox.currentIndex()))))

	@Slot()
	def renameConfigButtonPressed(self):
		if (self.__blockUICallbacks): return
		if (self.ui.configComboBox.count() == 0): return
		oldname=self.ui.configComboBox.currentText()
		newname, good = QInputDialog.getText(self, 'new config', 'enter unique name',text=oldname)
		if (not good): return
		self.__project.config(oldname).rename(self.__project.makeUniqueConfigName(newname))

	@Slot()
	def configRemoveButtonPressed(self):
		if (self.__blockUICallbacks): return
		if(self.ui.configComboBox.count()==0):return
		# TODO: add popup
		self.__project.removeConfig(self.ui.configComboBox.currentText())

	@Slot()
	def saveProjectButtonPressed(self):
		if (self.__project is None): return
		self.__project.sync()


##### PANE IMPLEMENTATION
	def paneHeader(self):
		return ('Houdini', ':/icons/houdini/houlogo.png')
