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
from builtins import str
from qgis.core import QgsMessageLog, Qgis
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

class RemoveDuplicatesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(RemoveDuplicatesProcess,self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'correction'
        self.processAlias = self.tr('Remove Duplicated Elements')
        
        #self.flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifyDuplicatedGeometriesProcess')
        #self.parameters = {'Classes':self.flagsDict.keys()}

    def preProcess(self):
        """
        Gets the process that should be execute before this one
        """
        return self.tr('Identify Duplicated Geometries')

    def postProcess(self):
        return self.preProcess()

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        try:
            self.startTimeCount()
            self.setStatus(self.tr('Running'), 3) #now I'm running!

            # getting parameters after the execution of our pre process
            self.flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifyDuplicatedGeometriesProcess')

            flagsClasses = list(self.flagsDict.keys())
            if len(flagsClasses) == 0:
                self.setStatus(self.tr('There are no duplicated geometries.'), 1) #Finished
                return 1
            numberOfProblems = 0
            for cl in flagsClasses:
                # preparation
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(cl)
                localProgress.step()
                #running the process in the temp table
                localProgress = ProgressWidget(0, 1, self.tr('Running process on ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                problems = self.abstractDb.removeFeatures(processTableName,self.flagsDict[cl], keyColumn)
                localProgress.step()
                numberOfProblems += problems
                # finalization
                self.postProcessSteps(processTableName, lyr)
                QgsMessageLog.logMessage(str(problems) + self.tr(' duplicated features from ') + cl + self.tr(' were removed.'), "DSG Tools Plugin", Qgis.Critical)
                self.logLayerTime(cl)
            self.setStatus(str(numberOfProblems) + self.tr(' duplicated features were removed.'), 1)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0