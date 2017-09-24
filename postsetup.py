import os
import zipfile


def zipfolder(filename,resulZipName='res.zip'):
	filename=os.path.normpath(filename)
	basedir=os.path.dirname(filename)
	zf=zipfile.ZipFile(os.path.join(basedir,resulZipName),'w',zipfile.ZIP_DEFLATED)

	zipstuff(zf,filename)
	zf.close()

def zipstuff(zf,filepath,basezippath=''):
	#print('zipping %s'%filepath)
	if(os.path.isfile(filepath)):
		zf.write(filepath,'/'.join((basezippath,os.path.basename(filepath))))
	elif(os.path.isdir(filepath)):
		for fn in os.listdir(filepath):
			zipstuff(zf,os.path.join(filepath,fn),'/'.join((basezippath,os.path.basename(filepath))))



def executePostinstallScript():
	cwd=os.getcwd()
	distFolder=os.path.join(cwd,'dist')

	print('making a zip distribution...')
	zipfolder(os.path.join(distFolder,'cglauncher'),'cglauncher.zip')
	print('done!')


if(__name__=='__main__'):
	executePostinstallScript()


