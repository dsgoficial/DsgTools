# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-31
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
from qgis.PyQt.Qt import QObject
#DsgTools Imports

class CustomJSONValidator(QObject):
    def __init__(self, jsonFile):
        super(CustomJSONValidator,self).__init__()
        self.jsonFile = jsonFile
    
    def parseJson(self):
        pass
    
    def validateTags(self):
        pass
    
    def validateDsgToolsClassNames(self):
        pass
    
    def validateGeometricPrimitives(self):
        pass
    
    def validate(self):
        pass