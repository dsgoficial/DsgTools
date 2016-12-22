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
    def __init__(self):
        super(CustomJSONBuilder,self).__init__()
    
    def buildClassElement(self, schema, name, attrList):
        return {'schema':schema, 'name':name, 'attrs':attrList}
    
    def buildNewAttributeElement(self, schema, name, attrList):
        return {'schema':schema, 'name':name, 'attrs':attrList}
    
    def buildAttributeElement(self, attrName, attrType, isPk, isNullable, defaultValue = None, references = None, filter = []):
        return {'attrName':attrName, 'attrType':attrType, 'isPk':isPk, 'isNullable':isNullable, 'defaultValue':defaultValue, 'references':references, 'filter':filter}

    def addDomainTableElement(self, domainName, valueDict):
        return {'domainName':domainName, 'valueDict': valueDict}
    
    def addValueToValueDict(self, valueDict, code, codeName):
        if code not in valueDict.keys():
            valueDict[code] = codeName
    
    def buildCodeNameToChangeElement(self, domainTable, codeValue, oldCodeName, newCodeName):
        return {'domainTable':domainTable, 'codeValue':codeValue, 'oldCodeName':oldCodeName, 'newCodeName':newCodeName}
    
    def buildChangeDefaultElement(self, schema, table, attrName, oldValue, newValue):
        return {'schema': schema, 'table': table, 'attrName':attrName, 'oldValue':oldValue, 'newValue':newValue}
    
    def buildChangeNullityElemnt(self, schema, table, attrName, notNull):
        return {'schema':schema, 'table':table, 'attrName':attrName, 'notNull':notNull}
