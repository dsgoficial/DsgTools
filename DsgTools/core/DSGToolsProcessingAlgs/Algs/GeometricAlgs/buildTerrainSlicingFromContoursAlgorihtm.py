# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-16
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import numpy as np
import processing
from osgeo import gdal
from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsFeature, QgsFeatureSink, QgsField, QgsFields,
                       QgsGeometry, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer, QgsProcessingUtils,
                       QgsProject, QgsVectorLayer, QgsWkbTypes)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler


class BuildTerrainSlicingFromContoursAlgorihtm(QgsProcessingAlgorithm):

    INPUT = 'INPUT'
    CONTOUR_INTERVAL = 'CONTOUR_INTERVAL'
    GEOGRAPHIC_BOUNDARY = 'GEOGRAPHIC_BOUNDARY'
    AREA_WITHOUT_INFORMATION_POLYGONS = 'AREA_WITHOUT_INFORMATION_POLYGONS'
    WATER_BODIES_POLYGONS = 'WATER_BODIES_POLYGONS'
    MIN_PIXEL_GROUP_SIZE = 'MIN_PIXEL_GROUP_SIZE'
    SMOOTHING_PARAMETER = 'SMOOTHING_PARAMETER'
    OUTPUT_POLYGONS = 'OUTPUT_POLYGONS'
    OUTPUT_RASTER = 'OUTPUT_RASTER'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT,
                self.tr('Input DEM'),
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.CONTOUR_INTERVAL,
                self.tr('Equidistance value'), 
                type=QgsProcessingParameterNumber.Integer, 
                minValue=0,
                defaultValue=10
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr('Geographic bounds layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=False
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AREA_WITHOUT_INFORMATION_POLYGONS,
                self.tr('Area without information layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.WATER_BODIES_POLYGONS,
                self.tr('Water bodies layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_PIXEL_GROUP_SIZE,
                self.tr('Minimum pixel group size'), 
                type=QgsProcessingParameterNumber.Integer, 
                minValue=0,
                defaultValue=100
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SMOOTHING_PARAMETER,
                self.tr('Smoothing parameter'), 
                type=QgsProcessingParameterNumber.Double, 
                minValue=0,
                defaultValue=0.001
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_POLYGONS,
                self.tr('Output polygons')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output slicing')
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        algRunner = AlgRunner()
        self.geometryHandler = GeometryHandler()
        inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        threshold = self.parameterAsInt(
            parameters, self.CONTOUR_INTERVAL, context)
        geoBoundsSource = self.parameterAsSource(
            parameters, self.GEOGRAPHIC_BOUNDARY, context)
        areaWithoutInformationSource = self.parameterAsSource(
            parameters, self.AREA_WITHOUT_INFORMATION_POLYGONS, context)
        waterBodiesSource = self.parameterAsSource(
            parameters, self.WATER_BODIES_POLYGONS, context)
        minPixelGroupSize = self.parameterAsInt(
            parameters, self.MIN_PIXEL_GROUP_SIZE, context
        )
        smoothingThreshold = self.parameterAsDouble(
            parameters, self.SMOOTHING_PARAMETER, context
        )
        outputRaster = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
        outputFields = self.getOutputFields()
        (output_sink, output_sink_id) = self.getOutputSink(inputRaster, outputFields, parameters, context)

        multiStepFeedback = QgsProcessingMultiStepFeedback(15, feedback) #ajustar depois
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)

        geographicBounds = self.overlayPolygonLayer(
            inputLyr=parameters[self.GEOGRAPHIC_BOUNDARY],
            polygonLyr=parameters[self.AREA_WITHOUT_INFORMATION_POLYGONS],
            crs=inputRaster.crs() if inputRaster is not None else QgsProject.instance().crs(),
            context=context,
            feedback=multiStepFeedback,
            operator=2
        ) if areaWithoutInformationSource is not None and \
            areaWithoutInformationSource.featureCount() > 0 else parameters[self.GEOGRAPHIC_BOUNDARY]
        
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        geographicBounds = self.overlayPolygonLayer(
            inputLyr=geographicBounds,
            polygonLyr=parameters[self.WATER_BODIES_POLYGONS],
            crs=inputRaster.crs() if inputRaster is not None else QgsProject.instance().crs(),
            context=context,
            feedback=multiStepFeedback,
            operator=2
        ) if waterBodiesSource is not None and \
            waterBodiesSource.featureCount() > 0 else geographicBounds
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        clippedRaster = algRunner.runClipRasterLayer(
            inputRaster,
            mask=geographicBounds,
            context=context,
            feedback=multiStepFeedback,
            noData=-9999
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        slicedDEM = algRunner.runGrassMapCalcSimple(
            inputA=clippedRaster,
            expression=f'{threshold} * floor(A / {threshold})',
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        slicingThresholdDict = self.findSlicingThresholdDict(slicedDEM)
        expression = '\n'.join(
            [
                f"{a} thru {b} = {i}" for i, (a, b) in slicingThresholdDict.items()
            ]
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        bufferedGeographicBounds = algRunner.runBuffer(
            parameters[self.GEOGRAPHIC_BOUNDARY],
            distance=10*smoothingThreshold,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        clippedRaster = algRunner.runClipRasterLayer(
            inputRaster,
            mask=bufferedGeographicBounds,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        classifiedRaster = algRunner.runGrassReclass(
            clippedRaster, expression, context=context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        sieveOutput = algRunner.runSieve(
            classifiedRaster,
            threshold=minPixelGroupSize,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        finalRaster = algRunner.runClipRasterLayer(
            sieveOutput,
            mask=geographicBounds,
            context=context,
            feedback=multiStepFeedback,
            outputRaster=outputRaster
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        polygonLayer = algRunner.runGdalPolygonize(
            sieveOutput,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        smoothPolygons = algRunner.runChaikenSmoothing(
            polygonLayer,
            threshold=smoothingThreshold,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        ) if smoothingThreshold > 0 else polygonLayer
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        overlayedPolygons = self.overlayPolygonLayer(
            inputLyr=smoothPolygons,
            polygonLyr=geographicBounds,
            crs=inputRaster.crs() if inputRaster is not None else QgsProject.instance().crs(),
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        # multiStepFeedback.setCurrentStep(currentStep)
        # cleanedPolygons = self.cleanPolyonLayer()
        # currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(overlayedPolygons, context, feedback=multiStepFeedback)
        currentStep += 1

        featCount = overlayedPolygons.featureCount()
        if featCount == 0:
            return {
                "OUTPUT_POLYGONS": output_sink_id,
                "OUTPUT_RASTER": finalRaster,
            }

        multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100/featCount
        valueSet = set(int(feat['a_DN']) for feat in overlayedPolygons.getFeatures())
        diff = valueSet.difference(set(range(len(valueSet))))
        def classLambda(x):
            x = int(x)
            if x == 0:
                return x
            return x - 1 if diff != set() else x

        for current, feat in enumerate(overlayedPolygons.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            newFeat = QgsFeature(outputFields)
            newFeat['class'] = classLambda(feat['a_DN'])
            newFeat['class_min'], newFeat['class_max'] = slicingThresholdDict[feat['a_DN']]
            geom = self.validatePolygon(feat, overlayedPolygons)
            newFeat.setGeometry(geom)
            output_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
            multiStepFeedback.setProgress(current * stepSize)

        return {
            "OUTPUT_POLYGONS": output_sink_id,
            "OUTPUT_RASTER": finalRaster,
        }
    
    def validatePolygon(self, feat, overlayerPolygons):
        geom = feat.geometry()
        _, donutholes = self.geometryHandler.getOuterShellAndHoles(geom, False)
        filteredHoles = []
        holesIdsToDelete = set()
        if donutholes == []:
            return geom
        def holeWithValue(centerPoint):
            centerPointBB = centerPoint.boundingBox()
            for polygonFeat in overlayerPolygons.getFeatures(centerPointBB):
                polygonGeom = polygonFeat.geometry()
                if polygonGeom.equals(geom):
                    continue
                if polygonGeom.intersects(centerPoint):
                    return True
            return False
        for idx, hole in enumerate(donutholes):
            centerPoint = hole.pointOnSurface()
            hasValue = holeWithValue(centerPoint)
            if not hasValue:
                holesIdsToDelete.add(idx+1)
                continue
            filteredHoles.append(hole)
        if donutholes == filteredHoles:
            return geom
        geom = QgsGeometry(geom)
        for idx in holesIdsToDelete:
            geom.deleteRing(idx)
        return geom

    def overlayPolygonLayer(self, inputLyr, polygonLyr, crs, context, feedback, operator=0):
        parameters = {
            'ainput': inputLyr,
            'atype': 0,
            'binput': polygonLyr,
            'btype': 0,
            'operator': operator,
            'snap': 0,
            '-t': False,
            'output': 'TEMPORARY_OUTPUT',
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_MIN_AREA_PARAMETER': 1e-15,
            'GRASS_OUTPUT_TYPE_PARAMETER': 3,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_LCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False
            }
        x = processing.run(
            'grass7:v.overlay',
            parameters,
            context=context,
            feedback=feedback
        )
        lyr = QgsProcessingUtils.mapLayerFromString(x['output'], context)
        lyr.setCrs(crs)
        return lyr
    
    def findSlicingThresholdDict(self, inputRaster):
        ds = gdal.Open(inputRaster)
        npRaster = np.array(ds.GetRasterBand(1).ReadAsArray())
        npRaster = npRaster[~np.isnan(npRaster)] # removes nodata values
        minValue = np.amin(npRaster)
        maxValue = np.amax(npRaster)
        numberOfElevationBands = self.getNumberOfElevationBands(maxValue - minValue)
        areaRatioList = self.getAreaRatioList(numberOfElevationBands)
        uniqueValues, uniqueCount = np.unique(npRaster, return_counts=True)
        cumulativePercentage = np.cumsum(uniqueCount) / np.prod(npRaster.shape)
        areaPercentageValues = uniqueCount / np.prod(npRaster.shape)
        if any(areaPercentageValues >= 0.48) and numberOfElevationBands > 2:
            """
            The MTM spec states that if there is an elevation slice that covers more than
            50% of the map, there must only be 2 elevation bands.
            """
            idx = np.argmax(areaPercentageValues >= 0.5)
            if idx == 0:
                return {
                    0: (int(uniqueValues[0]), int(uniqueValues[1])),
                    1: (int(uniqueValues[1]), int(uniqueValues[-1])),
                }
            elif idx == len(areaPercentageValues):
                return {
                    0: (int(uniqueValues[0]), int(uniqueValues[-2])),
                    1: (int(uniqueValues[-2]), int(uniqueValues[-1])),
                }
            else:
                return {
                    0: (int(uniqueValues[0]), int(uniqueValues[idx])),
                    1: (int(uniqueValues[idx]), int(uniqueValues[idx+1])),
                }
        
        if numberOfElevationBands == 2 and np.argmax(areaPercentageValues >= 0.5) == 0:
            return {
                    0: (int(uniqueValues[0]), int(uniqueValues[1])),
                    1: (int(uniqueValues[1]), int(uniqueValues[-1])),
                }

        classThresholds = list(uniqueValues[
                np.searchsorted(
                    cumulativePercentage,
                    np.cumsum(areaRatioList)
                )
            ]
        )
        classDict = dict()
        lowerBounds = [minValue]+classThresholds if minValue not in classThresholds else classThresholds
        for i, (a, b) in enumerate(zip(lowerBounds, classThresholds)):
            classDict[i] = (int(a), int(b))
        return classDict


    def getAreaRatioList(self, numberOfElevationBands):
        bandDict = {
            2: [0.6, 0.4],
            3: [0.3, 0.4, 0.3],
            4: [0.2, 0.3, 0.3, 0.2],
        }
        return bandDict[numberOfElevationBands]
    
    def getOutputSink(self, inputRaster, outputFields, parameters, context):
        return self.parameterAsSink(
            parameters,
            self.OUTPUT_POLYGONS,
            context,
            outputFields,
            QgsWkbTypes.Polygon,
            inputRaster.crs() if inputRaster is not None else QgsProject.instance().crs()
        )
    
    def getNumberOfElevationBands(self, range):
        if range <= 100:
            return 2
        elif range <= 600:
            return 3
        else:
            return 4
    
    def getOutputFields(self):
        fields = QgsFields()
        fields.append(QgsField('class', QVariant.Int))
        fields.append(QgsField('class_min', QVariant.Int))
        fields.append(QgsField('class_max', QVariant.Int))

        return fields


    def tr(self, string):
        return QCoreApplication.translate('BuildTerrainSlicingFromContoursAlgorihtm', string)

    def createInstance(self):
        return BuildTerrainSlicingFromContoursAlgorihtm()

    def name(self):
        return 'buildterrainslicingfromcontours'

    def displayName(self):
        return self.tr('Build Terrain Slicing from Contours')

    def group(self):
        return self.tr('Geometric Algorithms')

    def groupId(self):
        return 'DSGTools: Geometric Algorithms'

    def shortHelpString(self):
        return self.tr("O algoritmo constrói o fatiamento do terreno baseado nas curvas de nível.")
