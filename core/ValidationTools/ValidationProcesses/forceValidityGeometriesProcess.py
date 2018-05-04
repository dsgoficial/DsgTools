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
from qgis.core import QgsMessageLog, QgsVectorLayer, Qgis
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

class ForceValidityGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(ForceValidityGeometriesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Force Geometries Validity')
        
        # we should use this code here when the pre Process is used
        #self.flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifyInvalidGeometriesProcess')
        #self.parameters = {'Classes': self.flagsDict.keys()}
        
    def preProcess(self):
        """
        Gets the process that should be execute before this one
        """
        return self.tr('Identify Invalid Geometries')
        
    def postProcess(self):
        """
        Gets the process that should be execute after this one
        """
        return [self.tr('Deaggregate Geometries'), self.tr('Identify Invalid Geometries')] #more than one post process (this is treated in validationManager)

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr('Process.\n'), "DSG Tools Plugin", Qgis.Critical)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            # getting parameters after the execution of our pre process
            self.flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifyInvalidGeometriesProcess')
            classesWithFlags = list(self.flagsDict.keys())
            self.startTimeCount()
            if len(classesWithFlags) == 0:
                self.setStatus(self.tr('There are no invalid geometries.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('There are no invalid geometries.'), "DSG Tools Plugin", Qgis.Critical)
                return 1
            numberOfProblems = 0
            for cl in classesWithFlags:
                self.startTimeCount()
                # preparation
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(cl)
                localProgress.step()
                #running the process in the temp table
                localProgress = ProgressWidget(0, 1, self.tr('Running process on ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                problems = self.abstractDb.forceValidity(processTableName, self.flagsDict[cl], keyColumn)
                localProgress.step()
                numberOfProblems += problems
                self.logLayerTime(cl) #check this time later (I guess time will be counted twice due to postProcess)
                # finalization
                self.postProcessSteps(processTableName, lyr)
                QgsMessageLog.logMessage(self.tr('{0} features from {1} were changed.').format(problems, cl), "DSG Tools Plugin", Qgis.Critical)
            self.setStatus(self.tr('{0} features were changed.').format(numberOfProblems), 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0