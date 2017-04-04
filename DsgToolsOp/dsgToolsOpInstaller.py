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
import codecs, os, json, binascii

#PyQt4 imports
from PyQt4.Qt import QObject

class DsgToolsOpInstaller:
    def __init__(self):
        pass
    
    def copyFiles(self):
        pass
    
    def checkIfInstalled(self):
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
            raise self.tr('DsgToolsOp not installed!')
    