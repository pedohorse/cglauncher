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


		# self.ui.envTableView.setModel(EnvTableModel())
		# self.ui.envTableView.verticalHeader().setMovable(True)
		# self.ui.envTableView.horizontalHeader().setStretchLastSection(True)
		# self.ui.envTableView.verticalHeader().setStretchLastSection(False)

		self.__projectDialog=projectdialog.ProjectDialog(self)
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
		self.ui.delConfigPushButton.clicked.connect(self.configRemoveButtonPressed)
		self.ui.launchPushButton.clicked.connect(self.launchButtonPressed)

		self.ui.projectPathLine.editingFinished.connect(self.projectPathChanged)
		self.ui.saveProjectPushButton.clicked.connect(self.saveProjectButtonPressed)

		self.ui.projectPathPushButton.clicked.connect(self.selectProjectClicked)

		# set default project
		settingspath = QDesktopServices.storageLocation(QDesktopServices.DataLocation)
		defProject = Project(os.path.join(settingspath,'default.project'))
		if(len(defProject.configs())==0):
			defProject.addConfig(ProjectConfig('default', self.__houconf.getClosestVersion()))
			defProject.sync()
		self.setProject(defProject)

	def setProject(self, project):
		# disconnect old project
		print("\n\n-----------------\n--NEW-PROJECT----\n-----------------")
		if (self.__project is not None):
			try:
				self.__project.configAdded.disconnect()  # self.configAdded
				self.__project.configRemoved.disconnect()  # self.configRemoved
			# TOTO:figure out why disconnect sometimes doesnt work
			except:
				print("Pane: strange error during disconnecting")
			self.__project.deleteLater()
		self.setConfig(None)
		self.__project = project

		self.ui.configComboBox.clear()
		self.ui.configComboBox.addItems([conf for conf in self.__project.configs()])

		self.__project.configAdded.connect(self.configAdded)
		self.__project.configRemoved.connect(self.configRemoved)

	def setConfig(self, config):  # TODO: make all UI fields be set by callbacks ?
		'''
		set UI to show config
		:param config: ProjectConfig or None
		:return:
		'''
		oldState = self.__blockUICallbacks
		self.__blockUICallbacks = True
		try:
			# setting version ui
			self.ui.envTableView.setModel(None)
			if (config is not None):
				self.otherDataFromConfig(config.allOtherData())
				self.ui.envTableView.setModel(config)
		except Exception as e:
			print("shit happened: %s = %s" % (str(type(e)), str(e.message)))
		finally:
			self.__blockUICallbacks = oldState

	# UI callbacks


	@Slot()
	def launchButtonPressed(self):
		conf = self.__project.config(self.ui.configComboBox.currentText())
		if (conf is None):
			print("failed to obtain config")
			return

		filepath = self.__houconf.getClosestVersionPath(conf.houVer())
		filepath = os.path.join(filepath, 'bin', '.'.join((self.ui.binNameComboBox.currentText(), 'exe')))  # TODO:bin name should be part of config
		# TODO: that exe makes this shit pretty non cross-platform...
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
		print(os.path.dirname(filepath))
		subprocess.Popen(filepath, stdin=None, stdout=None, stderr=None, env=env, cwd=os.path.dirname(filepath))

	@Slot()
	def projectDialogSelected(self):
		self.ui.projectPathLine.setText(self.__projectDialog.chosenPath())
		self.projectPathChanged()

	# Model-to-UI callbacks
	@Slot(str, object)
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
			#TODO: add all remaining keys
		finally:
			self.__blockUICallbacks = False

	@Slot(ProjectConfig)
	def configAdded(self, config):
		self.ui.configComboBox.addItem(config.name())
		# TODO: check name collision and rename
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
			# TODO: check if there are unsaved changed, popup
			# print("textChanged")
			self.ui.projectPathLine.clearFocus()
			gooddir = os.path.isdir(value) and os.path.exists(value)
			self.ui.saveProjectPushButton.setEnabled(gooddir or value=='')
			if (gooddir):
				# TODO: check if folder haz no project - ask if to keep current, or start from scratch
				self.ui.bkgProjectLabel.setText(os.path.basename(value))
				self.ui.bkgProjectLabel.adjustSize()
				projectfile = os.path.join(value, 'houdini.project')
				if (os.path.isfile(projectfile)):
					self.setProject(Project(projectfile))
				else:
					self.__project.setFilename(projectfile)
			elif(value==''):
				settingspath = QDesktopServices.storageLocation(QDesktopServices.DataLocation)
				self.ui.bkgProjectLabel.setText('launcher')
				self.setProject(Project(os.path.join(settingspath, 'default.project')))
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
		name, good = QInputDialog.getText(self, 'enter name', 'you bastard')
		if (not good): return
		self.__project.addConfig(ProjectConfig(name, tuple(self.ui.houVersionComboBox.itemData(self.ui.houVersionComboBox.currentIndex()))))

	@Slot()
	def configRemoveButtonPressed(self):
		if (self.__blockUICallbacks): return
		# TODO: add popup
		self.__project.removeConfig(self.ui.configComboBox.currentText())

	@Slot()
	def saveProjectButtonPressed(self):
		if (self.__project is None): return
		self.__project.sync()


##### PANE IMPLEMENTATION
	def paneHeader(self):
		return ('Houdini', ':/icons/houdini/houlogo.png')
