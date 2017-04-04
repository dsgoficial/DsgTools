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

#PyQt4 imports
from PyQt4.Qt import QObject

class DsgToolsOpInstaller(QObject):
    def __init__(self):
        super(DsgToolsOpInstaller,self).__init__()
    
    def createAuxFolder(self):
        currentPath = os.path.dirname(__file__)
        auxFolder = os.path.join(currentPath, 'aux')
        os.makedirs(auxFolder)
        return auxFolder
    
    def deleteAuxFolder(self):
        currentPath = os.path.dirname(__file__)
        top = os.path.join(currentPath, 'aux')
        shutil.rmtree(top, ignore_errors=False)

    def installDsgToolsOp(self, fullZipPath):
        try:
            currentPath = os.path.dirname(__file__)
            auxFolder = self.createAuxFolder()
            destFolder = os.path.join(currentPath, 'MilitaryTools')
            zip = zipfile.ZipFile(fullZipPath)
            zip.extractall(auxFolder)
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

        except Exception as e:
            try:
                self.deleteAuxFolder()
            except:
                pass
            raise e
    
    def checkIfInstalled(self):
        installPath = os.path.join(os.path.dirname(__file__),'MilitaryTools')
        w = os.walk(installPath).next()[2]
        if len(w)<=2:
            return False
        else:
            return True
    
    def checkInstalledVersion(self):
        pass
    
    def checkFilesVersion(self, filesFolder):
        pass
    
    def loadTools(self, parentMenu, parent, icon_path):
        try:
            from DsgTools.DsgToolsOp.MilitaryTools.toolLoader import ToolLoader
            self.toolLoader = ToolLoader(parentMenu, parent, icon_path)
            self.toolLoader.loadTools()
        except:
            raise Exception(self.tr('DsgToolsOp not installed!'))

if __name__ == '__main__':
    fullZipPath = '/home/borba/MilitarySimbologyTools.zip'
    dsgToolsOpInstaller = DsgToolsOpInstaller()
    print 'initial state'
    print dsgToolsOpInstaller.checkIfInstalled()
    dsgToolsOpInstaller.installDsgToolsOp(fullZipPath)
    print 'final state'
    print dsgToolsOpInstaller.checkIfInstalled()