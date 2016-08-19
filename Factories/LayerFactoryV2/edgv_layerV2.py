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
from xml.dom.minidom import parse, parseString

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant
from PyQt4.Qt import QObject

# QGIS imports
from qgis.core import QgsVectorLayer,QgsDataSourceURI, QgsMessageLog, QgsField, QGis
from qgis.utils import iface

#DsgTools imports
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.Utils.utils import Utils


class EDGVLayerV2(QObject):
    
    def __init__(self, iface, abstractDb):
        """Constructor."""
        super(EDGVLayerV2, self).__init__()
        
        self.abstractDb = abstractDb
        self.uri = QgsDataSourceURI() 
        self.iface = iface
        self.utils = Utils()    
        
    def load(self, crs, idSubgrupo = None):
        return None

    def loadDomainTable(self,name):
        pass
    
    def getStyle(self, stylePath, className):
        if 'db:' in stylePath:
            return self.abstractDb.getStyle(stylePath.split(':')[-1], className)
        else:
            return self.getStyleFromFile(stylePath, className)
    
    def getStyleFromFile(self, stylePath, className):
        availableStyles = os.walk(stylePath).next()[2]
        styleName = className+'.qml'
        if styleName in availableStyles:
            path = os.path.join(stylePath, styleName)
            qml = self.utils.parseStyle(path)
            return qml
        else:
            return None
    
    def prepareLoad(self):
        dbName = self.abstractDb.getDatabaseName()
        groupList =  iface.legendInterface().groups()
        if dbName in groupList:
            return groupList.index(dbName)
        else:
            parentTreeNode = iface.legendInterface().addGroup(self.abstractDb.getDatabaseName(), -1)
            return parentTreeNode

    def createMeasureColumn(self, layer):
        if layer.geometryType() == QGis.Polygon:
            layer.addExpressionField('$area', QgsField('area_otf', QVariant.Double))
        elif layer.geometryType() == QGis.Line:
            layer.addExpressionField('$length', QgsField('comprimento_otf', QVariant.Double))
        return layer
    
        