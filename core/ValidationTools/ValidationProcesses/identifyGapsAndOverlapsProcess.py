# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-09-22
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
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsProject, Qgis
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

from collections import OrderedDict

from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess, ValidationAlgorithm
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

from PyQt5.QtCore import QCoreApplication
import processing
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
                       QgsProcessingParameterMultipleLayers,
                       QgsWkbTypes,
                       QgsProcessingUtils,
                       QgsProcessingException)

class IdentifyGapsAndOverlapsAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUTLAYERS = 'INPUTLAYERS'
    FRAMELAYER = 'FRAMELAYER'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr('Coverage Polygon Layers'),
                QgsProcessing.TypeVectorPolygon
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED,
                self.tr('Process only selected features')
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.FRAMELAYER,
                self.tr('Frame Layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional = True
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
        geometryHandler = GeometryHandler()
        layerHandler = LayerHandler()
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        if inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUTLAYERS))
        frameLyr = self.parameterAsVectorLayer(parameters, self.FRAMELAYER, context)
        if frameLyr and frameLyr in inputLyrList:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.FRAMELAYER))
        isMulti = True
        for inputLyr in inputLyrList:
            isMulti &= QgsWkbTypes.isMultiType(int(inputLyr.wkbType()))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyrList[0], QgsWkbTypes.Polygon, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(inputLyrList, QgsWkbTypes.Polygon, onlySelected = onlySelected)
        lyr = self.overlayCoverage(coverage, context)
        if frameLyr:
            self.getGapsOfCoverageWithFrame(lyr, frameLyr, context)
        featureList, total = self.getIteratorAndFeatureCount(lyr) #only selected is not applied because we are using an inner layer, not the original ones
        geomDict = self.getGeomDict(featureList, isMulti, feedback, total)
        self.raiseFlags(geomDict, feedback)
        QgsProject.instance().removeMapLayer(lyr)
        return {self.FLAGS: self.dest_id}

    def overlayCoverage(self, coverage, context):
        output = QgsProcessingUtils.generateTempFilename('output.shp')
        parameters = {
            'ainput':coverage,
            'atype':0,
            'binput':coverage,
            'btype':0,
            'operator':0,
            'snap':0,
            '-t':False,
            'output':output,
            'GRASS_REGION_PARAMETER':None,
            'GRASS_SNAP_TOLERANCE_PARAMETER':-1,
            'GRASS_MIN_AREA_PARAMETER':0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER':0,
            'GRASS_VECTOR_DSCO':'',
            'GRASS_VECTOR_LCO':''
            }
        x = processing.run('grass7:v.overlay', parameters, context = context)
        lyr = QgsProcessingUtils.mapLayerFromString(x['output'], context)
        return lyr
    
    def getGapsOfCoverageWithFrame(self, coverage, frameLyr, context):
        dissolveParameters = {
            'INPUT' : coverage,
            'FIELD':[],
            'OUTPUT':'memory:'
        }
        dissolveOutput = processing.run('native:dissolve', dissolveParameters, context = context)
        differenceParameters = {
            'INPUT' : frameLyr,
            'OVERLAY' : dissolveOutput['OUTPUT'],
            'OUTPUT':'memory:'
        }
        differenceOutput = processing.run('native:difference', differenceParameters, context = context)
        for feat in differenceOutput['OUTPUT'].getFeatures():
            self.flagFeature(feat.geometry(), self.tr('Gap in coverage with frame'))
    
    def getGeomDict(self, featureList, isMulti, feedback, total):
        geomDict = dict()
        for current, feat in enumerate(featureList):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            geom = feat.geometry()
            if isMulti and not geom.isMultipart():
                geom.convertToMultiType()
            geomKey = geom.asWkb()
            if geomKey not in geomDict:
                geomDict[geomKey] = []
            geomDict[geomKey].append(feat)
            # # Update the progress bar
            attrList = feat.attributes()
            if attrList == len(attrList)*[None]:
                self.flagFeature(geom, self.tr('Gap in coverage layer.'))
            feedback.setProgress(int(current * total)) 
        return geomDict

    def raiseFlags(self, geomDict, feedback):
        for k, v in geomDict.items():
            if feedback.isCanceled():
                break
            if len(v) > 1:
                textList = []
                for feat in v:
                    textList += ['({0},{1})'.format(feat['a_featid'], feat['a_layer'])]
                flagText = self.tr('Overlapping features (id,layer): {0}').format(', '.join(set(textList)))
                self.flagFeature(v[0].geometry(), flagText) 

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifygapsandoverlaps'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Gaps and Overlaps in Coverage Layers')

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
        return IdentifyGapsAndOverlapsAlgorithm()

class IdentifyGapsAndOverlapsProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifyGapsAndOverlapsProcess, self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'identification'
        self.processAlias = self.tr('Identify Earth Coverage Gaps and Overlaps')

        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a'], withElements = withElements, excludeValidation = True)
            # adjusting process parameters
            interfaceDict = dict()
            for key in self.classesWithElemDict:
                cat, lyrName, geom, geomType, tableType = key.split(',')
                interfaceDict[key] = {self.tr('Category'):cat, self.tr('Layer Name'):lyrName, self.tr('Geometry\nColumn'):geom, self.tr('Geometry\nType'):geomType, self.tr('Layer\nType'):tableType}
            # adjusting process parameters
            self.parameters = {'Reference and Layers': OrderedDict({'referenceDictList':{}, 'layersDictList':interfaceDict})}

    def execute(self):
        """
        Reimplementation of the execute method from the parent class
        """
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        try:
            self.startTimeCount()
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            refKey, classesKeys = self.parameters['Reference and Layers']
            if len(classesKeys) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1

            if not refKey:
                self.setStatus(self.tr('One reference must be selected! Stopping.'), 1) #Finished
                return 1

            # preparing reference layer
            refDict = self.classesWithElemDict[refKey]
            refcl = """{0}.{1}""".format(refDict['tableSchema'], refDict['tableName'])
            reflyr = self.loadLayerBeforeValidationProcess(refDict)

            # gathering all coverage layers
            classlist = []
            for key in classesKeys:
                self.startTimeCount()
                # preparation
                cl = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + cl['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                lyr = self.loadLayerBeforeValidationProcess(cl)
                classlist.append(lyr)
                localProgress.step()

            # creating the unified layer
            coverage = self.createUnifiedLayer(classlist)

            # creating the temporary coverage layer on postgis
            self.abstractDb.createAndPopulateCoverageTempTable(coverage)

            # running the process
            localProgress = ProgressWidget(0, 1, self.tr('Running process for coverage_temp'), parent=self.iface.mapCanvas())
            localProgress.step()
            result = self.abstractDb.getGapsAndOverlapsRecords(refcl, refDict['geom'])
            localProgress.step()

            #storing flags
            recordFlagList = []
            if len(result) > 0:
                for r in result:
                    featId, reason, geom = r
                    recordFlagList.append(('validation.coverage_temp', featId, reason, geom, 'geom'))

            #removing the coverage layer
            try:
                QgsProject.instance().removeMapLayer(coverage.id())
            except:
                QgsMessageLog.logMessage(self.tr('Error while trying to remove coverage layer.'), "DSG Tools Plugin", Qgis.Critical)
            
            # storing flags
            if len(recordFlagList) > 0:
                numberOfProblems = self.addFlag(recordFlagList)
                msg = self.tr('There are {} gaps or overlaps in the coverage layer. Check flags.').format(numberOfProblems)
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('The coverage has no gaps or overlaps.')
                self.setStatus(msg, 1) #Finished

            # dropping temp table
            self.abstractDb.dropTempTable('validation.coverage_temp')
            self.logLayerTime('coverage')


            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0

    def updateProgress(self):
        self.localProgress.step()