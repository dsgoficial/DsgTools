# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-04-04
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
#General imports
import zipfile, shutil, os, json

from DsgTools.Utils.utils import Utils

#PyQt4 imports
from PyQt4.Qt import QObject
from PyQt4.QtGui import QMessageBox

class DsgToolsOpInstaller(QObject):
    def __init__(self, iface, parent=None, parentMenu=None):
        """
        Constructor
        """
        super(DsgToolsOpInstaller,self).__init__()
        self.iface = iface
        self.parentMenu = parentMenu
        self.utils = Utils()
        self.parent = parent
        self.icon_path = ':/plugins/DsgTools/icons/militarySimbology.png'
        # QAction list created when installing
        self.toolList = []
    
    def createAuxFolder(self):
        """
        Creates a auxiliary foldes to unzip the installer zip file
        """
        # current path point to DsgToolsOp folder
        currentPath = os.path.abspath(os.path.dirname(__file__))
        # folder "auxiliar" inside DsgToolsOp folder
        auxFolder = os.path.join(currentPath, 'auxiliar')
        # creating and returning the folder
        os.makedirs(auxFolder)
        return auxFolder
    
    def deleteAuxFolder(self):
        """
        Deletes the auxiliar folder created by createAuxFolder method
        """
        currentPath = os.path.abspath(os.path.dirname(__file__))
        top = os.path.join(currentPath, 'auxiliar')
        shutil.rmtree(top, ignore_errors=True)
    
    def uninstallDsgToolsOp(self):
        """
        Uninstall all folders and files created
        """
        # removing the actions previously created by the installer
        self.removeMenus()

        parentUi = self.iface.mainWindow()
        if QMessageBox.question(parentUi, self.tr('Question'), self.tr('DsgToolsOp is going to be uninstalled. Would you like to continue?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return

        # current path point to DsgToolsOp folder
        currentPath = os.path.abspath(os.path.dirname(__file__))
        # working on MilitaryTools folder
        toolsPath = os.path.join(currentPath,'MilitaryTools')
        for root, dirs, files in os.walk(toolsPath):
            # deleting directories from MilitaryTools folder
            for dir_ in dirs:
                top = os.path.join(currentPath, 'MilitaryTools', dir_)
                shutil.rmtree(top, ignore_errors=True)
            # deleting files (keeping __init__.py) files MilitaryTools folder
            for file_ in files:    
                if file_ != '__init__.py':
                    os.remove(os.path.join(toolsPath, file_))

        QMessageBox.information(parentUi, self.tr('Success!'), self.tr('DsgToolsOp uninstalled successfully!'))
    
    def removeMenus(self):
        """
        Removes created menus
        """
        for tupple_ in self.toolList:
            text = tupple_[0]
            action = tupple_[1]
            self.iface.removePluginMenu(text, action)
        self.toolList = []

    def installDsgToolsOp(self, fullZipPath, parentUi=None):
        """
        Install files present into installer zip file
        :param fullZipPath: zip file path
        """
        try:
            reinstalled = False
            # current path point to DsgToolsOp folder
            currentPath = os.path.abspath(os.path.dirname(__file__))
            # creating auxiliar folder
            auxFolder = self.createAuxFolder()
            destFolder = os.path.join(currentPath, 'MilitaryTools')
            # unzipping files into Military tools
            self.unzipFiles(fullZipPath, auxFolder)
            # check if installed
            if self.checkIfInstalled():
                # if installed, get the version
                installedVersion = self.getInstalledVersion()
                # getting the version to be installed
                toBeInstalledVersion = self.getFilesVersion(auxFolder)
                # checks if the version to be installed is already installed
                if installedVersion == toBeInstalledVersion:
                    QMessageBox.warning(parentUi, self.tr('Warning!'), self.tr('DsgToolsOp version already installed!'))
                    self.deleteAuxFolder()
                    return
                # Checks if the version to be installed is lower
                if installedVersion > toBeInstalledVersion:
                    if QMessageBox.question(parentUi, self.tr('Question'), self.tr('Selected version is lower than installed one. Would you like to continue?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                        self.deleteAuxFolder()
                        return
                # deleting previous version files
                self.uninstallDsgToolsOp()
                reinstalled = True
            # copying files to destination folder
            self.copyFiles(auxFolder, destFolder)
            QMessageBox.information(parentUi, self.tr('Success!'), self.tr('DsgToolsOp installed successfully!'))
            if reinstalled:
                QMessageBox.warning(parentUi, self.tr('Warning!'), self.tr('Please, reload QGIS to access the new installed version!'))
        except Exception as e:
            try:
                self.deleteAuxFolder()
            except:
                pass
            QMessageBox.critical(self.parentMenu, self.tr('Critical!'), self.tr('Problem installing DsgToolsOp: ') + '|'.join(e.args))
    
    def addUninstall(self, icon_path, parent, parentMenu):
        """
        Creates the uninstall action menu
        """
        uninstallText = parent.tr('DsgTools Op Uninstaller')
        action = parent.add_action(
            icon_path,
            text=uninstallText,
            callback=parent.uninstallDsgToolsOp,
            parent=parentMenu,
            add_to_menu=False,
            add_to_toolbar=False)
        parentMenu.addAction(action)
        return uninstallText, action
    
    def unzipFiles(self, fullZipPath, auxFolder):
        """
        Unzips files inside a zip into a folder
        :param fullZipPath: zip file path
        :param auxFolder: unzip folder
        """
        zip = zipfile.ZipFile(fullZipPath)
        zip.extractall(auxFolder)

    def copyFiles(self, auxFolder, destFolder):
        """
        Copies all files to destination folder
        :param destFolder: destination folder
        :param auxFolder: source folder
        """
        for src_dir, dirs, files in os.walk(auxFolder):
            dst_dir = src_dir.replace(auxFolder, destFolder, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.move(src_file, dst_dir)
        # deleting auxiliar folder
        self.deleteAuxFolder()
        self.loadTools()
    
    def checkIfInstalled(self):
        """
        Checks if the files are already installed
        """
        installPath = os.path.join(os.path.abspath(os.path.dirname(__file__)),'MilitaryTools')
        w = os.walk(installPath).next()[2]
        # checking the number of files in the folder
        if len(w)<=2:
            return False
        else:
            return True
    
    def getInstalledVersion(self):
        """
        Checks the current installed version
        """
        versionPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MilitaryTools', 'dsgtoolsop_version.json')
        jsonDict = self.utils.readJsonFile(versionPath)
        return jsonDict['version']
    
    def getFilesVersion(self, filesFolder):
        """
        Gets the version to be installed
        """
        versionPath = os.path.join(filesFolder, 'dsgtoolsop_version.json')
        jsonDict = self.utils.readJsonFile(versionPath)
        return jsonDict['version']
    
    def loadTools(self):
        """
        Loads the tools present in the installer zip file
        """
        try:
            self.toolList = []
            from DsgTools.DsgToolsOp.MilitaryTools.toolLoader import ToolLoader
            self.toolLoader = ToolLoader(self.parentMenu, self.parent, self.icon_path)
            toolText, toolAction = self.toolLoader.loadTools()
            uninstallText, uninstallAction = self.addUninstall(self.icon_path, self.parent, self.parentMenu)
            self.toolList.append((toolText, toolAction))
            self.toolList.append((uninstallText, uninstallAction))
        except Exception as e:
            QMessageBox.critical(self.parentMenu, self.tr('Critical!'), self.tr('Problem installing DsgToolsOp: ') + '|'.join(e.args))