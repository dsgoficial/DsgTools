# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-06-22
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

class CheckEarthCoverageProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(CheckEarthCoverageProcess,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Check Earth Coverage')
        
        if not self.instantiating:
            # getting area tables with elements
            classesWithElemDictList = self.abstractDb.listGeomClassesFromDatabase(primitiveFilter=['a'], withElements=True, getGeometryColumn=True)
            # creating a list of tuples (layer names, geometry columns)
            classesWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # creating a list of tuples (layer names, geometry columns)
            frameWithElem = ['{0}:{1}'.format(i['layerName'], i['geometryColumn']) for i in classesWithElemDictList]
            # adjusting process parameters
            self.parameters = {'Reference and Layers': (frameWithElem, classesWithElem)}
        
    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!

            # getting frame and reference parameters
            refWithElem = self.parameters['Reference and Layers'][0]
            lines = self.parameters['Reference and Layers'][1]
            frame, frameGeometryColumn = refWithElem.split(':')
            
            if len(lines) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1

            if not refWithElem:
                self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('One reference must be selected! Stopping.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
                
            tol = self.parameters['Snap']

            for classAndGeom in lines:
                # preparation
                cl, geometryColumn = classAndGeom.split(':')
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(cl, geometryColumn)
                frameTableName, frameLyr, frameKeyColumn = self.prepareExecution(frame, frameGeometryColumn)
                localProgress.step()

                #running the process in the temp table
                localProgress = ProgressWidget(0, 1, self.tr('Running process on ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                self.abstractDb.snapLinesToFrame([processTableName], frameTableName, tol, geometryColumn, keyColumn, frameGeometryColumn)
                self.abstractDb.densifyFrame([processTableName], frameTableName, tol, geometryColumn, frameGeometryColumn)
                localProgress.step()
                
                # finalization
                self.postProcessSteps(processTableName, lyr)
                self.postProcessSteps(frameTableName, frameLyr)
            msg = self.tr('All features snapped to frame succesfully.')
            self.setStatus(msg, 1) #Finished
            QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0