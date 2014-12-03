# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
import sys, os
from PyQt4.QtXml import *
from PyQt4.QtCore import QFile, QIODevice, QTextStream, QString

class QmlParser:
    def __init__(self, fileName):
        self.fileName = fileName
        self.qml = QDomDocument()
        self.qgisElement = None
        self.edittypesElement = None
        self.edittypeElementList = [] 
        self.domainDict = dict()
        
    def loadFileContent(self):
        qml = open(self.fileName, 'r')
        data = qml.read()
        loaded = self.qml.setContent(data)
        qml.close()
        return loaded
        
    def readQGISElement(self):
        self.qgisElement = self.qml.documentElement()
        
    def readEdittypesElement(self):
        self.edittypeElementList = []
        
        elements = self.qgisElement.elementsByTagName("edittypes")
        self.edittypesElement = elements.item(0).toElement()
        elements = self.edittypesElement.elementsByTagName("edittype")
        for i in range(len(elements)):
            self.edittypeElementList.append(elements.item(i).toElement())
        
    def readEdittypeElement(self, edittypeElement):
        type = edittypeElement.attribute("widgetv2type")
        if type == "ValueMap":
            name = edittypeElement.attribute("name")
            valueMapDict = dict()
            nodes = edittypeElement.elementsByTagName("widgetv2config")
            widgetv2configElement = nodes.item(0).toElement()
            values = widgetv2configElement.elementsByTagName("value")
            for i in range(len(values)):
                value = values.item(i).toElement()
                valueMapDict[str(value.attribute("key"))] = str(value.attribute("value"))
            self.domainDict[str(name)] = valueMapDict
            
    def getDomainDict(self):
        self.domainDict.clear()
        
        if not self.loadFileContent():
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "QML file not loaded properly. Enum values won't be available.")
            return
            
        self.readQGISElement()
        self.readEdittypesElement()
        for edittypeElement in self.edittypeElementList:
            self.readEdittypeElement(edittypeElement)
        return self.domainDict
