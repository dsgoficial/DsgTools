# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-04-05
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
from qgis.core import QgsMessageLog, QGis
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.ValidationTools.ValidationProcesses.identifyDanglesProcess import IdentifyDanglesProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
import binascii

class IdentifySmallLinesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Identify Small Lines')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {self.tr('Length'): 5.0, 'Classes': interfaceDictList, 'Only Selected':False, 'Only First Order Lines':False}
            self.identifyDangles = IdentifyDanglesProcess(postgisDb, iface, instantiating = True)
            self.identifyDangles.parameters = self.parameters
        
    def preProcess(self):
        return self.tr(self.tr('Clean Geometries'))

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            tol = self.parameters[self.tr('Length')]
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1
            classesWithGeom = []
            recordList = []
            for key in classesWithElem:
                self.startTimeCount()
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                localProgress.step()

                if self.parameters['Only Selected']:
                    featureList = [i for i in lyr.selectedFeatures()]
                else:
                    featureList = [i for i in lyr.getFeatures()]
                size = len(featureList)
                
                if self.parameters['Only First Order Lines']:
                    endVerticesDict = self.identifyDangles.buildInitialAndEndPointDict(featureList, classAndGeom['tableSchema'], classAndGeom['tableName'])
                    idList = self.identifyDangles.searchDanglesOnPointDict(endVerticesDict, classAndGeom['tableSchema'], classAndGeom['tableName'], returnIdList = True)
                    featureList = [i for i in featureList if i.id() in idList]

                localProgress = ProgressWidget(1, size, self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                for feat in featureList:
                    if feat.geometry().length() < tol:
                        geometry = binascii.hexlify(feat.geometry().asWkb())
                        recordList.append((classAndGeom['tableSchema']+'.'+classAndGeom['tableName'], feat.id(), self.tr('Small Line.'), geometry, classAndGeom['geom']))
                    localProgress.step()
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])

            if len(recordList) > 0:
                numberOfProblems = self.addFlag(recordList)
                msg =  str(numberOfProblems)+ self.tr(' features have small lines. Check flags.')
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('There are no small lines.')
                self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0