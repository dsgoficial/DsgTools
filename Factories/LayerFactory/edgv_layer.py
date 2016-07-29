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
    
    def getStyle(self, stylePath, schema, className):
        if 'db:' in stylePath:
            return self.abstractDb.getStyle(stylePath.split(':')[-1], schema, className)
        else:
            return self.getStyleFile(stylePath, className)
    
    def getStyleFile(self, stylePath, className):
        availableStyles = os.walk(stylePath).next()[2]
        styleName = className+'.qml'
        if styleName in availableStyles:
            return os.path.join(stylePath, styleName)
    
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
    
    def parseStyle(self, qml):
        if '.qml' in qml:
            doc = parse(qml)
        else:
            doc = parseString()
        forbiddenNode = doc.getElementsByTagName('edittypes')[0]
        qgisNode = doc.getElementsByTagName('qgis')[0]
        qgisNode.removeChild(forbiddenNode)
        return doc.toxml('utf-8')
        