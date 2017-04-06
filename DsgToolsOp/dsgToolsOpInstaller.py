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
from osgeo import ogr
from uuid import uuid4
import zipfile, shutil
import codecs, os, json, binascii

from DsgTools.Utils.utils import Utils

#PyQt4 imports
from PyQt4.Qt import QObject
from PyQt4.QtGui import QMessageBox

class DsgToolsOpInstaller(QObject):
    def __init__(self, parent = None, parentMenu = None):
        super(DsgToolsOpInstaller,self).__init__()
        self.parentMenu = parentMenu
        self.utils = Utils()
        self.parent = parent
        self.icon_path = ':/plugins/DsgTools/icons/militarySimbology.png'
        self.toolList = []
    
    def createAuxFolder(self):
        currentPath = os.path.dirname(__file__)
        auxFolder = os.path.join(currentPath, 'aux')
        os.makedirs(auxFolder)
        return auxFolder
    
    def deleteAuxFolder(self):
        currentPath = os.path.dirname(__file__)
        top = os.path.join(currentPath, 'aux')
        shutil.rmtree(top, ignore_errors=True)
    
    def uninstallDsgToolsOp(self, iface):
        parentUi = iface.mainWindow()
        if QMessageBox.question(parentUi, self.tr('Question'), self.tr('DsgToolsOp is going to be uninstalled. Would you like to continue?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        currentPath = os.path.dirname(__file__)
        toolsPath = os.path.join(currentPath,'MilitaryTools')
        for name in os.listdir(toolsPath):
            top = os.path.join(currentPath, 'MilitaryTools', name)
            shutil.rmtree(top, ignore_errors=True)
        for filename in os.walk(toolsPath).next()[2]:
            if '__init__' not in filename:
                os.remove(os.path.join(toolsPath, filename))
        self.removeMenus(iface)
        QMessageBox.warning(parentUi, self.tr('Success!'), self.tr('DsgToolsOp uninstalled successfully!'))
    
    def removeMenus(self, iface):
        for item in self.toolList:
            iface.removePluginMenu(item)
        self.toolList = []

    def installDsgToolsOp(self, fullZipPath, parentUi = None):
        try:
            currentPath = os.path.dirname(__file__)
            auxFolder = self.createAuxFolder()
            destFolder = os.path.join(currentPath, 'MilitaryTools')
            self.unzipFiles(fullZipPath, auxFolder)
            if self.checkIfInstalled():
                installedVersion = self.getInstalledVersion()
                toBeInstalledVersion = self.getFilesVersion(auxFolder)
                if installedVersion == toBeInstalledVersion:
                    QMessageBox.warning(parentUi, self.tr('Warning!'), self.tr('DsgToolsOp version already installed!'))
                    return
                if installedVersion > toBeInstalledVersion:
                    if QMessageBox.question(parentUi, self.tr('Question'), self.tr('Selected version is lower than installed one. Would you like to continue?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                        QMessageBox.warning(parentUi, self.tr('Warning!'), self.tr('DsgToolsOp not installed!'))
                        self.deleteAuxFolder()
                        return
            self.copyFiles(auxFolder,destFolder)
            self.deleteAuxFolder()
            QMessageBox.warning(parentUi, self.tr('Success!'), self.tr('DsgToolsOp installed successfully!'))

        except Exception as e:
            try:
                self.deleteAuxFolder()
            except:
                pass
            raise e
    
    def addUninstall(self, icon_path, parent, parentMenu):
        action = self.add_action(
            icon_path,
            text=self.tr('DsgTools Op Uninstaller'),
            callback=parent.uninstallDsgToolsOp,
            parent=parentMenu,
            add_to_menu=False,
            add_to_toolbar=False)
        parentMenu.addAction(action)
        return action
    
    def unzipFiles(self, fullZipPath, auxFolder):
        zip = zipfile.ZipFile(fullZipPath)
        zip.extractall(auxFolder)

    def copyFiles(self, auxFolder, destFolder):
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
        self.deleteAuxFolder()
        self.toolList = self.loadTools()
    
    def checkIfInstalled(self):
        installPath = os.path.join(os.path.dirname(__file__),'MilitaryTools')
        w = os.walk(installPath).next()[2]
        if len(w)<=2:
            return False
        else:
            return True
    
    def getInstalledVersion(self):
        versionPath = os.path.join(os.path.dirname(__file__), 'MilitaryTools', 'dsgtoolsop_version.json')
        jsonDict = self.utils.readJsonFile(versionPath)
        return jsonDict['version']
    
    def getFilesVersion(self, filesFolder):
        versionPath = os.path.join(filesFolder, 'dsgtoolsop_version.json')
        jsonDict = self.utils.readJsonFile(versionPath)
        return jsonDict['version']
    
    def loadTools(self):
        try:
            from DsgTools.DsgToolsOp.MilitaryTools.toolLoader import ToolLoader
            self.toolLoader = ToolLoader(self.parentMenu, self.parent, self.icon_path)
            toolList = self.toolLoader.loadTools()
            uninstallAction = self.addUninstall(self.icon_path, self.parent, self.parentMenu)
            toolList.append(uninstallAction)
            return toolList

        except:
            raise Exception(self.tr('DsgToolsOp not installed!'))