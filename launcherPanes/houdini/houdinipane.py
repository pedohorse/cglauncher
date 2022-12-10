import os
import subprocess

from PySide2.QtCore import QStandardPaths
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# import json
import re

from ..baselauncherpane import BaseLauncherPane
from . import houdini_ui
from . import houdini_rc

from .project import *
from . import houutils

from . import projectdialog

from pprint import pprint


class HoudiniConfig(QObject):
    # signals
    newVersionsDetected = Signal()  # TODO: add parameter with set of new versions

    def __init__(self, parent=None):
        super(HoudiniConfig, self).__init__(parent)
        self.__houdinies = {}
        self.rescan()

    def rescan(self):
        overs = set(self.__houdinies.keys())
        self.__houdinies = houutils.locateHoudinies()
        if set(self.__houdinies.keys()) != overs:
            self.newVersionsDetected.emit()

    def all_versions(self):
        return self.__houdinies

    def get_closest_version(self, ver=()):
        return houutils.get_closest_version(ver, self.all_versions())

    def get_closest_version_path(self, ver=()):
        return self.all_versions()[self.get_closest_version(ver)]


class HoudiniPane(BaseLauncherPane):
    attribParseRegex = r'([^\s"]+|"[^"]*")(?:\s|$)+'

    def __init__(self, parent=None):
        super(HoudiniPane, self).__init__(parent)
        self.__blockUICallbacks = False
        self.__projectPathChangedInProgress = False
        self.__project = None

        self.ui = houdini_ui.Ui_houdiniMenu()

        self.ui.setupUi(self)
        # extra background layout
        self.ui.bkgProjectLabel = QLabel("launcher", self)
        self.ui.bkgProjectLabel.setObjectName("bkgProjectLabel")
        self.ui.bkgProjectLabel.setStyleSheet('QLabel#bkgProjectLabel{font-size: 128px; color: rgb(64,64,64);}')
        self.ui.bkgProjectLabel.move(190, 180)
        # self.bkgProjectLabel.setAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.ui.bkgProjectLabel.adjustSize()
        self.ui.bkgProjectLabel.lower()

        self.__sceneFileModel = QFileSystemModel(self)
        self.__sceneFileModel.setNameFilters(["*.hip", "*.hipnc"])
        # self.__sceneFileModel.setFilter(QDir.Files | QDir.Dirs | QDir.NoDotAndDotDot)
        self.__sceneFileModel.setNameFilterDisables(False)
        self.ui.sceneFilesTreeView.doubleClicked.connect(self.scene_file_tree_double_clicked)

        # self.ui.envTableView.setModel(EnvTableModel())
        # self.ui.envTableView.verticalHeader().setMovable(True)
        # self.ui.envTableView.horizontalHeader().setStretchLastSection(True)
        # self.ui.envTableView.verticalHeader().setStretchLastSection(False)

        self.__projectDialog = projectdialog.ProjectDialog('houdini', self)
        self.__projectDialog.accepted.connect(self.project_dialog_selected)

        self.__houconf = HoudiniConfig()
        self.ui.houVersionComboBox.clear()
        for ver in self.__houconf.all_versions().keys():
            self.ui.houVersionComboBox.addItem('.'.join((str(x) for x in ver)), ver)

        # for default project add default config
        # there should be no name collisions, cuz we r adding to the empty default project
        if len(self.__houconf.all_versions()) == 0:
            # houdini not found
            self.setEnabled(False)
            return

        # setup signals
        self.ui.configComboBox.currentIndexChanged[str].connect(self.config_selected)
        self.ui.houVersionComboBox.currentIndexChanged[int].connect(self.ui_hou_ver_changed)
        self.ui.binNameComboBox.editTextChanged.connect(self.binary_changed)
        self.ui.commandLineArgsLineEdit.editingFinished.connect(self.arguments_changed)
        self.ui.newConfigPushButton.clicked.connect(self.new_config_button_pressed)
        self.ui.renameConfigPushButton.clicked.connect(self.rename_config_button_pressed)
        self.ui.delConfigPushButton.clicked.connect(self.config_remove_button_clicked)
        self.ui.launchPushButton.clicked.connect(self.launch_button_clicked)
        self.ui.launchPushButton.customContextMenuRequested.connect(self.launch_button_right_clicked)
        self.ui.launchOptionsPushButton.clicked.connect(self.launcher_options_button_clicked)

        self.ui.projectPathLine.editingFinished.connect(self.project_path_changed)
        self.ui.saveProjectPushButton.clicked.connect(self.save_project_button_clicked)

        self.ui.projectPathPushButton.clicked.connect(self.select_project_clicked)

        # set default project
        self.__settingspath = QStandardPaths.writableLocation(QStandardPaths.DataLocation)
        defProject = Project(os.path.join(self.__settingspath, 'default.project'))  # TODO: he's not deleted when project's changed, and yet we dont keep a ref to it
        if len(defProject.configs()) == 0:
            defProject.add_config(ProjectConfig('default', self.__houconf.get_closest_version()))
            defProject.sync()
        self.set_project(defProject)

    def set_project(self, project):
        # disconnect old project
        print("\n\n-----------------\n--NEW-PROJECT----\n-----------------")
        if self.__project is not None:
            try:
                self.__project.config_added.disconnect(self.config_added)  #
                self.__project.config_removed.disconnect(self.config_removed)  #
                self.__project.project_file_path_changed.disconnect(self.update_tree_view)
            # TODO: The comment below was aboout python2 and PySide qt4, so figure out what i meant back then and if it is still relevant
            # TOTO:figure out why disconnect sometimes doesnt work
            # I think i figured out, but now i dont remember what was that
            # as i recall - something with pyqt signal-slots actually only supporting limited subset of only default types, so if you Slot from your type - it won't find that slot after
            except Exception as e:
                print("Pane: strange error during disconnecting: %s" % str(e))
        # self.__project.deleteLater()
        self.set_config(None)
        self.__project = project

        self.ui.configComboBox.clear()
        self.ui.sceneFilesTreeView.setModel(None)
        if self.__project is not None:
            self.ui.configComboBox.addItems([conf for conf in self.__project.configs()])

            self.__project.config_added.connect(self.config_added)
            self.__project.config_removed.connect(self.config_removed)
            self.__project.project_file_path_changed.connect(self.update_tree_view)
            # now set some ui #TODO: in some cases during new project's creation set_project may be not called, but this shit has to be updated still. DO
            self.update_tree_view()

    def update_tree_view(self, dirname=None):
        if dirname is None:
            if self.__project is None:
                raise RuntimeError("Tree view cannot be updated - cuz there's no project")
            dirname = os.path.dirname(self.__project.file_path())
        else:
            if not os.path.isdir(dirname):
                dirname = os.path.dirname(os.path.normpath(dirname))

        self.ui.bkgProjectLabel.setText(os.path.basename(os.path.normpath(dirname)))
        self.ui.bkgProjectLabel.adjustSize()
        index = self.__sceneFileModel.setRootPath(dirname)
        self.ui.sceneFilesTreeView.setModel(self.__sceneFileModel)
        self.ui.sceneFilesTreeView.setRootIndex(index)
        self.ui.sceneFilesTreeView.setColumnHidden(2, True)
        self.ui.sceneFilesTreeView.setColumnWidth(0, 256)
        self.ui.sceneFilesTreeView.setColumnWidth(1, 64)

    def set_config(self, config):  # all UI is driven by model callbacks after config is set
        '''
        set UI to show config
        :param config: ProjectConfig or None
        :return:
        '''
        oldState = self.__blockUICallbacks
        self.__blockUICallbacks = True
        try:
            # setting down
            oldconfig = self.ui.envTableView.model()
            if oldconfig is not None:
                oldconfig.otherDataChanged.disconnect(self.other_data_from_config)

            self.ui.envTableView.setModel(None)
            # setting up
            if config is not None:
                config.otherDataChanged.connect(self.other_data_from_config)
                self.other_data_from_config(config.allOtherData())

                self.ui.envTableView.setModel(config)
        except Exception as e:
            print("shit happened: %s = %s" % (str(type(e)), str(e.message)))
        finally:
            self.__blockUICallbacks = oldState

    # UI callbacks

    def launch(self, extraattribs=None):
        conf = self.__project.config(self.ui.configComboBox.currentText())
        if conf is None:
            print("failed to obtain config")
            return

        filepath = self.__houconf.get_closest_version_path(conf.houVer())
        binname = self.ui.binNameComboBox.currentText()
        filename = None
        try:
            filenamecandidates = [x for x in os.listdir(os.path.join(filepath, 'bin')) if os.path.splitext(x)[0] == binname]
            if (len(filenamecandidates) == 0):
                raise RuntimeError('no binary found')
            elif (len(filenamecandidates) > 1):
                raise RuntimeError('multiple matching files to launch found')
            filename = filenamecandidates[0]
        except Exception as e:
            print("HoudiniPane: launch failed: {}".format(str(e)))
            return
        filepath = os.path.join(filepath, 'bin', filename)
        # now set env
        env = os.environ.copy()
        envtokendict = {};
        envtokendict = os.environ.copy();
        envtokendict.update({'PWD': os.path.dirname(self.__project.file_path())})
        for i in range(conf.rowCount() - 1):
            name = conf.data(conf.index(i, 0))
            val = conf.data(conf.index(i, 1))
            # now replace ; with current os's pathseparator
            val = val.replace(';', os.pathsep)
            if (name == ''): continue
            val = re.sub(r'\$\{(\S+)\}|\$(\w+)', lambda match: envtokendict.get(match.group(1) or match.group(2), ''), val)
            env[str(name)] = str(val)  # just so no unicode
            envtokendict[str(name)] = str(val)
        print(filepath)
        pprint(env)
        basedir = os.path.dirname(filepath)

        # attributes
        attribs = self.ui.commandLineArgsLineEdit.text()
        if attribs != '':
            attrlist = re.findall(HoudiniPane.attribParseRegex, attribs)
            if (isinstance(filepath, str)): filepath = [filepath]
            filepath += attrlist

        if extraattribs is not None:
            assert isinstance(extraattribs, tuple) or isinstance(extraattribs, list), 'extra attributes must be either list or tuple'
            if (isinstance(filepath, str)): filepath = [filepath]
            filepath += list(extraattribs)
        print(filepath)
        subprocess.Popen(filepath, stdin=None, stdout=None, stderr=None, env=env, cwd=basedir)

    @Slot()
    def scene_file_tree_double_clicked(self, index):
        try:
            filepath = self.__sceneFileModel.filePath(index)
        except Exception:
            print("internal error")
            return
        self.launch([filepath])

    @Slot()
    def launch_button_clicked(self):
        self.launch()

    @Slot(bool)
    def launcher_options_button_clicked(self):
        sender = self.sender()
        pos = sender.parent().mapToGlobal(sender.geometry().bottomLeft())
        self.create_launch_options_menu(pos)

    @Slot()
    def launch_button_right_clicked(self, pos=None):
        self.create_launch_options_menu(self.sender().mapToGlobal(pos))

    def create_launch_options_menu(self, globalPos):
        menu = QMenu("what to do", self)
        action = menu.addAction("create a launcher script for current config")
        action.setData([0, None])
        menu.triggered.connect(self.launch_menu_triggered)
        menu.popup(globalPos)
        menu.aboutToHide.connect(menu.deleteLater)

    @Slot()
    def launch_menu_triggered(self, action):
        actionid = action.data()[0]
        if actionid == 0:
            if self.__project is None or self.__project.file_path() is None:
                QMessageBox.warning(self, "error", "failed to create launcher script\nfailed to obtain project's file location")
                return
            conf = self.__project.config(self.ui.configComboBox.currentText())
            if conf is None:
                QMessageBox.warning(self, "error", "failed to create launcher script\nfailed to obtain configuration")
                return

            env = {}
            for i in range(conf.rowCount() - 1):
                env[conf.data(conf.index(i, 0))] = conf.data(conf.index(i, 1))

            attribs = self.ui.commandLineArgsLineEdit.text()
            attrlist = None
            if attribs != '':
                attrlist = re.findall(HoudiniPane.attribParseRegex, attribs)
            code = houutils.launcherCodeTemplate(conf.houVer(), conf.otherData('binary'), env, attrlist, os.path.basename(os.path.normpath(os.path.dirname(self.__project.file_path()))), conf.name())
            with open(os.path.join(os.path.dirname(self.__project.file_path()), 'launcher.py'), 'w') as f:
                f.write(code)
            QMessageBox.information(self, "Success", "launcher.py was created in the project's folder")

    @Slot()
    def project_dialog_selected(self):
        self.ui.projectPathLine.setText(self.__projectDialog.chosenPath())
        self.project_path_changed()

    # Model-to-UI callbacks
    @Slot(object)
    def other_data_from_config(self, dictdata):
        self.__blockUICallbacks = True
        # if u want any UI-to-model callbacks to happen - think twice and modify model directly
        try:
            keys = dictdata.keys()
            if 'version' in keys:
                data = dictdata['version']
                # houfound = False
                closestversion = houutils.get_closest_version(data)
                closestversion_text = '.'.join(str(x) for x in closestversion)
                vid = self.ui.houVersionComboBox.findText(closestversion_text)
                if vid == -1:
                    print('somehow version list is incomplete, adding')
                    self.ui.houVersionComboBox.addItem(closestversion_text)
                    vid = self.ui.houVersionComboBox.count() - 1
                self.ui.houVersionComboBox.setCurrentIndex(vid)
            # if (not houfound): return
            if 'binary' in keys:
                data = dictdata['binary']
                self.ui.binNameComboBox.setEditText(data)
            if 'name' in keys:
                data = dictdata['name']
                self.ui.configComboBox.setItemText(self.ui.configComboBox.currentIndex(), data)
            if 'args' in keys:
                data = dictdata['args']
                self.ui.commandLineArgsLineEdit.setText(data)
        finally:
            self.__blockUICallbacks = False

    @Slot()
    def config_added(self, config):
        self.ui.configComboBox.addItem(config.name())
        self.ui.configComboBox.setCurrentIndex(self.ui.configComboBox.count() - 1)

    @Slot(str)
    def config_removed(self, confName):
        id = self.ui.configComboBox.findText(confName)
        if id < 0:
            return
        self.ui.configComboBox.removeItem(id)

    #####UI-to-model callbacks
    @Slot(str)
    def config_selected(self, text):
        if self.__blockUICallbacks:
            return
        self.set_config(self.__project.config(text))

    @Slot()
    def project_path_changed(self):
        """
        :param value:
        :return:
        """
        if self.__projectPathChangedInProgress:
            return
        self.__projectPathChangedInProgress = True
        try:
            value = self.ui.projectPathLine.text()
            self.ui.projectPathLine.clearFocus()
            gooddir = os.path.isdir(value) and os.path.exists(value)
            self.ui.saveProjectPushButton.setEnabled(gooddir or value == '')
            if gooddir:
                if self.__project.sync_needed():
                    button = QMessageBox.question(self, 'unsaved changes', 'what to do?', buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                    if button == QMessageBox.Save:
                        self.__project.sync()
                    elif button == QMessageBox.Cancel:
                        self.ui.projectPathLine.setText(os.path.dirname(self.__project.file_path()))
                        return

                projectfile = os.path.join(value, 'houdini.project')
                if os.path.isfile(projectfile):
                    self.set_project(Project(projectfile))
                else:
                    button = QMessageBox.question(self, 'no project found', 'copy current project in this location?', buttons=QMessageBox.Yes | QMessageBox.RestoreDefaults | QMessageBox.Cancel)
                    if button == QMessageBox.Yes:
                        self.__project.set_file_path(projectfile)
                        self.__project.sync()
                    elif button == QMessageBox.RestoreDefaults:
                        newproj = Project(os.path.join(self.__settingspath, 'default.project'))
                        newproj.set_file_path(projectfile)
                        self.set_project(newproj)
                    else:
                        self.ui.projectPathLine.setText(os.path.dirname(self.__project.file_path()))
                        return
            elif value == '':
                self.set_project(Project(os.path.join(self.__settingspath, 'default.project')))
            else:
                self.ui.projectPathLine.setText(os.path.dirname(self.__project.file_path()))
                return
        finally:
            self.__projectPathChangedInProgress = False

    @Slot(int)
    def ui_hou_ver_changed(self, id):
        # TODO: Think of some more robust way to get current config. What if say change config sigal is and this one are connected with QueuedConnection? then it's possible we first change the config and then apply these changes to the new config, not old one
        if self.__blockUICallbacks:
            return
        conf = self.__project.config(self.ui.configComboBox.currentText())
        conf.setOtherData('version', tuple(self.ui.houVersionComboBox.itemData(id)))

    @Slot(str)
    def binary_changed(self, text):
        if self.__blockUICallbacks:
            return
        conf = self.__project.config(self.ui.configComboBox.currentText())
        conf.setOtherData('binary', text)

    @Slot()
    def arguments_changed(self):
        if self.__blockUICallbacks:
            return
        conf = self.__project.config(self.ui.configComboBox.currentText())
        conf.setOtherData('args', self.ui.commandLineArgsLineEdit.text())

    #	# Buttons Callbacks
    @Slot()
    def select_project_clicked(self):
        self.__projectDialog.move(QCursor.pos())
        self.__projectDialog.show()

    @Slot()
    def new_config_button_pressed(self):
        if self.__blockUICallbacks:
            return
        name, good = QInputDialog.getText(self, 'new config', 'enter unique name')
        if not good:
            return
        self.__project.add_config(ProjectConfig(name, tuple(self.ui.houVersionComboBox.itemData(self.ui.houVersionComboBox.currentIndex()))))

    @Slot()
    def rename_config_button_pressed(self):
        if self.__blockUICallbacks:
            return
        if self.ui.configComboBox.count() == 0:
            return
        oldname = self.ui.configComboBox.currentText()
        newname, good = QInputDialog.getText(self, 'new config', 'enter unique name', text=oldname)
        if not good:
            return
        self.__project.config(oldname).rename(self.__project.make_unique_config_name(newname))

    @Slot()
    def config_remove_button_clicked(self):
        if self.__blockUICallbacks:
            return
        if self.ui.configComboBox.count() == 0:
            return
        # TODO: add popup
        self.__project.remove_config(self.ui.configComboBox.currentText())

    @Slot()
    def save_project_button_clicked(self):
        if self.__project is None:
            return
        self.__project.sync()

    ##### PANE IMPLEMENTATION
    def pane_header(self):
        return 'Houdini', ':/icons/houdini/houlogo.png'
