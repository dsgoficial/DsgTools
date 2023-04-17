# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-04-15
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Felipe Diniz - Cartographic Engineer @ Brazilian Army
        email                : diniz.felipe@eb.mil.br
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

from collections import defaultdict
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterField,
                       QgsProcessingUtils,
                       QgsPointXY,
                       QgsGeometry,
                       QgsRectangle,
                       QgsFeature,
                       QgsSpatialIndex,
                       QgsWkbTypes,
                       QgsFeatureRequest,
                       QgsProcessingMultiStepFeedback,
                       QgsField)
from qgis.PyQt.QtCore import QCoreApplication

class SplitPolygonsByGrid(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    X_DISTANCE = 'X_DISTANCE'
    Y_DISTANCE = 'Y_DISTANCE'
    NEIGHBOUR = 'NEIGHBOUR'
    ID_FIELD = 'ID_FIELD'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return SplitPolygonsByGrid()

    def name(self):
        return 'polygon_split_by_grid'

    def displayName(self):
        return self.tr('Polygon Split by Grid')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Geometric Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Geometric Algorithms"

    def shortHelpString(self):
        return self.tr("Splits input polygon layer by regular grid with user-defined X and Y distances and dissolves the intersection polygons based on the nearest neighbor's ID attribute.")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr('Input Polygon Layer'), [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(
            QgsProcessingParameterDistance(
                self.X_DISTANCE, self.tr('X Distance'), parentParameterName=self.INPUT, minValue=0.0, defaultValue=0.0001))
        self.addParameter(
            QgsProcessingParameterDistance(
                self.Y_DISTANCE, self.tr('Y Distance'), parentParameterName=self.INPUT, minValue=0.0, defaultValue=0.0001))
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.NEIGHBOUR, self.tr('Neighbour Polygon Layer'), [QgsProcessing.TypeVectorPolygon]))
        self.addParameter(
            QgsProcessingParameterField(
                self.ID_FIELD, self.tr('Attribute Field'), parentLayerParameterName=self.NEIGHBOUR, type=QgsProcessingParameterField.Any))
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, self.tr('Output Layer')))

    def processAlgorithm(self, parameters, context, feedback):
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        source = self.parameterAsSource(parameters, self.INPUT, context)
        x_distance = self.parameterAsDouble(parameters, self.X_DISTANCE, context)
        y_distance = self.parameterAsDouble(parameters, self.Y_DISTANCE, context)
        neighbour_source = self.parameterAsSource(parameters, self.NEIGHBOUR, context)
        class_field = self.parameterAsString(parameters, self.ID_FIELD, context)

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                               source.fields(), source.wkbType(), source.sourceCrs())

        # Create a spatial index for the Neighbour layer

        nFeats = source.featureCount()
        features = source.getFeatures()
        # Create a dictionary to store dissolved geometries
        multiStepFeedback = QgsProcessingMultiStepFeedback(nFeats, feedback)
        
        for current, feature in enumerate(features):
            multiStepFeedback.setCurrentStep(current)
            if multiStepFeedback.isCanceled():
                break
            outputFeatures = self.runSplitAndDissolve(
                layer=source,
                neighborsLayer=parameters[self.NEIGHBOUR],
                neighborFields=neighbour_source.fields(),
                feature=feature,
                x_distance=x_distance,
                y_distance=y_distance,
                classFieldName=class_field,
                context=context,
                feedback=multiStepFeedback,
            )
            if outputFeatures is None:
                continue
            sink.addFeatures(outputFeatures)

        return {self.OUTPUT: dest_id}

    def runSplitAndDissolve(self, layer, neighborsLayer, neighborFields, feature, x_distance, y_distance, classFieldName, context, feedback):
        algRunner = AlgRunner()
        multiStepFeedback = QgsProcessingMultiStepFeedback(14, feedback)
        multiStepFeedback.setCurrentStep(0)
        if multiStepFeedback.isCanceled():
            return []
        featureLayer = self.layerHandler.createMemoryLayerWithFeature(layer, feature, context=context, isSource=True)
        multiStepFeedback.setCurrentStep(1)
        if multiStepFeedback.isCanceled():
            return []
        bbox = feature.geometry().boundingBox()
        xmin, ymin, xmax, ymax = bbox.toRectF().getCoords()
        xSpacing = x_distance if abs(xmax-xmin) > x_distance else min(abs(xmax-xmin)/2, abs(ymax-ymin)/2)
        ySpacing = y_distance if abs(ymax-ymin) > y_distance else min(abs(xmax-xmin)/2, abs(ymax-ymin)/2)
        gridLayer = algRunner.runCreateGrid(
            extent=bbox,
            crs=layer.sourceCrs(),
            hSpacing=xSpacing,
            vSpacing=ySpacing,
            context=context
        )
        multiStepFeedback.setCurrentStep(2)
        if multiStepFeedback.isCanceled():
            return []
        algRunner.runCreateSpatialIndex(gridLayer, context=context)
        multiStepFeedback.setCurrentStep(3)
        if multiStepFeedback.isCanceled():
            return []
        clippedPolygons = algRunner.runClip(gridLayer, featureLayer, context=context)
        multiStepFeedback.setCurrentStep(4)
        if multiStepFeedback.isCanceled():
            return []
        algRunner.runCreateSpatialIndex(clippedPolygons, context=context)
        nFeats = clippedPolygons.featureCount()
        if nFeats == 0:
            return None
        multiStepFeedback.setCurrentStep(5)
        if multiStepFeedback.isCanceled():
            return []
        bufferZone = algRunner.runBuffer(featureLayer, distance=max(xSpacing,ySpacing), context=context)
        multiStepFeedback.setCurrentStep(6)
        if multiStepFeedback.isCanceled():
            return []
        algRunner.runCreateSpatialIndex(bufferZone, context)
        multiStepFeedback.setCurrentStep(7)
        if multiStepFeedback.isCanceled():
            return []
        clippedNeighbors = algRunner.runClip(neighborsLayer, bufferZone, context=context)
        multiStepFeedback.setCurrentStep(8)
        if multiStepFeedback.isCanceled():
            return []
        localNeighborVertexes = algRunner.runExtractVertices(clippedNeighbors, context=context)
        multiStepFeedback.setCurrentStep(9)
        if multiStepFeedback.isCanceled():
            return []
        neighbour_idx = QgsSpatialIndex(localNeighborVertexes.getFeatures())
        neighbourFeatDict = {feat.id():feat for feat in localNeighborVertexes.getFeatures()}
        stepSize = 100/nFeats
        clippedPolygons.startEditing()
        clippedPolygons.beginEditCommand("Updating features")
        clippedPolygonsDataProvider = clippedPolygons.dataProvider()
        if not any(i.name() == classFieldName for i in clippedPolygons.fields()):
            clippedPolygonsDataProvider.addAttributes([i for i in neighborFields if i.name() == classFieldName])
            clippedPolygons.updateFields()
        fieldIdx = clippedPolygons.fields().indexFromName(classFieldName)
        for current, feat in enumerate(clippedPolygons.getFeatures()):
            if multiStepFeedback.isCanceled():
                return []
            geom = feat.geometry()
            nearest_neighbor_id = neighbour_idx.nearestNeighbor(geom.centroid().asPoint(), 1)[0]
            destinationAttr = neighbourFeatDict[nearest_neighbor_id][classFieldName]
            clippedPolygonsDataProvider.changeAttributeValues(
                {
                    feat.id(): {
                        fieldIdx: destinationAttr
                    }
                }
            )
            multiStepFeedback.setProgress(current * stepSize)
        clippedPolygons.endEditCommand()
        multiStepFeedback.setCurrentStep(10)
        if multiStepFeedback.isCanceled():
            return []
        snappedToGrid = algRunner.runSnapToGrid(
            inputLayer=clippedPolygons,
            tol=1e-15,
            context=context
        )
        multiStepFeedback.setCurrentStep(11)
        if multiStepFeedback.isCanceled():
            return []
        dissolvedLyr = algRunner.runDissolve(
            inputLyr=snappedToGrid,
            field=[classFieldName],
            context=context,
        )
        multiStepFeedback.setCurrentStep(12)
        if multiStepFeedback.isCanceled():
            return []
        snappedLyr = algRunner.runSnapGeometriesToLayer(
            dissolvedLyr, localNeighborVertexes, tol=1e-6, context=context, behavior=2
        )
        multiStepFeedback.setCurrentStep(13)
        if multiStepFeedback.isCanceled():
            return []
        retainedFields = algRunner.runRetainFields(
            snappedLyr, [field.name() for field in layer.fields()], context=context
        )
        return [feat for feat in retainedFields.getFeatures()]
