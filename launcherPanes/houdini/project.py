
from PySide.QtCore import *
from PySide.QtGui import *

import json
import re




# project stuff
class IncompatibleVersionError(Exception):
	pass

class ConfigNameCollisionError(Exception):
	pass

class ProjectConfig(QAbstractTableModel):pass #forwarf

class Project(QObject):
	# signals
	configAdded = Signal(ProjectConfig)
	configRemoved = Signal(str)

	__currentFormatVersion=(1,0)
	__projectTemplateStr=json.dumps({'formatVersion':list(__currentFormatVersion)},indent=4)

	def __init__(self,projectfilename=None):
		super(Project,self).__init__()
		self.__configs=[]
		self.__projectFileName=projectfilename
		self.__formatVersion=Project.__currentFormatVersion
		self.__saveNeeded=False


		if(self.__projectFileName is not None):
			try:
				self.__loadFromFile(self.__projectFileName)
			except Exception as e:
				print("Project: couldnt load %s"%e.message)
				try:
					with open(self.__projectFileName,'w') as f:
						f.write(Project.__projectTemplateStr)
					self.__saveNeeded = True
				except:
					raise RuntimeError("Project: cannot access the project file")

	def makeUniqueConfigName(self,name):
		newname=name
		good=False
		for x in xrange(9999): #we try to resolve name collisions till it's resolved or till we hit trying limit
			if(len([x for x in self.__configs if x.name()==newname])>0):
				#so we have a name collision
				try:
					match=re.match(r'((\D*\d*)*(?<=\D)|^)(\d*)$',newname)
					if(match is not None):
						id=0
						if(match.group(3)!=''):id=int(match.group(3))
						newname=match.group(1)+str(id+1)
				except Exception as e:
					print(e.message)
					raise ConfigNameCollisionError("unique config name could not be found")
			else:
				good=True
				break

		if(not good):raise ConfigNameCollisionError("unique config name could not be found")
		return newname

	def addConfig(self,newConfig):
		newConfig.rename(self.makeUniqueConfigName(newConfig.name()))
		self.__configs.append(newConfig)
		newConfig.dataChanged.connect(self.configChanged)
		newConfig.columnsRemoved.connect(self.configChanged)
		newConfig.columnsInserted.connect(self.configChanged)
		self.configAdded.emit(newConfig)

	def removeConfig(self,name):
		if(name not in self.configs()):return
		todel=[]
		for x in self.__configs:
			if(x.name()==name):
				todel.append(x)
				x.dataChanged.disconnect(self.configChanged)
				x.columnsRemoved.disconnect(self.configChanged)
				x.columnsInserted.disconnect(self.configChanged)

		for x in todel:
			self.__configs.remove(x)

		#no deleteLater - let gc do it's job,
		self.configRemoved.emit(name)

	def configs(self):
		return [x.name() for x in self.__configs]

	def config(self,configName):
		pot=[x for x in self.__configs if x.name()==configName]
		if(len(pot)==0):return None
		return pot[0]

	def filename(self):
		if(self.__projectFileName is None):return ''
		else: return self.__projectFileName

	def setFilename(self,filename):
		'''
		reattaches Project to another file or detaches from file if filename is None
		:param filename: str or None
		:return:
		'''
		self.__projectFileName=filename
		self.__saveNeeded=self.__projectFileName is not None

	def __loadFromFile(self,filename):
		with open(filename,'r') as f:
			valuesDict=json.load(f)

		try:
			self.__formatVersion=tuple(valuesDict['formatVersion'])
			if(self.__formatVersion[0]>Project.__currentFormatVersion[0]):raise IncompatibleVersionError("Config major version higher")
			for cfgdict in valuesDict['configs']:
				try:
					config=ProjectConfig(valuesDict=cfgdict)
					self.addConfig(config)
				except Exception as e:
					print('Couldnt load config: %s'%e.message)
					#TODO: make a logging system
					continue
		except KeyError as e:
			raise RuntimeError("Config: Couldn't load config: unknown key %s"%(e.message,))

	def syncNeeded(self):
		return self.__saveNeeded

	def sync(self):
		if(self.__projectFileName is None):return
		res={}
		res['formatVersion']=Project.__currentFormatVersion
		res['configs']=[x.dataSerialize() for x in self.__configs]
		with open(self.__projectFileName,'w') as f:
			json.dump(res,f,indent=4)

		#set state to synced
		self.__saveNeeded=False

	#Config callback
	@Slot()
	def configChanged(self):
		self.__saveNeeded=True


class ProjectConfig(QAbstractTableModel):
	otherDataChanged=Signal(dict)
	__currentFormatVersion = (1, 0)

	def __init__(self, name=None, ver=None, valuesDict=None):
		super(ProjectConfig, self).__init__()

		if(name is not None and ver is None or name is None and ver is not None or valuesDict is not None and (name is not None or ver is not None)):raise RuntimeError("either give name and ver, or valuesDict")

		self.__data=[]
		self.__otherData={'binary':'hmaster','ver':(0,0,0),'name':'default'}
		self.__formatVersion = ProjectConfig.__currentFormatVersion
		if(ver is not None):self.setOtherData('ver',ver) #TODO: make more readable, cuz now it looks like there's a possibility for ver not to be set, but it's not
		if(name is not None):self.setOtherData('name',name)

		if (valuesDict is not None): self.__loadFromData(valuesDict)


	def __loadFromData(self,valuesData):
		try:
			self.beginResetModel()
			self.__formatVersion=tuple(valuesData['formatVersion'])
			if(self.__formatVersion[0]>ProjectConfig.__currentFormatVersion[0]):raise IncompatibleVersionError("Config major version higher")
			self.__data=valuesData['env']+[] #to copy data

			#TODO: maybe in analogue with dataSerialize - just shove in all unprocessed keys?
			self.setOtherData('name',valuesData['name'])
			self.setOtherData('ver',tuple(valuesData['version']))
			self.setOtherData('binary',valuesData['binary'])
		except KeyError as e:
			raise RuntimeError("Config: Couldn't load config: unknown key %s"%(e.message,))
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
		res['name'] = self.otherData('name')
		res['version']=self.otherData('ver')
		res['binary']=self.otherData('binary')
		return res

#Get/Set stuff
	def allOtherData(self):
		return dict(self.__otherData)

	def otherData(self,dataName):
		return self.__otherData[dataName]

	def setOtherData(self,dataName,dataVal):
		if(dataName=='ver'):
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
		return self.otherData('ver')

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


