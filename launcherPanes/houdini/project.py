
from PySide2.QtCore import QObject, Slot, Signal, QAbstractTableModel, Qt, QModelIndex

import json
import re

from typing import Optional


# project stuff
class IncompatibleVersionError(Exception):
	pass


class ConfigNameCollisionError(Exception):
	pass


class ProjectConfig(QAbstractTableModel):  # forward declaration
	pass


class Project(QObject):
	# signals
	configAdded = Signal(ProjectConfig)
	configRemoved = Signal(str)
	project_file_path_changed = Signal(str)

	__currentFormatVersion = (1, 0)
	__projectTemplateStr = json.dumps({'formatVersion': list(__currentFormatVersion)}, indent=4)

	def __init__(self, project_file_path: Optional[str] = None):
		super(Project, self).__init__()
		self.__configs = []
		self.__projectFilePath = project_file_path
		self.__formatVersion = Project.__currentFormatVersion
		self.__saveNeeded = False

		if self.__projectFilePath is not None:
			try:
				self.__loadFromFile(self.__projectFilePath)
			except Exception as e:
				print("Project: couldnt load %s" % repr(e))
				try:
					with open(self.__projectFilePath, 'w') as f:
						f.write(Project.__projectTemplateStr)
					self.__saveNeeded = True
				except:
					raise RuntimeError("Project: cannot access the project file")

	def make_unique_config_name(self, name):
		newname = name
		good = False
		for x in range(9999):  # we try to resolve name collisions till it's resolved or till we hit trying limit
			if len([x for x in self.__configs if x.name() == newname]) > 0:
				# so we have a name collision
				try:
					match = re.match(r'((\D*\d*)*(?<=\D)|^)(\d*)$', newname) # TODO: optimize this regexp
					if match is not None:
						id = 0
						if match.group(3) != '':
							id = int(match.group(3))
						newname=match.group(1)+str(id+1)
				except Exception as e:
					print(e)
					raise ConfigNameCollisionError("unique config name could not be found")
			else:
				good = True
				break
		if not good:
			raise ConfigNameCollisionError("unique config name could not be found")
		return newname

	def add_config(self, new_config):
		new_config.rename(self.make_unique_config_name(new_config.name()))
		self.__configs.append(new_config)
		new_config.dataChanged.connect(self.config_changed)
		new_config.columnsRemoved.connect(self.config_changed)
		new_config.columnsInserted.connect(self.config_changed)
		self.configAdded.emit(new_config)

	def remove_config(self, name):
		if name not in self.configs():
			return
		todel = []
		for x in self.__configs:
			if x.name() == name:
				todel.append(x)
				x.dataChanged.disconnect(self.config_changed)
				x.columnsRemoved.disconnect(self.config_changed)
				x.columnsInserted.disconnect(self.config_changed)

		for x in todel:
			self.__configs.remove(x)

		# no deleteLater - let gc do it's job,
		self.configRemoved.emit(name)

	def configs(self):
		return [x.name() for x in self.__configs]

	def config(self, config_name: str):
		pot = [x for x in self.__configs if x.name() == config_name]
		if len(pot) == 0:
			return None
		return pot[0]

	def file_path(self) -> str:
		if self.__projectFilePath is None:
			return ''
		else:
			return self.__projectFilePath

	def set_file_path(self, file_path: str) -> None:
		"""
		reattaches Project to another file or detaches from file if file_path is None
		:param file_path: str or None
		:return:
		"""
		self.__projectFilePath = file_path
		self.__saveNeeded = self.__projectFilePath is not None
		self.project_file_path_changed.emit(file_path)

	def __loadFromFile(self, filename):
		with open(filename,'r') as f:
			valuesDict=json.load(f)

		try:
			self.__formatVersion=tuple(valuesDict['formatVersion'])
			if(self.__formatVersion[0]>Project.__currentFormatVersion[0]):raise IncompatibleVersionError("Config major version higher")
			for cfgdict in valuesDict['configs']:
				try:
					config=ProjectConfig(values_dict=cfgdict)
					self.add_config(config)
				except Exception as e:
					print('Couldnt load config: %s'%e.message)
					#TODO: make a logging system
					continue
		except KeyError as e:
			raise RuntimeError("Config: Couldn't load config: unknown key %s"%(e.message,))

	def sync_needed(self):
		return self.__saveNeeded

	def sync(self):
		if self.__projectFilePath is None:
			return
		res = dict()
		res['formatVersion'] = Project.__currentFormatVersion
		res['configs'] = [x.dataSerialize() for x in self.__configs]
		with open(self.__projectFilePath, 'w') as f:
			json.dump(res, f, indent=4)

		# set state to synced
		self.__saveNeeded = False

	# Config callback
	@Slot()
	def config_changed(self):
		self.__saveNeeded = True


class ProjectConfig(QAbstractTableModel):
	otherDataChanged = Signal(dict)
	__currentFormatVersion = (1, 1)

	def __init__(self, name=None, ver=None, values_dict=None):
		super(ProjectConfig, self).__init__()

		if name is not None and ver is None \
					or name is None and ver is not None \
					or values_dict is not None and (name is not None or ver is not None):
			raise RuntimeError("either give name and ver, or valuesDict")

		self.__data = []
		self.__otherData = {'binary': 'hmaster', 'version': (0, 0, 0), 'name': 'default', 'args': ''}
		self.__formatVersion = ProjectConfig.__currentFormatVersion
		if ver is not None:
			self.setOtherData('version', ver)  # TODO: make more readable, cuz now it looks like there's a possibility for ver not to be set, but it's not
		if name is not None:
			self.setOtherData('name', name)
		if values_dict is not None:
			self.__load_from_data(values_dict)

	def __load_from_data(self, values_data):
		try:
			self.beginResetModel()
			self.__formatVersion=tuple(values_data['formatVersion'])
			if self.__formatVersion[0] > ProjectConfig.__currentFormatVersion[0]:
				raise IncompatibleVersionError("Config major version higher")
			self.__data = values_data['env'] + []  # to copy data

			# TODO: maybe in analogue with dataSerialize - just shove in all unprocessed keys?
			for key in values_data.keys():
				if key == 'env' or key == 'formatVersion':
					continue
				data = values_data[key]
				if key == 'version':
					data = tuple(data)
				self.setOtherData(key, data)
		except KeyError as e:
			raise RuntimeError("Config: Couldn't load config: unknown key %s" % repr(e))
		finally:
			self.endResetModel()

	def dataSerialize(self):
		'''
		actually not serialize, but convert to dict
		:return: a json-eatable structure (dict of lists and shit)
		'''
		res={}
		res['formatVersion']=ProjectConfig.__currentFormatVersion
		res['env']=self.__data+[] #TO COPY

		#TODO: replace with: for key in self.__otherData:res[key]=self.__otherData[key]
		for key in self.__otherData.keys():
			if (key == 'env' or key == 'formatVersion'): continue
			res[key] = self.otherData(key)

		return res

#Get/Set stuff
	def allOtherData(self):
		return dict(self.__otherData)

	def otherData(self,dataName):
		return self.__otherData[dataName]

	def setOtherData(self,dataName,dataVal):
		if(dataName=='version'):
			if (not isinstance(dataVal, tuple) or len(dataVal) != 3): raise TypeError("version must be a 3 int tuple")
		self.__otherData[dataName]=dataVal
		self.otherDataChanged.emit({dataName:dataVal})

	def rename(self,newName):
		''' shortcut to otherData '''
		self.setOtherData('name',newName)

	def name(self):
		''' shortcut to otherData '''
		return self.otherData('name')

	def houVer(self):
		''' shortcut to otherData '''
		return self.otherData('version')

#QAbstractModel implementation
	def rowCount(self, parent=None):
		if(parent is None):parent=QModelIndex()
		if(parent!=QModelIndex()):
			raise RuntimeError("something wrong with rowCount")
		return len(self.__data)+1

	def columnCount(self, parent=None):
		if (parent is None): parent = QModelIndex()
		if(parent != QModelIndex()):
			raise RuntimeError("something wrong with columnCount")
		return 2

	def data(self, index, role=Qt.DisplayRole):
		if(role!=Qt.DisplayRole and role!=Qt.EditRole):return None
		row=index.row()
		if(row==self.rowCount()-1):return ''
		return self.__data[row][index.column()]

	def setData(self,index, value, role):
		if(role!=Qt.EditRole):return False
		col=index.column()
		row=index.row()
		if(row==self.rowCount()-1):
			if(value==''):return False
			else:self.insertRows(row,1)

		self.__data[row][col]=str(value)
		if(value=='' and self.__data[row][(col+1)%2]==''):self.removeRows(row,1)
		else:self.dataChanged.emit(index,index)
		return True

	def insertRows(self, row, count, parent=None):
		if(parent is None):parent = QModelIndex()
		#parent should be default
		self.beginInsertRows(parent,row,row+count-1)
		self.__data+=[['','']]*count
		self.endInsertRows()
		return True

	def removeRows(self,row,count,parent=None):
		if (parent is None): parent = QModelIndex()
		# parent should be default
		self.beginRemoveRows(parent,row,row+count-1)
		self.__data=self.__data[:row]+self.__data[row+count:]
		self.endRemoveRows()


	def flags(self, index):
		return Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled


	def headerData(self, section, orientation, role):
		if(role!=Qt.DisplayRole):return None
		if(orientation==Qt.Orientation.Vertical):return section
		return ['name','value'][section]


