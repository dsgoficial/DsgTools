# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-04-06
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
from qgis.core import QgsMessageLog
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess

class RemoveDuplicatesProcess(ValidationProcess):
    def __init__(self, postgisDb, codelist):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, codelist)

    def preProcess(self):
        '''
        Gets the process that should be execute before this one
        '''
        return 'IdentifyDuplicatedGeometriesProcess'

    def postProcess(self):
        '''
        Gets the process that should be execute before this one
        '''
        return 'IdentifyDuplicatedGeometriesProcess'

    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage('Starting '+self.getName()+'Process.\n', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus('Running', 3) #now I'm running!
            flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifyDuplicatedGeometriesProcess')
            numberOfProblems = 0
            for cl in flagsDict.keys():
                numberOfProblems += self.abstractDb.removeFeatures(cl,flagsDict[cl])
            self.setStatus('%s features were removed.\n' % numberOfProblems, 1)
            QgsMessageLog.logMessage('%s features were removed.\n' % numberOfProblems, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0