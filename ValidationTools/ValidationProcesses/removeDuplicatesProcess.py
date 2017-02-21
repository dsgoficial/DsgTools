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
    def __init__(self, postgisDb, iface):
        '''
        Constructor
        '''
        super(self.__class__,self).__init__(postgisDb, iface)
        self.processAlias = self.tr('Remove Duplicated Elements')
        
        self.flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifyDuplicatedGeometriesProcess')
        self.parameters = {'Classes':self.flagsDict.keys()}

    def preProcess(self):
        '''
        Gets the process that should be execute before this one
        '''
        return self.tr('Identify Duplicated Geometries')
 
    def execute(self):
        '''
        Reimplementation of the execute method from the parent class
        '''
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            flagsClasses = self.parameters['Classes']
            if len(flagsClasses) == 0:
                self.setStatus(self.tr('There are no duplicated geometries.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('There are no duplicated geometries.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            numberOfProblems = 0
            for cl in flagsClasses:
                # preparation
                processTableName, lyr = self.prepareExecution(cl)
                #running the process in the temp table
                problems = self.abstractDb.removeFeatures(processTableName,self.flagsDict[cl])
                numberOfProblems += problems
                # finalization
                self.postProcessSteps(processTableName, lyr)
                QgsMessageLog.logMessage(self.tr('{0} duplicated features from {1} were removed.').format(problems, cl), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.setStatus(self.tr('{0} duplicated features were removed.').format(numberOfProblems), 1)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0