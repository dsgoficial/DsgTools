# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
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

from DsgTools.ValidationTools.ValidationProcesses.identifyInvalidGeometriesProcess import IdentifyInvalidGeometriesProcess

class ValidationManager(object):
    def __init__(self):
        object.__init__(self)
        self.currProc = None
        self.log = '' 
    
    def executeProcess(self, processName):
        if self.currProc == None:
            pass
    
    def currentProcess(self):
        return self.currProc