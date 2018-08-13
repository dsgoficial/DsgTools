# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.ValidationTools.ValidationProcesses.identifyDanglesProcess import IdentifyDanglesProcess

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterNumber)

class IdentifySmallLinesAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorLine ]
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr('Line length tolerance'),
                minValue=0,
                defaultValue=100
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('Flag layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        inputLyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        tol = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        self.prepareFlagSink(parameters, inputLyr, inputLyr.wkbType(), context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        featureList, total = self.getIteratorAndFeatureCount(inputLyr)           

        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            if feat.geometry().length() < tol:
                flagText = self.tr('Feature from layer {0} with id={1} has length of value {2:.2f}, which is lesser than the tolerance of {3} units.').format(inputLyr.name(), feat.id(), feat.geometry().length(), tol)
                self.flagFeature(feat.geometry(), flagText)      
            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {self.FLAGS: self.flagSink}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifysmalllines'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Small Lines')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Validation Tools')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Validation Tools'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IdentifySmallLinesAlgorithm()

class IdentifySmallLinesProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifySmallLinesProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'identification'
        self.processAlias = self.tr('Identify Small Lines')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['l'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDictList = []
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDictList.append({self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType})
            self.parameters = {'Length': 1.0, 'Classes': interfaceDictList, 'Only Selected':False, 'Only First Order Lines':False}
            self.identifyDangles = IdentifyDanglesProcess(postgisDb, iface, instantiating = True)
            self.identifyDangles.parameters = self.parameters

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            tol = self.parameters['Length']
            classesWithElem = self.parameters['Classes']
            self.startTimeCount()
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1
            featFlagList = []
            flagLyr = self.getFlagLyr(1)
            for key in classesWithElem:
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
                    pointList = self.identifyDangles.searchDanglesOnPointDict(endVerticesDict, classAndGeom['tableSchema'], classAndGeom['tableName'])
                    idList = [endVerticesDict[point][0] for point in pointList]
                    featureList = [i for i in featureList if i.id() in idList]

                localProgress = ProgressWidget(1, size, self.tr('Running process on ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                for feat in featureList:
                    if feat.geometry().length() < tol:
                        newFlag = self.buildFlagFeature(flagLyr, self.processName, classAndGeom['tableSchema'], classAndGeom['tableName'], feat.id(), classAndGeom['geom'], feat.geometry(), self.tr('Small line. Line length smaller than {0}').format(tol))
                        featFlagList.append(newFlag)
                    localProgress.step()
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])

            if len(featFlagList) > 0:
                self.raiseVectorFlags(flagLyr, featFlagList)
                numberOfProblems = len(featFlagList)
                msg = self.tr('{0} features have small lines. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('There are no small lines.')
                self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0