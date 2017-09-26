c:\\python27\\python.exe C:\\Python27\\Scripts\\cxfreeze --include-modules=json --target-dir=dist\\cglauncher --icon=icon.ico --base-name=WIN32GUI --target-name=cglauncher.exe main.py
xcopy launcherPanes dist\cglauncher\launcherPanes /E /Y
c:\\python27\\python.exe postsetup.py