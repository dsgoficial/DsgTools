# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-05-01
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
from __future__ import absolute_import
from builtins import range
import itertools
from qgis.core import QgsMessageLog, QgsVectorLayer, QgsGeometry, QgsField, QgsVectorDataProvider, \
                      QgsFeatureRequest, QgsExpression, QgsFeature, QgsSpatialIndex, Qgis, \
                      QgsCoordinateTransform, QgsWkbTypes, QgsProcessingMultiStepFeedback,\
                      QgsVectorLayerUtils, QgsCoordinateReferenceSystem, QgsProject
from qgis.PyQt.Qt import QObject, QVariant

from .geometryHandler import GeometryHandler
from .attributeHandler import AttributeHandler
from DsgTools.core.Utils.FrameTools.map_index import UtmGrid

class FeatureHandler(QObject):
    def __init__(self, iface=None, parent=None):
        super(FeatureHandler, self).__init__()
        self.parent = parent
        self.iface = iface
        if iface:
            self.canvas = iface.mapCanvas()
        self.geometryHandler = GeometryHandler(iface)
        self.attributeHandler = AttributeHandler(iface)
        self.utmGrid = UtmGrid()
        self.stepsTotal = 0
    
    def reclassifyFeatures(self, featureList, destinationLayer, reclassificationDict, coordinateTransformer, parameterDict):
        newFeatList = []
        deleteList = []
        for feat in featureList:
            geom = self.geometryHandler.reprojectWithCoordinateTransformer(feat.geometry(), coordinateTransformer)
            geomList = self.geometryHandler.adjustGeometry(geom, parameterDict)
            newFeatList += self.createFeaturesWithAttributeDict(geomList, feat, reclassificationDict, destinationLayer)
            deleteList.append(feat.id())
        return newFeatList, deleteList
    
    def createFeaturesWithAttributeDict(self, geomList, originalFeat, attributeDict, destinationLayer):
        """
        Creates a newFeatureList using each geom from geomList. attributeDict is used to set attributes
        """
        newFeatureList = []
        fields = destinationLayer.fields()
        for geom in geomList:
            newFeature = QgsFeature(fields)
            newFeature.setGeometry(geom)
            newFeature = self.attributeHandler.setFeatureAttributes(newFeature, attributeDict, oldFeat = originalFeat)
            newFeatureList.append(newFeature)
        return newFeatureList

    def createFeatureFromLayer(self, layer, attributes=None, geom=None, fields=None):
        """
        Creates a feature for a layer. Attributes for new feature may be passed on
        for pre-populating it.
        :param layer: (QgsVectorLayer) layer from which a new feature will be
                      generated.
        :param attributes: (dict) attributes to be set to new feature.
        :param geom: (QgsGeometry) geometry to be for the new feature.
        :param fields: (QgsFields) a set of fields to be set to the new feature,
                        if not provided, it will be read from input layer (non-optimal).
        :return: (QgsFeature) new feature.
        """
        newFeature = QgsFeature(fields or layer.fields())
        if geom:
            newFeature.setGeometry(geom)
        if attributes:
            newFeature = self.attributeHandler.setFeatureAttributes(newFeature, attributes)
        return newFeature

    def createUnifiedFeature(self, unifiedLyr, feature, classname, bList = None, attributeTupple = False, coordinateTransformer = None, parameterDict = None):
        parameterDict = {} if parameterDict is None else parameterDict
        bList = [] if bList is None else bList
        newFeats = []
        for geom in self.geometryHandler.handleGeometry(feature.geometry(), parameterDict=parameterDict, coordinateTransformer=coordinateTransformer):
            newfeat = QgsFeature(unifiedLyr.fields())
            newfeat.setGeometry(feature.geometry())
            newfeat['featid'] = feature.id()
            newfeat['layer'] = classname
            if attributeTupple:
                newfeat['tupple'] = self.attributeHandler.getTuppleAttribute(feature, unifiedLyr, bList=bList)
            newFeats.append(newfeat)
        return newFeats
    
    def getNewFeatureWithoutGeom(self, referenceFeature, lyr):
        newFeat = QgsFeature(referenceFeature)
        # provider = lyr.dataProvider()
        # in case of no PK found, use the FIRST registered column
        for idx in lyr.primaryKeyAttributes() or [0]:
            newFeat.setAttribute(idx, None)
        return newFeat
    
    def handleFeature(self, featList, featureWithoutGeom, lyr, parameterDict = None, coordinateTransformer = None):
        parameterDict = {} if parameterDict is None else parameterDict
        geomList = []
        for feat in featList:
            geomList += self.geometryHandler.handleGeometry(feat.geometry(), parameterDict, coordinateTransformer)
        geomToUpdate = None
        newFeatList = []
        if not geomList:
            return geomToUpdate, [], True
        for idx, geom in enumerate(geomList):
            if idx == 0:
                geomToUpdate = geom
                continue
            else:
                newFeat = self.getNewFeatureWithoutGeom(featureWithoutGeom, lyr)
                newFeat.setGeometry(geom)
                newFeatList.append(newFeat)
        return geomToUpdate, newFeatList, False

    def handleConvertedFeature(self, feat, lyr, parameterDict = None, coordinateTransformer = None):
        parameterDict = {} if parameterDict is None else parameterDict
        geomList = self.geometryHandler.handleGeometry(feat.geometry(), parameterDict, coordinateTransformer)
        newFeatSet = set()
        for geom in geomList:
            newFeat = QgsVectorLayerUtils.createFeature(lyr, geom)
            for idx, field in enumerate(lyr.fields()):
                fieldName = field.name()
                if idx not in lyr.primaryKeyAttributes() \
                    and fieldName in newFeat and fieldName in feat:
                    newFeat[field.name()] = feat[field.name()]
            newFeatSet.add(newFeat)
        return newFeatSet

    def getFeatureOuterShellAndHoles(self, feat, isMulti):
        geom = feat.geometry()
        
        outershells, donutholes = self.geometryHandler.getOuterShellAndHoles(geom, isMulti)
        outershellList = []
        for shell in outershells:
            outerShellFeat = QgsFeature(feat)
            outerShellFeat.setGeometry(shell)
            outershellList.append(outerShellFeat)

        donutHoleList = []
        for hole in donutholes:
            newFeat = QgsFeature(feat)
            newFeat.setGeometry(hole)
            donutHoleList.append(newFeat)
        return outershellList, donutHoleList
    
    def mergeLineFeatures(self, featList, lyr, idsToRemove, networkDict, parameterDict=None, feedback=None):
        parameterDict = {} if parameterDict is None else parameterDict
        changeDict = dict()
        size = 100 / len(featList)
        for current, feat_a in enumerate(featList):
            if feedback:
                if feedback.isCanceled():
                    break
            id_a = feat_a.id()
            if id_a in idsToRemove:
                continue
            for feat_b in featList:
                if feedback:
                    if feedback.isCanceled():
                        break
                id_b = feat_b.id()
                if id_a == id_b or id_b in idsToRemove:
                    continue
                geom_a = feat_a.geometry()
                geom_b = feat_b.geometry()
                if geom_a.touches(geom_b):
                    intersectionPoint = geom_a.intersection(geom_b)
                    for pointPart in intersectionPoint.asGeometryCollection():
                        point = pointPart.asPoint()
                        if (point in networkDict and len(networkDict[point]) == 2):
                            newGeom = self.geometryHandler.handleGeometry(geom_a.combine(geom_b).mergeLines(), parameterDict)[0] #only one candidate is possible because features are touching
                            feat_a.setGeometry(newGeom)
                            lyr.updateFeature(feat_a)
                            idsToRemove.append(id_b)
                            # changeDict[id_a] = newGeom
            if feedback:
                feedback.setProgress(size*current)
        # for id, geom in changeDict.items():
        #     lyr.changeGeometry(id, geom)
    
    def getNewGridFeat(self, index, geom, fields):
        feat = QgsFeature(fields)
        feat['inom'] = index
        feat['mi'] = self.utmGrid.get_MI_MIR_from_inom(index)
        feat.setGeometry(geom)
        return feat
    
    def getSystematicGridFeatures(self, featureList, index, stopScale, coordinateTransformer,\
        fields, constraintDict=None, feedback=None):
        if feedback is not None and feedback.isCanceled():
            return
        scale = self.utmGrid.getScale(index)
        if scale == stopScale:
            frameGeom = self.createGridItem(
                index,
                coordinateTransformer,
                constraintDict
            )
            if frameGeom is None:
                return
            newFeat = self.getNewGridFeat(index, frameGeom, fields)
            featureList.append(newFeat)
        else:
            scaleId = self.utmGrid.getScaleIdFromiNomen(index)
            sufixIterator = itertools.chain.from_iterable(
                self.utmGrid.scaleText[scaleId+1]
            ) #flatten list into one single list
            localMultiStepFeedback = QgsProcessingMultiStepFeedback(
                len(sufixIterator),
                feedback
            )
            for i, line in enumerate(sufixIterator):
                if feedback is not None and feedback.isCanceled():
                    break
                localMultiStepFeedback.setCurrentStep(i)
                inomen2 = '{oldInomem}-{newPart}'.format(oldInomem=index, newPart=line)
                if coordinateTransformer is not None \
                    and self.createGridItem(
                        inomen2, coordinateTransformer, constraintDict
                    ) is None:
                    continue
                self.getSystematicGridFeatures(featureList, inomen2, stopScale, coordinateTransformer, fields, feedback=feedback)

    def createGridItem(self, index, coordinateTransformer, constraintDict):
        frameGeom = self.utmGrid.getQgsPolygonFrame(index)
        frameGeom.transform(coordinateTransformer)
        frameBB = frameGeom.boundingBox()
        engine = QgsGeometry.createGeometryEngine(frameGeom.constGet())
        engine.prepareGeometry()
        for fid in constraintDict['spatialIdx'].intersects(frameBB):
            if getattr(engine, constraintDict['predicate'])(
                    constraintDict['idDict'][fid].geom().constGet()
                ):
                return frameGeom
        return None

    def getSystematicGridFeaturesWithConstraint(self, featureList, inputLyr, stopScale,\
                            coordinateTransformer, fields, feedback=None, predicate=None):
        """
        TODO: Progress
        """
        if feedback is not None and feedback.isCanceled():
            return
        predicate = 'intersects' if predicate is None else predicate
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr('Creating spatial index'))
        spatialIdx, idDict = self.buildSpatialIndexAndIdDict(
            inputLyr,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr('Getting candidate start indexes'))
        xmin, ymin, xmax, ymax = self.getLyrUnprojectedGeographicBounds(
            inputLyr
        )
        inomenList = self.utmGrid.get_INOM_range_from_BB(
            xmin, ymin, xmax, ymax
        )
        multiStepFeedback.setCurrentStep(3)
        multiStepFeedback.pushInfo(self.tr('Building grid'))
        gridMultistepFeedback = QgsProcessingMultiStepFeedback(
            len(inomenList),
            multiStepFeedback
        )
        constraintDict = {
            'spatialIdx' : spatialIdx,
            'idDict' : idDict,
            'predicate' : predicate
        }
        for i, inomen in enumerate(inomenList):
            gridMultistepFeedback.setCurrentStep(i)
            if gridMultistepFeedback.isCanceled():
                break
            self.getSystematicGridFeatures(
                featureList,
                inomen,
                stopScale,
                coordinateTransformer,
                fields,
                constraintDict=constraintDict,
                feedback=None
            )


    def buildSpatialIndexAndIdDict(self, inputLyr, feedback=None,\
                                                    featureRequest=None):
        """
        creates a spatial index for the input layer
        :param inputLyr: (QgsVectorLayer) input layer;
        :param feedback: (QgsProcessingFeedback) processing feedback;
        :param featureRequest: (QgsFeatureRequest) optional feature request;
        """
        spatialIdx = QgsSpatialIndex()
        idDict = {}
        featCount = inputLyr.featureCount()
        size = 100/featCount if featCount else 0
        iterator = inputLyr.getFeatures() if featureRequest is None\
            else inputLyr.getFeatures(featureRequest)
        addFeatureAlias = lambda x: self.addFeatureToSpatialIndex(
            current=x[0],
            feat=x[1],
            spatialIdx=spatialIdx,
            idDict=idDict,
            size=size,
            feedback=feedback
        )
        list(map(addFeatureAlias, enumerate(iterator)))
        return spatialIdx, idDict

    def addFeatureToSpatialIndex(self, current, feat, spatialIdx,\
                                                idDict, size, feedback):
        """
        Adds feature to spatial index. Used along side with a
        python map operator to improve performance.
        :param current : (int) current index
        :param feat : (QgsFeature) feature to be added on spatial
        index and on idDict
        :param spatialIdx: (QgsSpatialIndex) spatial index
        :param idDict: (dict) dictionary with format {feat.id(): feat}
        :param size: (int) size to be used to update feedback
        :param feedback: (QgsProcessingFeedback) feedback to be used
        on processing
        """
        if feedback is not None and feedback.isCanceled():
            return
        idDict[feat.id()] = feat
        spatialIdx.addFeature(feat)
        if feedback is not None:
            feedback.setProgress(size * current)

    def getLyrUnprojectedGeographicBounds(self, inputLyr):
        crs = inputLyr.crs()
        coordinateTransformer = QgsCoordinateTransform(
            crs,
            QgsCoordinateReferenceSystem(crs.geographicCrsAuthId()),
            QgsProject.instance()
        )
        reprojectedGeographicBB = coordinateTransformer.transformBoundingBox(
            inputLyr.boundingBox()
        )
        xmin = reprojectedGeographicBB.xMinimum()
        ymin = reprojectedGeographicBB.yMinimum()
        xmax = reprojectedGeographicBB.xMaximum()
        ymax = reprojectedGeographicBB.yMaximum()
        return xmin, xmax, ymin, ymax
