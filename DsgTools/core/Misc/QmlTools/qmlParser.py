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
from builtins import range
from builtins import object
from qgis.PyQt.QtXml import QDomDocument


class QmlParser(object):
    def __init__(self, fileName):
        """
        Constructor
        """
        self.fileName = fileName
        self.qml = QDomDocument()
        self.qgisElement = None
        self.edittypesElement = None
        self.edittypeElementList = []
        self.domainDict = dict()

    def loadFileContent(self):
        """
        Loads QML data
        """
        qml = open(self.fileName, "r")
        data = qml.read()
        loaded = self.qml.setContent(data)
        qml.close()
        return loaded

    def readQGISElement(self):
        """
        Reads the QML's parent node
        """
        self.qgisElement = self.qml.documentElement()

    def readEdittypesElement(self):
        """
        Read edittypes element
        """
        self.edittypeElementList = []

        elements = self.qgisElement.elementsByTagName("edittypes")
        self.edittypesElement = elements.item(0).toElement()
        elements = self.edittypesElement.elementsByTagName("edittype")
        for i in range(len(elements)):
            self.edittypeElementList.append(elements.item(i).toElement())

    def readEdittypeElement(self, edittypeElement):
        """
        Read a specific edittype tag
        """
        type = edittypeElement.attribute("widgetv2type")
        if type == "ValueMap":
            name = edittypeElement.attribute("name")
            valueMapDict = dict()
            nodes = edittypeElement.elementsByTagName("widgetv2config")
            widgetv2configElement = nodes.item(0).toElement()
            values = widgetv2configElement.elementsByTagName("value")
            for i in range(len(values)):
                value = values.item(i).toElement()
                keyText = value.attribute("key")
                # print 'key: '+keyText
                valueText = value.attribute("value")
                # print 'value: '+valueText
                valueMapDict[keyText] = valueText
            self.domainDict[name] = valueMapDict
        elif type == "ValueRelation":
            name = edittypeElement.attribute("name")
            nodes = edittypeElement.elementsByTagName("widgetv2config")
            widgetv2configElement = nodes.item(0).toElement()
            filter = widgetv2configElement.attribute("FilterExpression")
            table = widgetv2configElement.attribute("Layer")
            filter_keys = filter.replace("code in (", "").replace(")", "").split(",")
            self.domainDict[name] = (table, filter_keys)

    def getDomainDict(self):
        """
        Gets the domain dictionary (value relation and value map)
        """
        self.domainDict.clear()

        if not self.loadFileContent():
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr("Warning!"),
                self.tr(
                    "QML file not loaded properly. Enum values won't be available."
                ),
            )
            return

        self.readQGISElement()
        self.readEdittypesElement()
        for edittypeElement in self.edittypeElementList:
            self.readEdittypeElement(edittypeElement)
        return self.domainDict
