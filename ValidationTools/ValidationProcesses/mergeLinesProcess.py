# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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

class MergeLinesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Merge lines')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Classes': interfaceDictList, 'Only Selected':False, 'Attributes (comma separated)':''}

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
            attributeNames = self.parameters['Attributes (comma separated)']
            if ',' in attributeNames:
                attributeNames = attributeNames.split(',')
            else:
                attributeNames = [attributeNames]
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

                allIds = lyr.allFeatureIds()
                localProgress = ProgressWidget(1, len(allIds) - 1, self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                if self.parameters['Only Selected']:
                    featureList = lyr.selectedFeatures()
                else:
                    featureList = lyr.getFeatures()

                # iterating over features to store start and end points
                featuresDict = {}
                for feat in featureList:
                    attributes = []
                    for attributeName in attributeNames:
                        if not feat[attributeName]:
                            attributes.append('')
                        else:
                            attributes.append(feat[attributeName])
                    attributes = ''.join(attributes)
                    if attributes not in featuresDict.keys():
                        featuresDict[attributes] = []
                    featuresDict[attributes].append(feat)

                    localProgress.step()

                localProgress = ProgressWidget(0, 1, self.tr('Merging lines for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                lyr.startEditing()
                lyr.beginEditCommand('Merging lines')
                idsToRemove = []
                for key in featuresDict.keys():
                    features = featuresDict[key]
                    alreadyUsed = []
                    for feature in features:
                        if feature.id() in idsToRemove:
                            continue
                        geom = feature.geometry()
                        for other in features:
                            if other.id() == feature.id():
                                continue
                            if other.id() in alreadyUsed:
                                continue
                            if geom.touches(other.geometry()):
                                geom = geom.combine(other.geometry())
                                geom = geom.mergeLines()
                                geom.convertToMultiType()
                                idsToRemove.append(other.id())
                            alreadyUsed.append(other.id())
                        lyr.changeGeometry(feature.id(), geom)
                        alreadyUsed.append(feature.id())
                lyr.deleteFeatures(idsToRemove)
                lyr.endEditCommand()
                localProgress.step()
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])

            self.setStatus(self.tr('All lines were merged.'), 1) #Finished with flags
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            self.finishedWithError()
            return 0