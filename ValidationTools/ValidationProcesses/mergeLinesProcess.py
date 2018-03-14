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
from qgis.core import QgsMessageLog, QgsGeometry, QgsDataSourceURI
from DsgTools.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
import binascii

class MergeLinesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating=False):
        """
        Constructor
        """
        super(self.__class__,self).__init__(postgisDb, iface, instantiating)
        self.processAlias = self.tr('Merge lines with common attributes')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements=True, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Classes': interfaceDictList, 'Only Selected':False, 'AttributeBlackList (comma separated)':''}

    def postProcess(self):
        """
        Gets the process that should be execute after this one
        """
        return self.tr('Clean Geometries') #more than one post process (this is treated in validationManager)

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
            attributeNames = self.parameters['AttributeBlackList (comma separated)']
            if ',' in attributeNames:
                attributeNames = attributeNames.split(',')
            else:
                attributeNames = [attributeNames]
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
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

                # getting the key column
                uri = QgsDataSourceURI(lyr.dataProvider().dataSourceUri())
                keyColumn = uri.keyColumn()

                localProgress = ProgressWidget(1, size, self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                # iterating over features to store them in groups having same attributes
                featuresDict = {}
                columns = None
                for feat in featureList:
                    # getting the column names only once
                    if not columns:
                        columns = [field.name() for field in feat.fields() if (field.type() != 6 and field.name() != keyColumn)]
                    attributes = []
                    for column in columns:
                        # iterating only over allowed attribute names
                        if column in attributeNames:
                            continue
                        # creating a key using the selected attributes
                        if not feat[column]:
                            attributes.append('')
                        else:
                            attributes.append(u'{}'.format(feat[column]))
                    # making a string out of the key
                    attributes = ''.join(attributes)
                    if attributes not in featuresDict.keys():
                        featuresDict[attributes] = []
                    # storing the features
                    featuresDict[attributes].append(feat)

                    localProgress.step()

                localProgress = ProgressWidget(1, len(featuresDict.keys()), self.tr('Merging lines for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                lyr.startEditing()
                lyr.beginEditCommand('Merging lines')
                idsToRemove = []
                # iterating over the dictionary
                for key in featuresDict.keys():
                    # getting all features of a group
                    features = featuresDict[key]
                    for feature in features:
                        # if the feature is already in the remove list there is no point in checking it
                        if feature.id() in idsToRemove:
                            continue
                        geom = feature.geometry()
                        for other in features:
                            # the same idea applies here
                            if other.id() == feature.id():
                                continue
                            if other.id() in idsToRemove:
                                continue
                            # checking the spatial predicate touches
                            if geom.touches(other.geometry()):
                                # this generates a multi geometry
                                geom = geom.combine(other.geometry())
                                # this make a single line string if the multi geometries are neighbors
                                geom = geom.mergeLines()
                                # making a "single" multi geometry (useful for databases that use multi types)
                                geom.convertToMultiType()
                                # marking the other feature as to be removed
                                idsToRemove.append(other.id())
                                # updating feature
                                feature.setGeometry(geom)
                                # updating layer
                                lyr.updateFeature(feature)
                    localProgress.step()
                    
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