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
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class RemoveSmallLinesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(RemoveSmallLinesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Remove Small Lines')
        
        #self.flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifySmallLinesProcess')
        #self.parameters = {'Classes': self.flagsDict.keys()}
    
    def preProcess(self):
        """
        Gets the process that should be execute before this one
        """
        return self.tr('Identify Small Lines')

    def postProcessSteps(self):
        """
        Gets the process that should be execute before this one
        """
        return self.tr('Identify Small Lines')

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!

            # getting parameters after the execution of our pre process
            self.flagsDict = self.abstractDb.getFlagsDictByProcess('IdentifySmallLinesProcess')

            flagsClasses = self.flagsDict.keys()
            self.startTimeCount()
            if len(flagsClasses) == 0:
                self.setStatus(self.tr('There are no small lines.'), 1) #Finished
                return 1
            numberOfProblems = 0
            for cl in flagsClasses:
                # preparation
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                lyr = self.loadLayerBeforeValidationProcess(cl)
                localProgress.step()
                
                #running the process on cl
                localProgress = ProgressWidget(0, 1, self.tr('Running process on ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                problems = len(self.flagsDict[cl])
                smallIds = [int(flag['id']) for flag in self.flagsDict[cl]]
                lyr.startEditing()
                lyr.deleteFeatures(smallIds)
                localProgress.step()
                numberOfProblems += problems
                
                QgsMessageLog.logMessage(str(problems) + self.tr(' features from ')+cl+self.tr(' were changed.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                self.logLayerTime(cl)
            self.setStatus(str(numberOfProblems) + self.tr(' features were removed.'), 1) #Finished with flags
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0