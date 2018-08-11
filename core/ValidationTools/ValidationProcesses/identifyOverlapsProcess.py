# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-10-03
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
from builtins import str
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsProject, QgsGeometry, QgsVectorDataProvider, QgsFeatureRequest, QgsExpression, QgsFeature, Qgis
from DsgTools.core.ValidationTools.ValidationProcesses.validationProcess import ValidationProcess, ValidationAlgorithm
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.layerHandler import LayerHandler

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
                       QgsProcessingParameterMultipleLayers,
                       QgsWkbTypes)

class IdentifyOverlapsAlgorithm(ValidationAlgorithm):
    FLAGS = 'FLAGS'
    INPUTLAYERS = 'INPUTLAYERS'
    SELECTED = 'SELECTED'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUTLAYERS,
                self.tr('Coverage Polygons'),
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
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('Flag layer')
            )
        )

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

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        geometryHandler = GeometryHandler()
        layerHandler = LayerHandler()
        inputLyrList = self.parameterAsLayerList(parameters, self.INPUTLAYERS, context)
        if inputLyrList == []:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUTLAYERS))
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        self.prepareFlagSink(parameters, inputLyrList[0], QgsWkbTypes.Polygon, context)
        # Compute the number of steps to display within the progress bar and
        # get features from source
        
        epsg = inputLyrList[0].crs().authid().split(':')[-1]
        coverage = layerHandler.createAndPopulateUnifiedVectorLayer(inputLyrList, QgsWkbTypes.Polygon, epsg, onlySelected = onlySelected)
        lyr = self.overlayCoverage(coverage, context)
        featureList, total = self.getIteratorAndFeatureCount(lyr) #only selected is not applied because we are using an inner layer, not the original ones
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
            feedback.setProgress(int(current * total))         
        for k, v in geomDict.items():
            if feedback.isCanceled():
                break
            if len(v) > 1:
                layerList = ','.join( map(str, set([i['layername'] for i in v]) ) )
                flagText = self.tr('Features from layers {0} overlap.').format(layerList)
                self.flagFeature(v[0].geometry(), flagText) 

        return {self.FLAGS: self.dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifyoverlaps'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Overlaps')

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
        return IdentifyOverlapsAlgorithm()



class IdentifyOverlapsProcess(ValidationProcess):
    def __init__(self, postgisDb, iface, instantiating = False, withElements = True):
        """
        Constructor
        """
        super(IdentifyOverlapsProcess,self).__init__(postgisDb, iface, instantiating, withElements)
        self.processCategory = 'identification'
        self.processAlias = self.tr('Identify Layer Overlaps')
        
        if not self.instantiating:
            # getting tables with elements
            self.classesWithElemDict = self.abstractDb.getGeomColumnDictV2(primitiveFilter=['a'], withElements = withElements, excludeValidation = True)
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
        QgsMessageLog.logMessage(self.tr('Starting ')+self.getName()+self.tr(' Process.'), "DSG Tools Plugin", Qgis.Critical)
        self.startTimeCount()
        try:
            self.setStatus(self.tr('Running'), 3) #now I'm running!
            self.abstractDb.deleteProcessFlags(self.getName()) #erase previous flags
            classesWithElem = self.parameters['Classes']
            self.startTimeCount()
            if len(classesWithElem) == 0:
                self.setStatus(self.tr('No classes selected!. Nothing to be done.'), 1) #Finished
                return 1
            overlapsRecordList = []
            for key in classesWithElem:
                
                # preparation
                classAndGeom = self.classesWithElemDict[key]
                localProgress = ProgressWidget(0, 1, self.tr('Preparing execution for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                processTableName, lyr, keyColumn = self.prepareExecution(classAndGeom)
                localProgress.step()
                # running the process
                localProgress = ProgressWidget(0, 1, self.tr('Running process for ') + classAndGeom['tableName'], parent=self.iface.mapCanvas())
                localProgress.step()
                overlaps = self.abstractDb.getOverlapsRecords(processTableName, classAndGeom['geom'], keyColumn)
                localProgress.step()
                self.abstractDb.dropTempTable(processTableName)
                # storing flags
                if len(overlaps) > 0:
                    if classAndGeom['tableSchema'] not in ('validation'):
                        for result in overlaps:
                            id, reason, geom = result
                            overlapsRecordList.append((classAndGeom['tableSchema']+'.'+classAndGeom['tableName'], id, reason, geom, classAndGeom['geom']))
                self.logLayerTime(classAndGeom['tableSchema']+'.'+classAndGeom['tableName'])
            # storing flags
            if len(overlapsRecordList) > 0:
                numberOfOverlappingGeom = self.addFlag(overlapsRecordList)
                msg =  str(numberOfOverlappingGeom) + self.tr(' features are overlapping. Check flags.')
                self.setStatus(msg, 4) #Finished with flags
            else:
                msg = self.tr('There are no overlapping geometries.')
                self.setStatus(msg, 1) #Finished
            return 1
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
            self.finishedWithError()
            return 0
