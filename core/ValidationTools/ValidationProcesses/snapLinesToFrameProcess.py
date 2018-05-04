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
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

from collections import OrderedDict

class SnapLinesToFrameProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(SnapLinesToFrameProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Snap Lines to Frame')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDict = dict()
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            self.frameCandidateDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a'], withElements = withElements, excludeValidation = True)
            frameDict = dict()
            for key in self.frameCandidateDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                frameDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}

            self.parameters = {'Snap': 5.0, 'Reference and Layers': OrderedDict({'referenceDictList':frameDict, 'layersDictList':interfaceDict})}
        
    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!

            # getting frame and reference parameters
            refKey, linesKeys = self.parameters['Reference and Layers']
            if len(linesKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1

            if not refKey:
                self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
                return 1

            frameDict = self.frameCandidateDict[refKey]
            frame = """{0}.{1}""".format(frameDict['tableSchema'], frameDict['tableName'])
            frameGeometryColumn = frameDict['geom']
                
            tol = self.parameters['Snap']

            for key in linesKeys:
                self.startTimeCount()
                # preparation
                lineDict = self.classesWithElemDict[key]
                cl = """{0}.{1}""".format(lineDict['tableSchema'], lineDict['tableName'])
                geometryColumn = lineDict['geom']
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl, parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(lineDict)
                frameTableName, frameLyr, frameKeyColumn = self.prepareExecution(frameDict)
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
                self.logLayerTime(lineDict['tableSchema']+'.'+lineDict['tableName'])

            msg = self.tr('All features snapped to frame succesfully.')
            self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0