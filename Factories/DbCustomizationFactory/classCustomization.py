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
        email                : borba@dsg.eb.mil.br
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
#DsgTools Imports
from DsgTools.Factories.DbCustomizationFactory.dbCustomization import DbCustomization

class ClassCustomization(DbCustomization):
    def __init__(self, customJson):
        super(ClassCustomization, self).__init__(customJson)
    
    def buildSql(self):
        #Abstract method. Must be reimplemented in each child.
        pass
    
    def buildUndoSql(self):
        #Abstract method. Must be reimplemented in each child.
        pass