# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-20
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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

class RemoveEmptyGeometriesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False, withElements = True):
        """
        Constructor
        """
        super(RemoveEmptyGeometriesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processAlias = self.tr('Remove Empty Geometries')
    
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=[], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Classes': interfaceDictList}
        
    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        try:
            self.startTimeCount()
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1
                # preparation
            for key in classesWithElem:
                classAndGeom = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(classAndGeom)
                localProgress.step()

                # running the process
                localProgress = ProgressWidget(0, 1, self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                self.abstractDb.removeEmptyGeometries(processTableName, classAndGeom['geom'])
                localProgress.step()
                
                # finalization
                self.postProcessSteps(processTableName, lyr)
                #removes null geometries
                for feat in lyr.getFeatures():
                    if not feat.geometry():
                        lyr.deleteFeature(feat.id())
                localProgress.step()
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])
            msg = self.tr('Process executed successfully!')
            self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0