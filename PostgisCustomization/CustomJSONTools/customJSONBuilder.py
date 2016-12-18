# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-17
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import json
#Qt Imports
from PyQt4.Qt import QObject
#DsgTools Imports

class CustomJSONBuilder(QObject):
    def __init__(self, jsonDict):
        super(CustomJSONBuilder,self).__init__()
        self.jsonDict = jsonDict
    
    def buildClassElement(self, name, attrList, schema):
        return {'name':name, 'attrs':attrList,'schema':schema}
    
    def buildAttributeElement(self, attrName, attrType, isPk, isNullable, defaultValue = None, references = None):
        return {'attrName':attrName, 'attrType':attrType, 'isPk':isPk, 'isNullable':isNullable, 'defaultValue':defaultValue, 'references':references}

    def buildDomainElement(self, domainName, valueDict):
        return {'domainName':domainName, 'valueDict': valueDict}
