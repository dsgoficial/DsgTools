# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-09-29
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luizclaudio.andrade@eb.mil.br
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
from qgis.core import QgsMessageLog, QgsGeometry
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
import binascii

class IdentifyDanglesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Identify Dangles')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Classes': interfaceDictList, 'Only Selected':False}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                QgsMessageLog.logMessage(self.tr('No classes selected! Nothing to be done.'), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                return 1
            recordList = []
            for key in classesWithElem:
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                lyr = self.loadLayerBeforeValidationProcess(classAndGeom)
                localProgress.step()

                if self.parameters['Only Selected']:
                    featureList = lyr.selectedFeatures()
                    size = len(featureList)
                else:
                    featureList = lyr.getFeatures()
                    size = len(lyr.allFeatureIds())

                localProgress = ProgressWidget(1, size, self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                # start and end points dict
                endVerticesDict = {}
                # iterating over features to store start and end points
                for feat in featureList:
                    geom = feat.geometry()
                    if geom.isMultipart():
                        multiLine = geom.asMultiPolyline()
                        for j in xrange(len(multiLine)):
                            line = multiLine[j]
                            startPoint = line[0]
                            endPoint = line[len(line) - 1]
                            # storing start point in the dict
                            if startPoint not in endVerticesDict.keys():
                                endVerticesDict[startPoint] = []
                            endVerticesDict[startPoint].append(feat.id())
                            # storing end point in the dict
                            if endPoint not in endVerticesDict.keys():
                                endVerticesDict[endPoint] = []
                            endVerticesDict[endPoint].append(feat.id())
                    else:
                        line = geom.asPolyline()
                        startPoint = line[0]
                        endPoint = line[len(line) - 1]
                        # storing start point in the dict
                        if startPoint not in endVerticesDict.keys():
                            endVerticesDict[startPoint] = []
                        endVerticesDict[startPoint].append(feat.id())
                        # storing end point in the dict
                        if endPoint not in endVerticesDict.keys():
                            endVerticesDict[endPoint] = []
                        endVerticesDict[endPoint].append(feat.id())

                    localProgress.step()

                # actual search for dangles
                localProgress = ProgressWidget(1, len(endVerticesDict.keys()), self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                for point in endVerticesDict.keys():
                    # this means we only have one occurrence of point, therefore it is a dangle
                    if len(endVerticesDict[point]) > 1:
                        localProgress.step()
                        continue
                    geometry = binascii.hexlify(QgsGeometry.fromPoint(point).asWkb())
                    featid = endVerticesDict[point][0]
                    recordList.append((classAndGeom['tableSchema']+'.'+classAndGeom['tableName'], featid, self.tr('Dangle.'), geometry, classAndGeom['geom']))
                    localProgress.step()
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])

            if len(recordList) > 0:
                numberOfProblems = self.addFlag(recordList)
                msg = str(numberOfProblems) + self.tr(' features have dangles. Check flags.')
                self.setStatus(msg, 4) #Finished with flags
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                msg = self.tr('There are no dangles.')
                self.setStatus(msg, 1) #Finished
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0