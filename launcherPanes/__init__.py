#this will have a list of available plugins
import os
import importlib
import inspect

import re

from baselauncherpane import BaseLauncherPane




pluginClassList=[]
pluginModuleList=[]

def rescanPlugins():
	global pluginClassList
	global pluginModuleList
	global __all__
	pluginClassList = []
	pluginModuleList = []
	thisdir=os.path.dirname(__file__)
	ls=os.listdir(thisdir)
	files=[os.path.splitext(x)[0] for x in ls if os.path.splitext(x)[1]==".py" and x!="__init__.py" and x!='baselauncherpane.py' and not re.match(r'.+(_rc)|(_ui)$',os.path.splitext(x)[0])]
	dirs=[x for x in ls if os.path.exists(os.path.join(thisdir,x,'__init__.py'))]

	for fn in files+dirs:
		try:
			newmodule=importlib.import_module(".".join((__name__,fn)))
			reload(newmodule)
		except Exception as e:
			print("Launcher Panes: failed to load module %s"%fn)
			print("cuz: %s"%e.message)
			continue
		for name,obj in inspect.getmembers(newmodule):
			if(inspect.isclass(obj) and BaseLauncherPane in inspect.getmro(obj)[1:]):
				pluginModuleList.append(newmodule)
				pluginClassList.append(obj)



rescanPlugins()