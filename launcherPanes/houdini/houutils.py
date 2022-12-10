import os
import subprocess
import re

import platform
import inspect

from typing import Optional, List

#/Applications/Houdini/Houdini16.0.628/Frameworks/Houdini.framework/Versions/16.0.628/Resources/bin/houdinifx
def locateHoudinies(extraPathList=None):

	system=platform.system()
	if system=='Windows':
		commonpaths = [r"C:\Program Files\Side Effects Software"]
	elif system=='Linux':
		commonpaths = [r"/opt"]
	elif system=='Darwin':
		commonpaths = ["r/Applications/Houdini"]
	else:
		raise RuntimeError("looks like someone purposefully deleted you OS from jedi archives...")
	if extraPathList is not None:
		commonpaths += extraPathList

	houdinies = {}
	for path in commonpaths:
		dirs = []
		try:
			dirs = os.listdir(path)
		except:
			continue

		for dir in dirs:
			if system == 'Windows':
				matchexpr = r"[Hh]oudini ?(\d+)(\.(\d))?(\.(\d+))?"
			elif system == 'Linux':
				matchexpr = r"hfs(\d+)(\.(\d))(\.(\d+))" #we want full versions, not links or shortcuts
			elif system == 'Darwin':
				matchexpr = r"[Hh]oudini ?(\d+)(\.(\d))(\.(\d+))"
			match = re.match(matchexpr, dir)
			if not match:
				continue
			cver = (int(match.group(1)), 0 if match.group(3) == "" else int(match.group(3)), 9999 if match.group(5) == "" else int(match.group(5)))
			if system == 'Windows' or system == 'Linux':
				houdinies[cver] = os.path.join(path, dir)
			elif system == 'Darwin':
				houdinies[cver] = os.path.join(path, dir, 'Frameworks', 'Houdini.framework', 'Version', "%s.%s.%s" % cver, 'Resources')

	return houdinies


def get_closest_version(ver: tuple = (), houdinies: Optional[List[tuple]] = None) -> tuple:  # TODO: optimize, this was done by me when i didnt know about tuple comparison
	if len(ver) == 0:
		ver = (9999, 0, 9999)
	elif len(ver) == 1:
		ver = (ver[0], 0, 9999)
	elif len(ver) == 2:
		if ver[1] < 10:
			ver = (ver[0], ver[1], 9999)
		else:
			ver = (ver[0], 0, ver[1])
	elif len(ver) > 3:
		raise ValueError("version must have max 3 components")
	# now ver has format (XX.X.XXX)

	if houdinies is None:
		houdinies = locateHoudinies()

	vers = houdinies.keys()
	if len(vers) == 0:
		raise RuntimeError("houdini not found!!")
	# elif(len(vers)==1):return houdinies[vers[0]]

	sortvers = [((abs(x[0] - ver[0]), abs(x[1] - ver[1]), abs(x[2] - ver[2])), x) for x in vers]

	sortvers.sort(key=lambda el: el[0][0])
	sortvers = [x for x in sortvers if x[0][0] == sortvers[0][0][0]]
	sortvers.sort(key=lambda el: el[0][1])
	sortvers = [x for x in sortvers if x[0][1] == sortvers[0][0][1]]
	sortvers.sort(key=lambda el: el[0][2])
	sortvers = [x for x in sortvers if x[0][2] == sortvers[0][0][2]]

	return sortvers[0][1]


def launcherCodeTemplate(verTuple, bin, envDict=None, extraAttribs=None, projectName='', configName=''):
	if not isinstance(verTuple, tuple):
		verTuple = tuple(verTuple)
	if not isinstance(bin,str):
		bin = str(bin)
	code =  "# The following code was generated automatically by the cgLauncher\n"
	code += "# https://github.com/pedohorse/cglauncher\n"
	code += "# ----------------------------------------------------------------\n\n"
	code += \
'''import os
import subprocess
import re
import platform
import time

'''
	code += inspect.getsource(locateHoudinies)
	code += inspect.getsource(get_closest_version)
	code += "\n\n"

	code += \
'''def launch():
	hous=locateHoudinies()
	binpath=os.path.join(os.path.join(hous[get_closest_version({0},hous)],'bin'),"{1}")
	arglist=[binpath]
'''.format(str(verTuple),bin)
	if extraAttribs is not None:
		code += '''\
	arglist+=list({0})
	print("Additional arguments are set to %s"%str(list({0})))
'''.format(extraAttribs)

	#set environment
	if envDict is not None:
		code += '''\
	print("Setting up environment variables...")
	envtokendict={ 'PWD':os.getcwd() }
'''
		for env in envDict:
			if env=='':
				continue
			code += '''\
	val = re.sub(r'\[(\S+)\]',lambda match:envtokendict[match.group(1)] if match.group(1) in envtokendict else '',"{1}")
	val = val.replace(';',os.pathsep)
	os.environ["{0}"] = val
	print("{0} is set to %s"%val)
'''.format(str(env),str(envDict[env]))
	code += '''\
	print("Environment setup is done!\\n")
'''
	code += '''\
	print("Launching: %s"%arglist[0])
	subprocess.Popen(arglist, stdin=None, stdout=None, stderr=None)
'''

	code += '''\

print("This launcher was automatically generated from project '{0}' configuration '{1}' by cgLauncher")
print("------------------------------------------------------------------------------------------")
try:
	launch()
	print("Launcher finished\\n\\nYou may close this window or it will close itself in 5 seconds")
	time.sleep(5)
except Exception as e:
	print("ERROR OCCURED!!!\\n%s\\n\\n"%e.message)
	raw_input("Press enter to close the window...")
'''.format(projectName,configName)
	return code


# # THIS IS NOT USED AND BROKEN THEREFORE HAVE TO BE EITHER FIXED OR DELETED, OR WHY NOT BOTH
# def launchHoudini(ver=(), hsite=None, job=None):
# 	os.environ["JOB"] = r"c:\temp"
# 	if (not (hsite is None) and isinstance(hsite, str)):
# 		os.environ["HSITE"] = hsite
# 		print("HSITE set to %s" % (str(hsite),))
# 	if (not (job is None) and isinstance(job, str)):
# 		os.environ["JOB"] = job
# 		print("JOB   set to %s" % (str(job),))
# 	os.environ["FPS"] = "25"
# 	houbin = locateHoudini(ver)
# 	print("Calling closest found version: %s" % (houbin,))
# 	subprocess.Popen(houbin, stdin=None, stdout=None, stderr=None)
# 	print("Done!")
