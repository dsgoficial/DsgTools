# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
import os

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.Qt import QObject

# QGIS imports
from qgis.core import QgsVectorLayer,QgsDataSourceURI, QgsMessageLog
from qgis.utils import iface

#DsgTools imports
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb

class EDGVLayer(QObject):
    qmlLoaded = pyqtSignal()
    
    def __init__(self, abstractDb, codeList):
        """Constructor."""
        super(EDGVLayer, self).__init__()
        
        self.abstractDb = abstractDb
        self.codeList = codeList
        self.uri = QgsDataSourceURI()
        self.qmlLoaded.connect(self.codeList.setState)        
        
    def load(self, crs, idSubgrupo = None):
        return None

    def loadDomainTable(self,name):
        pass
    
    def getStyles(self):
        '''
        The first iteration of walk lists all dirs as the second element of the list in os.walk(styleDir).next()[1]. 
        As only God and Mauricio were going to remember this, I wrote it down.
        '''
        styleDir = self.abstractDb.getStyleDir()
        return os.walk(styleDir).next()[1]
    
    def prepareLoad(self):
        dbName = self.abstractDb.getDatabaseName()
        groupList =  iface.legendInterface().groups()
        if dbName in groupList:
            return groupList.index(dbName)
        else:
            parentTreeNode = iface.legendInterface().addGroup(self.abstractDb.getDatabaseName(), -1)
            return parentTreeNode
    