# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-08-09
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Matheus Alves Silva - Cartographic Engineer @ Brazilian Army
        email                : matheus.silva@ime.eb.br
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
from PyQt5.QtCore import QCoreApplication, QVariant
import os
import concurrent.futures
from qgis import core
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessing,
    QgsGeometry,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsSpatialIndex,
    QgsFields,
    QgsProcessingParameterNumber,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsField,
    QgsProcessingParameterDistance,
    QgsProject,
    QgsWkbTypes,
    QgsPoint,
    QgsPointXY,
    QgsProcessingFeatureSourceDefinition,
)

from .validationAlgorithm import ValidationAlgorithm


class VerifyLigationAlgorithm(ValidationAlgorithm):
    POINT_FLAGS = "POINT_FLAGS"
    LINE_FLAGS = "LINE_FLAGS"
    INPUT_FRAME = "INPUT_FRAME"
    INPUT_LINE_POLYGON = "INPUT_LINE_POLYGON"
    ATTRIBUTES = "ATTRIBUTES"
    DISTANCE_SEARCH = "DISTANCE_SEARCH"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LINE_POLYGON,
                self.tr("Input layer"),
                [
                    QgsProcessing.TypeVectorLine,
                    QgsProcessing.TypeVectorPolygon,
                ],
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_FRAME,
                self.tr("Input frame"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            core.QgsProcessingParameterField(
                self.ATTRIBUTES,
                self.tr("Select the attributes for disconsiderer"),
                type=core.QgsProcessingParameterField.Any,
                parentLayerParameterName=self.INPUT_LINE_POLYGON,
                allowMultiple=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterDistance(
                self.DISTANCE_SEARCH,
                self.tr("Search distance"),
                parentParameterName=self.INPUT_FRAME,
                minValue=0.0,
                defaultValue=0.0001,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.POINT_FLAGS, self.tr("Point Flags"))
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.LINE_FLAGS, self.tr("Line Flags"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        algRunner = AlgRunner()
        inputLinePolyLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_LINE_POLYGON, context
        )
        inputFrameLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_FRAME, context
        )
        inputLyrAttributes = self.parameterAsFields(
            parameters, self.ATTRIBUTES, context
        )
        distSearch = self.parameterAsDouble(parameters, self.DISTANCE_SEARCH, context)

        fields = QgsFields()
        fields.append(QgsField("Flag", QVariant.String))

        (point_flag_sink, point_flag_sink_id) = self.parameterAsSink(
            parameters,
            self.POINT_FLAGS,
            context,
            fields,
            QgsWkbTypes.Point,
            inputLinePolyLyr.sourceCrs(),
        )

        (line_flag_sink, line_flag_sink_id) = self.parameterAsSink(
            parameters,
            self.LINE_FLAGS,
            context,
            fields,
            QgsWkbTypes.LineString,
            inputLinePolyLyr.sourceCrs(),
        )

        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.pushInfo(self.tr("processed layers."))

        # Transform the frame (polygon) em lines
        linesOfFrameLyr = algRunner.runPolygonsToLines(
            inputLyr=inputFrameLyr,
            context=context,
        )

        # Explode lines
        explodeLinesLyr = algRunner.runExplodeLines(
            inputLyr=linesOfFrameLyr,
            context=context,
        )

        # Spatial index of lines in frame
        lineFrameFeatDict, _, lineFrameSpatialIdx = self.spatialIndex(explodeLinesLyr)

        # Dict of lines in inside frame
        dictLineInsideFrame = defaultdict(list)

        stepSizeLine, feed = self.stepFeedbackLyr(multiStepFeedback, explodeLinesLyr)

        self.lineInsideFrame(
            explodeLinesLyr,
            lineFrameFeatDict,
            lineFrameSpatialIdx,
            dictLineInsideFrame,
            stepSizeLine,
            feed,
        )

        # List of line buffer
        listLineBuffFrame = []

        multiStepFeedback.setCurrentStep(1)
        multiStepFeedback.pushInfo(self.tr("Lines from inside the frame."))

        feed, stepSizeLineInside = self.stepFeedback(
            multiStepFeedback, dictLineInsideFrame
        )

        # Application buffer in the lines of frame
        self.linesBuffFrame(
            distSearch, dictLineInsideFrame, listLineBuffFrame, stepSizeLineInside, feed
        )

        # List of attributes
        attributes = self.listAttributes(inputLinePolyLyr, inputLyrAttributes)

        if inputLinePolyLyr.geometryType() == QgsWkbTypes.LineGeometry:
            # Extract specific vertices
            extractSpecifVertLyr = algRunner.runExtractSpecificVertices(
                inputLyr=inputLinePolyLyr,
                vertices="0, -1",
                context=context,
            )

            multiChildOne = QgsProcessingMultiStepFeedback(2, multiStepFeedback)
            multiChildOne.setCurrentStep(0)
            multiChildOne.pushInfo(self.tr("Specific vertices were extracted."))

            # Espacial Index
            specifVertFeatDict, _, specifVertSpatialIdx = self.spatialIndex(
                extractSpecifVertLyr
            )

            # Dict vertice in frame
            dictVertInFrame = defaultdict(list)

            feed, stepSize = self.stepFeedback(multiChildOne, listLineBuffFrame)

            self.verticesInFrame(
                listLineBuffFrame,
                specifVertFeatDict,
                specifVertSpatialIdx,
                dictVertInFrame,
                stepSize,
                multiChildOne,
            )

            multiChildOne.setCurrentStep(1)
            multiChildOne.pushInfo(self.tr("Vertices in frame."))

            feed, stepSize = self.stepFeedback(multiChildOne, dictVertInFrame)

            self.verifyLine(
                feed, attributes, dictVertInFrame, stepSize, fields, line_flag_sink
            )

        elif inputLinePolyLyr.geometryType() == QgsWkbTypes.PolygonGeometry:
            multiChildTwo = QgsProcessingMultiStepFeedback(4, multiStepFeedback)
            multiChildTwo.setCurrentStep(0)

            tempPolyLyr = algRunner.runCreateFieldWithExpression(
                inputLyr=inputLinePolyLyr,
                expression="$id",
                fieldName="featid",
                fieldType=1,
                context=context,
                is_child_algorithm=False,
            )

            algRunner.runCreateSpatialIndex(tempPolyLyr, context)

            # Spatial Index of polygons
            dictPolygon, idPolygon, polygonSpatialIdx = self.spatialIndex(tempPolyLyr)

            feed, stepSize = self.stepFeedback(multiChildTwo, listLineBuffFrame)

            # List of vertices polygons in frame
            setVtxPolyFrame = self.verticesPolyInFrame(
                listLineBuffFrame,
                stepSize,
                dictPolygon,
                polygonSpatialIdx,
                multiChildTwo,
            )

            multiChildTwo.setCurrentStep(1)
            multiChildTwo.pushInfo(self.tr("Vertices of polygon in frame."))

            idPolyIn = self.idPolygonInFrame(listLineBuffFrame, polygonSpatialIdx)

            listPolyOut = list(idPolygon.difference(idPolyIn))

            self.removePolygonsTempLyr(tempPolyLyr, listPolyOut)

            # Boundary of polygons of layer input
            boundaryPolygons = algRunner.runBoundary(
                inputLayer=tempPolyLyr,
                context=context,
            )

            # Explode lines of boundary of polygons
            explodeLinePolygon = algRunner.runExplodeLines(
                inputLyr=boundaryPolygons,
                context=context,
            )

            # Spatial Index of lines of boundary polygon
            dictExplodeLinePoly, _, explodeLinePolySpatialIdx = self.spatialIndex(
                explodeLinePolygon
            )

            feed, stepSize = self.stepFeedback(multiChildTwo, listLineBuffFrame)

            dictLinePoly = self.dictBBoxWktId(
                listLineBuffFrame,
                stepSize,
                dictExplodeLinePoly,
                explodeLinePolySpatialIdx,
                multiChildTwo,
            )

            multiChildTwo.setCurrentStep(2)
            multiChildTwo.pushInfo(self.tr("Check link between polygons "))

            feed, stepSize = self.stepFeedback(multiChildTwo, dictLinePoly)
            # List of lines
            listLines = self.verifyLigationPolygon(
                attributes,
                stepSize,
                dictExplodeLinePoly,
                dictLinePoly,
                fields,
                line_flag_sink,
                multiChildTwo,
            )

            # Spatial Index in frame
            dictLine, lineSpatialIndex = self.spatialIndexList(listLines)

            multiChildTwo.setCurrentStep(3)

            feed, stepSize = self.stepFeedback(multiChildTwo, setVtxPolyFrame)
            # List vertex of flag
            dictVtxFlag = self.vertexInLineFrame(
                stepSize, setVtxPolyFrame, dictLine, lineSpatialIndex, multiChildTwo
            )

            self.flagPoint(fields, point_flag_sink, dictVtxFlag)

        return {
            self.POINT_FLAGS: point_flag_sink_id,
            self.LINE_FLAGS: line_flag_sink_id,
        }

    def flagPoint(self, fields, point_flag_sink, dictVtxFlag):
        for vtx in dictVtxFlag:
            vtxFlag = QgsGeometry.fromWkt(vtx)
            if len(dictVtxFlag[vtx]) >= 1:
                continue
            newFeat = QgsFeature(fields)
            newFeat.setGeometry(vtxFlag)
            newFeat["flag"] = "O polígono está conectado incorretamente."
            point_flag_sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

    def linesBuffFrame(
        self,
        distSearch,
        dictLineInsideFrame,
        listLineBuffFrame,
        stepSizeLineInside,
        feed,
    ):
        for current, bboxLineDict in enumerate(dictLineInsideFrame):
            if feed.isCanceled():
                break
            if len(dictLineInsideFrame[bboxLineDict]) != 2:
                continue
            featLineInsideFrame = dictLineInsideFrame[bboxLineDict][0]
            geomLineInsideFrame = featLineInsideFrame.geometry()
            buffLineInsideFrame = geomLineInsideFrame.buffer(distSearch, -1)
            listLineBuffFrame.append(buffLineInsideFrame)

            feed.setProgress(current * stepSizeLineInside)

    def lineInsideFrame(
        self,
        explodeLinesLyr,
        lineFrameFeatDict,
        lineFrameSpatialIdx,
        dictLineInsideFrame,
        stepSizeLine,
        feed,
    ):
        for current, line in enumerate(explodeLinesLyr.getFeatures()):
            if feed.isCanceled():
                break
            geomLine = line.geometry()
            bboxLine = geomLine.boundingBox()
            for lineIntersectsId in lineFrameSpatialIdx.intersects(bboxLine):
                geomIntersects = lineFrameFeatDict[lineIntersectsId].geometry()
                if lineIntersectsId == line.id():
                    continue
                if geomIntersects.within(geomLine):
                    dictLineInsideFrame[bboxLine.asWktPolygon()].append(line)

            feed.setProgress(current * stepSizeLine)

    def vertexInLineFrame(
        self, stepSize, setVtxPolyFrame, dictLine, lineSpatialIndex, feed
    ):
        dictVtxFlag = dict()
        for current, vtx in enumerate(setVtxPolyFrame):
            dictVtxFlag[vtx.asWkt()] = set()
            if feed.isCanceled():
                break
            bboxVtx = vtx.boundingBox()
            for idL in lineSpatialIndex.intersects(bboxVtx):
                dictVtxFlag[vtx.asWkt()].add(idL)
            feed.setProgress(current * stepSize)
        return dictVtxFlag

    def verifyLigationPolygon(
        self,
        attributes,
        stepSize,
        dictExplodeLinePoly,
        dictLinePoly,
        fields,
        sink,
        feed,
    ):
        listLines = []
        newFeat = QgsFeature(fields)
        for current, bbGeomWkt in enumerate(dictLinePoly):
            if feed.isCanceled():
                break
            # listId = list(dictLinePoly[bbGeomWkt])
            for id in dictLinePoly[bbGeomWkt]:
                f = dictExplodeLinePoly[id]
                listLines.append(f)
            lenIdSet = len(dictLinePoly[bbGeomWkt])
            for featId in dictLinePoly[bbGeomWkt]:
                break
            featLine = dictExplodeLinePoly[featId]
            line = featLine.geometry()
            if lenIdSet == 1:
                newFeat.setGeometry(line)
                newFeat["Flag"] = "Polígonos não conectados corretamente."
                sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
            elif lenIdSet == 2:
                [id1, id2] = list(dictLinePoly[bbGeomWkt])
                feat1 = dictExplodeLinePoly[id1]
                feat2 = dictExplodeLinePoly[id2]
                msg = ""
                for attr in attributes:
                    if feat1[attr] == feat2[attr]:
                        continue
                    msg += f"{attr}, "
                if msg != "":
                    newFeat.setGeometry(line)
                    newFeat[
                        "Flag"
                    ] = f"Polígonos não possuem os atributos {msg[:len(msg)-2]} iguais."
                    sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
            else:
                newFeat.setGeometry(line)
                newFeat["Flag"] = "Mais de 2 polígonos conectados."
                sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

            feed.setProgress(current * stepSize)
        return listLines

    def dictBBoxWktId(
        self,
        listLineBuffFrame,
        stepSize,
        dictExplodeLinePoly,
        explodeLinePolySpatialIdx,
        feed,
    ):
        dictLinePoly = defaultdict(set)
        for current, line in enumerate(listLineBuffFrame):
            if feed.isCanceled():
                break
            bboxlineBuffFrame = line.boundingBox()
            for linePolyId in explodeLinePolySpatialIdx.intersects(bboxlineBuffFrame):
                linePoly = dictExplodeLinePoly[linePolyId]
                geomLinePoly = linePoly.geometry()
                if not geomLinePoly.within(line):
                    continue
                bbGeomLine = geomLinePoly.boundingBox()
                bbGeomLineWkt = bbGeomLine.asWktPolygon()
                dictLinePoly[bbGeomLineWkt].add(linePolyId)

            feed.setProgress(current * stepSize)
        return dictLinePoly

    def verticesPolyInFrame(
        self, listLineBuffFrame, stepSize, dictPolygon, polygonSpatialIdx, feed
    ):
        setVtxPolyFrame = set()
        dictVtxIdPoly = defaultdict(set)
        for current, lineFrame in enumerate(listLineBuffFrame):
            if feed.isCanceled():
                break
            bboxLine = lineFrame.boundingBox()
            for idPoly in polygonSpatialIdx.intersects(bboxLine):
                poly = dictPolygon[idPoly]
                geomPoly = poly.geometry()
                vtx = [v.asWkt() for v in geomPoly.vertices()]
                for vertex in vtx:
                    geomVertex = QgsGeometry.fromWkt(vertex)
                    if not geomVertex.within(lineFrame):
                        continue
                    setVtxPolyFrame.add(geomVertex)
                    dictVtxIdPoly[vertex].add(idPoly)

            feed.setProgress(current * stepSize)
        return setVtxPolyFrame

    def listAttributes(self, inputLinePolyLyr, inputLyrAttributes):
        listNameAttributes = list(inputLinePolyLyr.attributeAliases())
        attributes = []
        for attr in listNameAttributes:
            if attr in inputLyrAttributes:
                continue
            attributes.append(attr)
        return attributes

    def stepFeedback(self, multiStepFeedback, iterator):
        nSteps = len(iterator)
        stepSizeLineInside = 100 / nSteps
        feed = QgsProcessingMultiStepFeedback(nSteps, multiStepFeedback)
        return feed, stepSizeLineInside

    def stepFeedbackLyr(self, multiStepFeedback, explodeLinesLyr):
        nSteps = len([f for f in explodeLinesLyr.getFeatures()])
        stepSizeLine = 100 / nSteps
        feed = QgsProcessingMultiStepFeedback(nSteps, multiStepFeedback)
        return stepSizeLine, feed

    def idPolygonInFrame(self, listLineBuffFrame, polygonSpatialIdx):
        idPolyIn = set()
        for lineFrame in listLineBuffFrame:
            bboxLineFrame = lineFrame.boundingBox()
            for idPolyInter in polygonSpatialIdx.intersects(bboxLineFrame):
                idPolyIn.add(idPolyInter)
        return idPolyIn

    def removePolygonsTempLyr(self, tempPolyLyr, listPolyOut):
        tempPolyLyr.startEditing()
        tempPolyLyr.beginEditCommand("Filter Polygons")
        tempPolyLyr.deleteFeatures(listPolyOut)
        tempPolyLyr.commitChanges()

    def verticesInFrame(
        self,
        listLineBuffFrame,
        specifVertFeatDict,
        specifVertSpatialIdx,
        dictVertInFrame,
        stepSize,
        feed,
    ):
        for current, lineBuffFrame in enumerate(listLineBuffFrame):
            if feed.isCanceled():
                break
            bboxlineBuffFrame = lineBuffFrame.boundingBox()
            for vertId in specifVertSpatialIdx.intersects(bboxlineBuffFrame):
                geomVert = specifVertFeatDict[vertId].geometry()
                vertWkt = geomVert.asWkt()
                dictVertInFrame[vertWkt].append(specifVertFeatDict[vertId])

            feed.setProgress(current * stepSize)

    def verifyLine(self, feed, attributes, dictVertInFrame, stepSize, sink, fields):
        newFeat = QgsFeature(fields)
        for current, wktSpecifVert in enumerate(dictVertInFrame):
            if feed.isCanceled():
                break
            if len(dictVertInFrame[wktSpecifVert]) == 1:
                geomVertFlag = dictVertInFrame[wktSpecifVert][0].geometry()
                newFeat.setGeometry(geomVertFlag)
                newFeat["Flag"] = "Não há conexão na moldura"
                sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
            elif len(dictVertInFrame[wktSpecifVert]) == 2:
                [vertFeatOne, vertFeatTwo] = dictVertInFrame[wktSpecifVert]
                attrFeatOne = []
                attrFeatTwo = []
                for attributeName in attributes:
                    attrFeatOne.append(vertFeatOne[attributeName])
                    attrFeatTwo.append(vertFeatTwo[attributeName])
                if attrFeatOne == attrFeatTwo:
                    continue
                geomFeatOne = vertFeatOne.geometry()
                newFeat.setGeometry(geomFeatOne)
                newFeat["Flag"] = "Conectado com atributos diferentes"
                sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
            else:
                geomVertFlag = dictVertInFrame[wktSpecifVert][0].geometry()
                newFeat.setGeometry(geomVertFlag)
                newFeat["Flag"] = "Três ou mais vias conectadas"
                sink.addFeature(newFeat, QgsFeatureSink.FastInsert)

            feed.setProgress(current * stepSize)

    def spatialIndex(self, tempPolyLyr):
        dictPolygon = dict()
        idPolygon = set()
        polygonSpatialIdx = QgsSpatialIndex()
        for polygon in tempPolyLyr.getFeatures():
            idPolygon.add(polygon.id())
            dictPolygon[polygon.id()] = polygon
            polygonSpatialIdx.addFeature(polygon)
        return dictPolygon, idPolygon, polygonSpatialIdx

    def spatialIndexList(self, list):
        dictList = dict()
        listSpatialIdx = QgsSpatialIndex()
        for l in list:
            dictList[l.id()] = l
            listSpatialIdx.addFeature(l)
        return dictList, listSpatialIdx

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "verifyligation"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Verify Ligation")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate("VerifyLigation", string)

    def createInstance(self):
        return VerifyLigationAlgorithm()
