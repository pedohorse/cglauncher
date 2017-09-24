import os
import subprocess
import re


def locateHoudinies(extraPathList=None):
	commonpaths = [r"C:\Program Files\Side Effects Software",r"/opt",r"/Applications"]
	if(extraPathList is not None):commonpaths+=extraPathList

	houdinies = {}
	for path in commonpaths:
		dirs = []
		try:
			dirs = os.listdir(path)
		except:
			continue

		for dir in dirs:
			match = re.match(r"[Hh]oudini ?(\d+)(\.(\d))?(\.(\d{3,}))?", dir)
			if (not match): continue
			cver = (int(match.group(1)), 0 if match.group(3) == "" else int(match.group(3)), 9999 if match.group(5) == "" else int(match.group(5)))
			houdinies[cver] = os.path.join(path, dir)

	return houdinies


def getClosestVersion(ver=(),houdinies=None):
	if (len(ver) == 0):
		ver = (9999, 0, 9999)
	elif (len(ver) == 1):
		ver = (ver[0], 0, 9999)
	elif (len(ver) == 2):
		if (ver[1] < 10):
			ver = (ver[0], ver[1], 9999)
		else:
			ver = (ver[0], 0, ver[1])
	elif (len(ver) > 3):
		raise ValueError("version must have max 3 components")
	# now ver has format (XX.X.XXX)

	if(houdinies is None):houdinies=locateHoudinies()

	vers = houdinies.keys()
	if (len(vers) == 0): raise RuntimeError("houdini not found!!")
	# elif(len(vers)==1):return houdinies[vers[0]]

	sortvers = [((abs(x[0] - ver[0]), abs(x[1] - ver[1]), abs(x[2] - ver[2])), x) for x in vers]

	sortvers.sort(key=lambda el: el[0][0])
	sortvers = [x for x in sortvers if x[0][0] == sortvers[0][0][0]]
	sortvers.sort(key=lambda el: el[0][1])
	sortvers = [x for x in sortvers if x[0][1] == sortvers[0][0][1]]
	sortvers.sort(key=lambda el: el[0][2])
	sortvers = [x for x in sortvers if x[0][2] == sortvers[0][0][2]]


	return sortvers[0][1]


def launchHoudini(ver=(), hsite=None, job=None):
	os.environ["JOB"] = r"c:\temp"
	if (not (hsite is None) and isinstance(hsite, str)):
		os.environ["HSITE"] = hsite
		print("HSITE set to %s" % (str(hsite),))
	if (not (job is None) and isinstance(job, str)):
		os.environ["JOB"] = job
		print("JOB   set to %s" % (str(job),))
	os.environ["FPS"] = "25"
	houbin = locateHoudini(ver)
	print("Calling closest found version: %s" % (houbin,))
	subprocess.Popen(houbin, stdin=None, stdout=None, stderr=None)
	print("Done!")
