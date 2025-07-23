# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-08-15
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
import uuid
from typing import List, Optional, Tuple, Union

import processing
from qgis.core import (
    Qgis,
    QgsMapLayer,
    QgsProcessingContext,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingUtils,
    QgsVectorLayer,
    QgsFeedback,
    QgsRasterLayer,
    QgsRectangle,
    QgsCoordinateReferenceSystem,
    QgsProperty,
)


class AlgRunner:
    (
        Break,
        Snap,
        RmDangle,
        ChDangle,
        RmBridge,
        ChBridge,
        RmDupl,
        RmDac,
        BPol,
        Prune,
        RmArea,
        RmLine,
        RMSA,
    ) = range(13)
    (
        Intersects,
        Contains,
        Disjoint,
        Equals,
        Touches,
        Overlaps,
        Within,
        Crosses,
    ) = range(8)
    (
        AlignNodesInsertExtraVerticesWhereRequired,  # Prefer aligning nodes, insert extra vertices where required
        PreferClosestInsertExtraVerticesWhereRequired,  # Prefer closest point, insert extra vertices where required
        AlignNodesDoNotInsertNewVertices,  # Prefer aligning nodes, don't insert new vertices
        PreferClosestDoNotInsertNewVertices,  # Prefer closest point, don't insert new vertices
        MoveEndPointsOnlyPreferAligningNodes,  # Move end points only, prefer aligning nodes
        MoveEndPointsOnlyPreferClosestPoint,  # Move end points only,prefer closest point
        SnapEndPointsToEndPointsOnly,  # Snap end points to end points only
        SnapToAnchorNodes,  # Snap to anchor nodes (single layer only)
    ) = range(8)
    (
        FieldTypeDecimal,
        FieldTypeInteger,
        FieldTypeText,
        FieldTypeDate,
        FieldTypeTime,
        FieldTypeDateAndTime,
        FieldTypeBoolean,
        FieldTypeBlob,
        FieldTypeStringList,
        FieldTypeIntegerList,
        FieldTypeDecimalList,
    ) = range(11)

    def generateGrassOutputAndError(self):
        uuid_value = str(uuid.uuid4()).replace("-", "")
        output = QgsProcessingUtils.generateTempFilename(
            "output_{uuid}.shp".format(uuid=uuid_value)
        )
        error = QgsProcessingUtils.generateTempFilename(
            "error_{uuid}.shp".format(uuid=uuid_value)
        )
        return output, error

    def getGrassReturn(self, outputDict, context, returnError=False):
        lyr = QgsProcessingUtils.mapLayerFromString(outputDict["output"], context)
        if returnError:
            errorLyr = QgsProcessingUtils.mapLayerFromString(
                outputDict["error"], context
            )
            return lyr, errorLyr
        else:
            return lyr

    def runDissolve(
        self,
        inputLyr,
        context,
        feedback=None,
        outputLyr=None,
        field=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        field = [] if field is None else field
        parameters = {"INPUT": inputLyr, "FIELD": field, "OUTPUT": outputLyr}
        if Qgis.QGIS_VERSION_INT >= 32800:
            parameters["SEPARATE_DISJOINT"] = True
        output = processing.run(
            "native:dissolve",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runPoleOfInaccessibility(
        self,
        inputLyr,
        context,
        feedback=None,
        outputLyr=None,
        tolerance=1,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "TOLERANCE": tolerance, "OUTPUT": outputLyr}
        output = processing.run(
            "native:poleofinaccessibility",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runGrassDissolve(
        self,
        inputLyr,
        context,
        feedback=None,
        column=None,
        outputLyr=None,
        onFinish=None,
    ):
        """
        Runs dissolve from GRASS algorithm provider.
        :param inputLyr: (QgsVectorLayer) layer to be dissolved.
        :param context: (QgsProcessingContext) processing context.
        :param feedback: (QgsProcessingFeedback) QGIS object to keep track of progress/cancelling option.
        :param column: ()
        :param outputLyr: (str) URI to output layer.
        :param onFinish: (list-of-str) sequence of algs to be run after dissolve is executed, in execution order.
        :return: (QgsVectorLayer) dissolved (output) layer.
        """
        parameters = {
            "GRASS_MIN_AREA_PARAMETER": 0.0001,
            "GRASS_OUTPUT_TYPE_PARAMETER": 0,
            "GRASS_REGION_PARAMETER": None,
            "GRASS_SNAP_TOLERANCE_PARAMETER": -1,
            "GRASS_VECTOR_DSCO": "",
            "GRASS_VECTOR_EXPORT_NOCAT": False,
            "GRASS_VECTOR_LCO": "",
            "column": column,
            "input": inputLyr,
            "output": outputLyr
            or QgsProcessingUtils.generateTempFilename("output.shp"),
        }
        output = processing.run(
            "grass7:v.dissolve", parameters, onFinish, feedback, context
        )
        return self.getGrassReturn(output, context)

    def runDonutHoleExtractor(
        self,
        inputLyr,
        context,
        feedback=None,
        donuthole=None,
        outershell=None,
        selected=False,
        is_child_algorithm=False,
    ):
        donuthole = "memory:" if donuthole is None else donuthole
        outershell = "memory:" if outershell is None else outershell
        parameters = {
            "INPUT": inputLyr,
            "SELECTED": selected,
            "OUTERSHELL": outershell,
            "DONUTHOLE": donuthole,
        }
        output = processing.run(
            "dsgtools:donutholeextractor",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTERSHELL"], output["DONUTHOLE"]

    def runDeleteHoles(
        self, inputLyr, context, feedback=None, outputLyr=None, min_area=0
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "MIN_AREA": min_area, "OUTPUT": outputLyr}
        output = processing.run(
            "native:deleteholes", parameters, context=context, feedback=feedback
        )
        return output["OUTPUT"]

    def runOverlay(
        self,
        lyrA,
        lyrB,
        context,
        atype=0,
        btype=0,
        feedback=None,
        snap=0,
        operator=0,
        minArea=1e-8,
    ):
        output, _ = self.generateGrassOutputAndError()
        parameters = {
            "ainput": lyrA,
            "atype": atype,
            "binput": lyrB,
            "btype": btype,
            "operator": operator,
            "snap": snap,
            "-t": False,
            "output": output,
            "GRASS_REGION_PARAMETER": None,
            "GRASS_SNAP_TOLERANCE_PARAMETER": -1,
            "GRASS_MIN_AREA_PARAMETER": minArea,
            "GRASS_OUTPUT_TYPE_PARAMETER": 0,
            "GRASS_VECTOR_DSCO": "",
            "GRASS_VECTOR_LCO": "",
        }
        outputDict = processing.run(
            "grass7:v.overlay", parameters, context=context, feedback=feedback
        )
        return self.getGrassReturn(outputDict, context)

    def runClean(
        self,
        inputLyr,
        toolList,
        context,
        feedback=None,
        typeList=None,
        returnError=False,
        useFollowup=False,
        snap=None,
        minArea=None,
    ):
        snap = -1 if snap is None else snap
        minArea = 0.0001 if minArea is None else minArea
        typeList = [0, 1, 2, 3, 4, 5, 6] if typeList is None else typeList
        output, error = self.generateGrassOutputAndError()
        parameters = {
            "input": inputLyr,
            "type": typeList,
            "tool": toolList,
            "-b": False,
            "-c": useFollowup,
            "output": output,
            "error": error,
            "GRASS_REGION_PARAMETER": None,
            "GRASS_SNAP_TOLERANCE_PARAMETER": snap,
            "GRASS_MIN_AREA_PARAMETER": minArea,
            "GRASS_OUTPUT_TYPE_PARAMETER": 0,
            "GRASS_VECTOR_DSCO": "",
            "GRASS_VECTOR_LCO": "",
            "GRASS_VECTOR_EXPORT_NOCAT": False,
        }
        outputDict = processing.run(
            "grass7:v.clean", parameters, context=context, feedback=feedback
        )
        return self.getGrassReturn(outputDict, context, returnError=returnError)

    def runDsgToolsClean(
        self,
        inputLyr,
        context,
        feedback=None,
        onlySelected=False,
        snap=None,
        minArea=None,
        geographicBoundaryLyr=None,
        flags=None,
    ):
        snap = -1 if snap is None else snap
        minArea = 0.0001 if minArea is None else minArea
        flags = "memory:" if flags is None else flags
        parameters = {
            "INPUT": inputLyr,
            "SELECTED": onlySelected,
            "TOLERANCE": snap,
            "MINAREA": minArea,
            "GEOGRAPHIC_BOUNDARY": geographicBoundaryLyr,
            "FLAGS": flags,
        }
        output = processing.run(
            "dsgtools:cleangeometries", parameters, context=context, feedback=feedback
        )
        return inputLyr

    def runDouglasSimplification(
        self,
        inputLyr,
        threshold,
        context,
        feedback=None,
        snap=None,
        minArea=None,
        iterations=None,
        type=None,
        returnError=False,
        flags=None,
    ):
        """
        Runs simplify GRASS algorithm
        :param inputLyr: (QgsVectorLayer) layer, or layers, to be dissolved.
        :param method: (QgsProcessingParameterEnum) which algorithm would be
            used to simplify lines, in this case, Douglas-Peucker Algorithm.
        :param threshold: (QgsProcessingParameterNumber) give in map units.
            For latitude-longitude locations give in decimal degree.
        :param context: (QgsProcessingContext) processing context.
        :param feedback: (QgsProcessingFeedback) QGIS object to keep track of
            progress/cancelling option.
        :param onlySelected: (QgsProcessingParameterBoolean) process only
            selected features.
        :param outputLyr: (str) URI to output layer.
        :return: (QgsVectorLayer) simplified output layer or layers.
        """
        snap = -1 if snap is None else snap
        minArea = 0.0001 if minArea is None else minArea
        iterations = 1 if iterations is None else iterations
        flags = "memory:" if flags is None else flags
        algType = [0, 1, 2] if type is None else type
        output, error = self.generateGrassOutputAndError()
        parameters = {
            "input": inputLyr,
            "type": algType,
            "cats": "",
            "where": "",
            "method": 0,
            "threshold": threshold,
            "look_ahead": 7,
            "reduction": 50,
            "slide": 0.5,
            "angle_thresh": 3,
            "degree_thresh": 0,
            "closeness_thresh": 0,
            "betweeness_thresh": 0,
            "alpha": 1,
            "beta": 1,
            "iterations": iterations,
            "-t": False,
            "-l": True,
            "output": output,
            "error": error,
            "GRASS_REGION_PARAMETER": None,
            "GRASS_SNAP_TOLERANCE_PARAMETER": snap,
            "GRASS_MIN_AREA_PARAMETER": minArea,
            "GRASS_OUTPUT_TYPE_PARAMETER": 0,
            "GRASS_VECTOR_DSCO": "",
            "GRASS_VECTOR_LCO": "",
        }
        outputDict = processing.run(
            "grass7:v.generalize", parameters, context=context, feedback=feedback
        )
        return self.getGrassReturn(outputDict, context, returnError=returnError)

    def runIdentifyDuplicatedGeometries(
        self, inputLyr, context, feedback=None, flagLyr=None, onlySelected=False
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        parameters = {"INPUT": inputLyr, "SELECTED": onlySelected, "FLAGS": flagLyr}
        output = processing.run(
            "dsgtools:identifyduplicatedgeometries",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["FLAGS"]

    def runIdentifyDuplicatedFeatures(
        self,
        inputLyr,
        context,
        onlySelected=False,
        attributeBlackList=None,
        excludePrimaryKeys=True,
        ignoreVirtualFields=True,
        feedback=None,
        flagLyr=None,
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        parameters = {
            "INPUT": inputLyr,
            "SELECTED": onlySelected,
            "FLAGS": flagLyr,
            "ATTRIBUTE_BLACK_LIST": attributeBlackList,
            "IGNORE_VIRTUAL_FIELDS": ignoreVirtualFields,
            "IGNORE_PK_FIELDS": excludePrimaryKeys,
        }
        output = processing.run(
            "dsgtools:identifyduplicatedfeatures",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["FLAGS"]

    def runIdentifySmallLines(
        self, inputLyr, tol, context, feedback=None, flagLyr=None, onlySelected=False
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        parameters = {
            "INPUT": inputLyr,
            "TOLERANCE": tol,
            "SELECTED": onlySelected,
            "FLAGS": flagLyr,
        }
        output = processing.run(
            "dsgtools:identifysmalllines",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["FLAGS"]
    
    def runRemoveSmallLines(
        self, inputLyr, tol, context, feedback=None, flagLyr=None, onlySelected=False
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        parameters = {
            "INPUT": inputLyr,
            "TOLERANCE": tol,
            "SELECTED": onlySelected,
        }
        output = processing.run(
            "dsgtools:removesmalllines",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["FLAGS"]

    def runIdentifySmallPolygons(
        self, inputLyr, tol, context, feedback=None, flagLyr=None, onlySelected=False
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        parameters = {
            "INPUT": inputLyr,
            "TOLERANCE": tol,
            "SELECTED": onlySelected,
            "FLAGS": flagLyr,
        }
        output = processing.run(
            "dsgtools:identifysmallpolygons",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["FLAGS"]

    def runSnapGeometriesToLayer(
        self,
        inputLayer,
        referenceLayer,
        tol,
        context,
        feedback=None,
        behavior=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        behavior = 0 if behavior is None else behavior
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLayer,
            "REFERENCE_LAYER": referenceLayer,
            "TOLERANCE": tol,
            "BEHAVIOR": behavior,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "qgis:snapgeometries",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSnapLayerOnLayer(
        self,
        inputLayer,
        referenceLayer,
        tol,
        context,
        onlySelected=False,
        feedback=None,
        behavior=None,
        buildCache=False,
        is_child_algorithm=False,
    ):
        behavior = 0 if behavior is None else behavior
        parameters = {
            "INPUT": inputLayer,
            "SELECTED": onlySelected,
            "REFERENCE_LAYER": referenceLayer,
            "TOLERANCE": tol,
            "BEHAVIOR": behavior,
            "BUILD_CACHE": buildCache,
        }
        output = processing.run(
            "dsgtools:snaplayeronlayer",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return inputLayer

    def runIdentifyDangles(
        self,
        inputLayer,
        searchRadius,
        context,
        feedback=None,
        onlySelected=False,
        lineFilter=None,
        polygonFilter=None,
        ignoreDanglesOnUnsegmentedLines=False,
        inputIsBoundaryLayer=False,
        geographicBoundsLyr=None,
        flagLyr=None,
        returnProcessingDict=False,
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        lineFilter = [] if lineFilter is None else lineFilter
        polygonFilter = [] if polygonFilter is None else polygonFilter
        parameters = {
            "INPUT": inputLayer,
            "SELECTED": onlySelected,
            "TOLERANCE": searchRadius,
            "LINEFILTERLAYERS": lineFilter,
            "POLYGONFILTERLAYERS": polygonFilter,
            "IGNORE_DANGLES_ON_UNSEGMENTED_LINES": ignoreDanglesOnUnsegmentedLines,
            "INPUT_IS_BOUDARY_LAYER": inputIsBoundaryLayer,
            "GEOGRAPHIC_BOUNDARY": geographicBoundsLyr,
            "FLAGS": flagLyr,
        }
        output = processing.run(
            "dsgtools:identifydangles", parameters, context=context, feedback=feedback
        )
        return output if returnProcessingDict else output["FLAGS"]

    def runSnapToGrid(self, inputLayer, tol, context, feedback=None, outputLyr=None):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLayer,
            "HSPACING": tol,
            "VSPACING": tol,
            "ZSPACING": 0,
            "MSPACING": 0,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "native:snappointstogrid", parameters, context=context, feedback=feedback
        )
        return output["OUTPUT"]

    def runRemoveNull(self, inputLayer, context, feedback=None, outputLyr=None):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:removenullgeometries",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runClip(
        self,
        inputLayer,
        overlayLayer,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLayer, "OVERLAY": overlayLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:clip",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSymDiff(
        self,
        inputLayer,
        overlayLayer,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLayer, "OVERLAY": overlayLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:symmetricaldifference",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runBoundary(
        self,
        inputLayer,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:boundary",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runMultipartToSingleParts(
        self,
        inputLayer,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:multiparttosingleparts",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runPromoteToMulti(
        self,
        inputLayer,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:promotetomulti",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runBuffer(
        self,
        inputLayer,
        distance,
        context,
        dissolve=False,
        endCapStyle=None,
        joinStyle=None,
        segments=None,
        mitterLimit=None,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        endCapStyle = 0 if endCapStyle is None else endCapStyle
        joinStyle = 0 if joinStyle is None else joinStyle
        segments = 5 if segments is None else segments
        mitterLimit = 2 if mitterLimit is None else mitterLimit
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLayer,
            "DISTANCE": distance,
            "DISSOLVE": dissolve,
            "END_CAP_STYLE": endCapStyle,
            "JOIN_STYLE": joinStyle,
            "SEGMENTS": segments,
            "MITER_LIMIT": mitterLimit,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "native:buffer",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runIntersection(
        self,
        inputLyr,
        context,
        inputFields=None,
        outputLyr=None,
        overlayLyr=None,
        overlayFields=None,
        feedback=None,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        inputFields = [] if inputFields is None else inputFields
        overlayFields = [] if overlayFields is None else overlayFields
        parameters = {
            "INPUT": inputLyr,
            "INPUT_FIELDS": inputFields,
            "OUTPUT": outputLyr,
            "OVERLAY": overlayLyr,
            "OVERLAY_FIELDS": overlayFields,
        }
        output = processing.run(
            "native:intersection", parameters, context=context, feedback=feedback
        )
        return output["OUTPUT"]

    def runUnion(
        self,
        inputLyr,
        context,
        inputFields=None,
        outputLyr=None,
        overlayLyr=None,
        overlayFields=None,
        feedback=None,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        inputFields = [] if inputFields is None else inputFields
        overlayFields = [] if overlayFields is None else overlayFields
        parameters = {
            "INPUT": inputLyr,
            "INPUT_FIELDS": inputFields,
            "OUTPUT": outputLyr,
            "OVERLAY": overlayLyr,
            "OVERLAY_FIELDS": overlayFields,
        }
        output = processing.run(
            "native:union", parameters, context=context, feedback=feedback
        )
        return output["OUTPUT"]

    def runFilterExpression(
        self,
        inputLyr,
        expression,
        context,
        outputLyr=None,
        feedback=None,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"EXPRESSION": expression, "INPUT": inputLyr, "OUTPUT": outputLyr}
        output = processing.run(
            "native:extractbyexpression",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runFilterExpressionWithFailOutput(
        self,
        inputLyr,
        expression,
        context,
        outputLyr=None,
        failOutputLyr=None,
        feedback=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        failOutputLyr = "memory:" if failOutputLyr is None else failOutputLyr
        parameters = {
            "EXPRESSION": expression,
            "INPUT": inputLyr,
            "OUTPUT": outputLyr,
            "FAIL_OUTPUT": failOutputLyr,
        }
        output = processing.run(
            "native:extractbyexpression",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"], output["FAIL_OUTPUT"]

    def runRemoveDuplicatedFeatures(
        self,
        inputLyr,
        context,
        onlySelected=False,
        attributeBlackList=None,
        excludePrimaryKeys=True,
        ignoreVirtualFields=True,
        feedback=None,
        outputLyr=None,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        parameters = {
            "INPUT": inputLyr,
            "SELECTED": onlySelected,
            "FLAGS": outputLyr,
            "ATTRIBUTE_BLACK_LIST": attributeBlackList,
            "IGNORE_VIRTUAL_FIELDS": ignoreVirtualFields,
            "IGNORE_PK_FIELDS": excludePrimaryKeys,
        }
        output = processing.run(
            "dsgtools:removeduplicatedfeatures",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["FLAGS"]

    def runApplStylesFromDatabaseToLayers(
        self, inputList, context, styleName, feedback=None, outputLyr=None
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT_LAYERS": inputList,
            "STYLE_NAME": styleName,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "dsgtools:applystylesfromdatabasetolayersalgorithm",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runMatchAndApplyQmlStylesToLayer(
        self, inputList, context, qmlFolder, feedback=None, outputLyr=None
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT_LAYERS": inputList,
            "QML_FOLDER": qmlFolder,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "dsgtools:matchandapplyqmlstylestolayersalgorithm",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runAddAutoIncrementalField(
        self,
        inputLyr,
        context,
        feedback=None,
        outputLyr=None,
        fieldName=None,
        start=1,
        sortAscending=True,
        sortNullsFirst=False,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        fieldName = "featid" if fieldName is None else fieldName
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLyr,
            "FIELD_NAME": fieldName,
            "START": start,
            "GROUP_FIELDS": [],
            "SORT_EXPRESSION": "",
            "SORT_ASCENDING": sortAscending,
            "SORT_NULLS_FIRST": sortNullsFirst,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "native:addautoincrementalfield",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runPolygonsToLines(
        self, inputLyr, context, feedback=None, outputLyr=None, is_child_algorithm=False
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "OUTPUT": outputLyr}
        output = processing.run(
            "native:polygonstolines"
            if Qgis.QGIS_VERSION_INT >= 30600
            else "qgis:polygonstolines",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runExtractVertices(
        self, inputLyr, context, feedback=None, outputLyr=None, is_child_algorithm=False
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "OUTPUT": outputLyr}
        output = processing.run(
            "native:extractvertices",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runExplodeLines(
        self, inputLyr, context, feedback=None, outputLyr=None, is_child_algorithm=False
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "OUTPUT": outputLyr}
        output = processing.run(
            "native:explodelines",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runMergeVectorLayers(
        self,
        inputList,
        context,
        feedback=None,
        outputLyr=None,
        crs=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"LAYERS": inputList, "CRS": crs, "OUTPUT": outputLyr}
        output = processing.run(
            "native:mergevectorlayers",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSaveSelectedFeatures(self, inputLyr, context, feedback=None, outputLyr=None):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "OUTPUT": outputLyr}
        output = processing.run(
            "native:saveselectedfeatures",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runReprojectLayer(self, layer, targetCrs, output=None, context=None, feedback=None, is_child_algorithm=False):
        """
        Reprojects layer's CRS.
        :param : (QgsVectorLayer) layer to be reprojected.
        :param targetCrs: (QgsCoordinateReferenceSystem) CRS object for the
                          output layer.
        :param output: (QgsVectorLayer) layer accomodate reprojected layer.
        :param context: (QgsProcessingContext) processing context in which algorithm
                    should be executed.
        :param feedback: (QgsFeedback) QGIS progress tracking component.
        :return: (QgsVectorLayer) reprojected layer.
        """
        return processing.run(
            "native:reprojectlayer",
            {"INPUT": layer, "OUTPUT": output or "memory:", "TARGET_CRS": targetCrs},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )["OUTPUT"]

    def runPointOnSurface(
        self,
        inputLyr,
        context,
        allParts=True,
        feedback=None,
        outputLyr=None,
        onlySelected=False,
        is_child_algorithm=True,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "ALL_PARTS": allParts, "OUTPUT": outputLyr}
        output = processing.run(
            "native:pointonsurface",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runRemoveDuplicatedGeometries(
        self, inputLyr, context, feedback=None, outputLyr=None, onlySelected=False
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLyr,
            "SELECTED": onlySelected,
            "FLAGS": "memory:",
        }
        output = processing.run(
            "dsgtools:removeduplicatedgeometries",
            parameters,
            context=context,
            feedback=feedback,
        )
        return inputLyr

    def runPolygonize(
        self,
        inputLyr,
        context,
        keepFields=False,
        feedback=None,
        outputLyr=None,
        onlySelected=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": inputLyr, "KEEP_FIELDS": keepFields, "OUTPUT": outputLyr}
        output = processing.run(
            "qgis:polygonize", parameters, context=context, feedback=feedback
        )
        return output["OUTPUT"]

    def runJoinAttributesByLocation(
        self,
        inputLyr: QgsVectorLayer,
        joinLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        predicateList: Optional[List[int]] = None,
        joinFields: Optional[List[str]] = None,
        method: Optional[int] = None,
        discardNonMatching: Optional[bool] = True,
        prefix: Optional[str] = None,
        feedback: Optional[QgsFeedback] = None,
        outputLyr: Optional[QgsVectorLayer] = None,
        unjoinnedLyr: Optional[QgsVectorLayer] = None,
        returnUnjoinned: Optional[bool] = False,
        is_child_algorithm: Optional[bool] = False,
    ) -> QgsVectorLayer:
        predicateList = [0] if predicateList is None else predicateList
        joinFields = [] if joinFields is None else joinFields
        method = 0 if method is None else method
        outputLyr = "memory:" if outputLyr is None else outputLyr
        prefix = "" if prefix is None else prefix
        parameters = {
            "INPUT": inputLyr,
            "JOIN": joinLyr,
            "PREDICATE": predicateList,
            "JOIN_FIELDS": joinFields,
            "METHOD": method,
            "DISCARD_NONMATCHING": discardNonMatching,
            "PREFIX": prefix,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "qgis:joinattributesbylocation",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runLineIntersections(
        self,
        inputLyr,
        intersectLyr,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLyr,
            "INTERSECT": intersectLyr,
            "INPUT_FIELDS": [],
            "INTERSECT_FIELDS": [],
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "native:lineintersections",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runStatisticsByCategories(
        self,
        inputLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        valuesFieldName: Optional[str] = None,
        categoriesFieldName: str = None,
        feedback: Optional[QgsProcessingContext] = None,
        outputLyr: Optional[QgsVectorLayer] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLyr,
            "VALUES_FIELD_NAME": "" if valuesFieldName is None else valuesFieldName,
            "CATEGORIES_FIELD_NAME": []
            if categoriesFieldName is None
            else categoriesFieldName,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "qgis:statisticsbycategories",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSplitLinesWithLines(
        self,
        inputLyr: QgsVectorLayer,
        linesLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: Optional[QgsFeedback] = None,
        onlySelected: Optional[bool] = False,
        outputLyr: Optional[QgsVectorLayer] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> Union[QgsVectorLayer, str]:
        inputLyr = (
            QgsProcessingUtils.mapLayerFromString(inputLyr, context)
            if isinstance(inputLyr, str)
            else inputLyr
        )
        usedInput = (
            inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True)
        )
        linesLyr = (
            QgsProcessingUtils.mapLayerFromString(linesLyr, context)
            if isinstance(linesLyr, str)
            else linesLyr
        )
        usedLines = (
            linesLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(linesLyr.id(), True)
        )
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {"INPUT": usedInput, "LINES": usedLines, "OUTPUT": outputLyr}
        output = processing.run(
            "native:splitwithlines",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runAggregate(
        self,
        inputLyr,
        context,
        groupBy=None,
        aggregates=None,
        feedback=None,
        outputLyr=None,
        onlySelected=False,
        is_child_algorithm=False,
    ):
        groupBy = "NULL" if groupBy is None else groupBy
        aggregates = [] if aggregates is None else aggregates
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLyr,
            "GROUP_BY": groupBy,
            "AGGREGATES": aggregates,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "qgis:aggregate",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDeaggregate(self, inputLyr, context, feedback=None, onlySelected=False):
        parameters = {"INPUT": inputLyr, "SELECTED": onlySelected}
        output = processing.run(
            "dsgtools:deaggregategeometries",
            parameters,
            context=context,
            feedback=feedback,
        )
        return inputLyr

    def runCreateSpatialIndex(
        self, inputLyr, context, feedback=None, is_child_algorithm=True
    ):
        processing.run(
            "native:createspatialindex",
            {"INPUT": inputLyr},
            feedback=feedback,
            context=context,
            is_child_algorithm=is_child_algorithm,
        )
        return None

    def runExtractByLocation(
        self,
        inputLyr,
        intersectLyr,
        context,
        predicate=None,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        predicate = [0] if predicate is None else predicate
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:extractbylocation",
            {
                "INPUT": inputLyr,
                "INTERSECT": intersectLyr,
                "PREDICATE": predicate,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runCreateFieldWithExpression(
        self,
        inputLyr,
        expression,
        fieldName,
        context,
        fieldType=0,
        fieldLength=1000,
        fieldPrecision=0,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:fieldcalculator",
            {
                "INPUT": inputLyr,
                "FIELD_NAME": fieldName,
                "FIELD_TYPE": fieldType,
                "FIELD_LENGTH": fieldLength,
                "FORMULA": expression,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runStringCsvToLayerList(self, stringCSV, context, feedback=None):
        output = processing.run(
            "dsgtools:stringcsvtolayerlistalgorithm",
            {"INPUTLAYERS": stringCSV, "OUTPUT": "memory:"},
            context=context,
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runClipRasterLayer(
        self,
        inputRaster: QgsRasterLayer,
        mask: QgsRasterLayer,
        context: QgsProcessingContext,
        sourceCrs: Optional[QgsCoordinateReferenceSystem] = None,
        targetCrs: Optional[QgsCoordinateReferenceSystem] = None,
        nodata: Optional[int] = None,
        options: Optional[str] = None,
        outputRaster: Optional[QgsRasterLayer] = None,
        xResolution: Optional[float] = None,
        yResolution: Optional[float] = None,
        setResolution: Optional[bool] = False,
        keepResolution: Optional[bool] = False,
        cropToCutline: Optional[bool] = True,
        alphaBand: Optional[bool] = False,
        dataType: Optional[int] = 0,
        multiThreading: Optional[bool] = False,
        targetExtent: Optional[list] = None,
        extra: Optional[str] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: Optional[bool] = False,
    ):
        outputRaster = "TEMPORARY_OUTPUT" if outputRaster is None else outputRaster
        options = "" if options is None else options
        extra = "" if extra is None else extra
        output = processing.run(
            "gdal:cliprasterbymasklayer",
            {
                "INPUT": inputRaster,
                "MASK": mask,
                "SOURCE_CRS": sourceCrs,
                "TARGET_CRS": targetCrs,
                "TARGET_EXTENT": targetExtent,
                "NODATA": nodata,
                "ALPHA_BAND": alphaBand,
                "CROP_TO_CUTLINE": cropToCutline,
                "KEEP_RESOLUTION": keepResolution,
                "SET_RESOLUTION": setResolution,
                "X_RESOLUTION": xResolution,
                "Y_RESOLUTION": yResolution,
                "MULTITHREADING": multiThreading,
                "OPTIONS": options,
                "DATA_TYPE": dataType,
                "EXTRA": extra,
                "OUTPUT": outputRaster,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runGrassMapCalcSimple(
        self,
        inputA,
        expression,
        context,
        feedback=None,
        inputB=None,
        inputC=None,
        inputD=None,
        inputE=None,
        inputF=None,
        outputRaster=None,
    ):
        outputRaster = "TEMPORARY_OUTPUT" if outputRaster is None else outputRaster
        output = processing.run(
            "grass7:r.mapcalc.simple",
            {
                "a": inputA,
                "b": inputB,
                "c": inputC,
                "d": inputD,
                "e": inputE,
                "f": inputF,
                "expression": expression,
                "output": outputRaster,
                "GRASS_REGION_PARAMETER": None,
                "GRASS_REGION_CELLSIZE_PARAMETER": 0,
                "GRASS_RASTER_FORMAT_OPT": "",
                "GRASS_RASTER_FORMAT_META": "",
            },
            context=context,
            feedback=feedback,
        )
        return output["output"]

    def runGrassReclass(
        self, inputRaster, expression, context, feedback=None, outputRaster=None
    ):
        outputRaster = "TEMPORARY_OUTPUT" if outputRaster is None else outputRaster
        output = processing.run(
            "grass7:r.reclass",
            {
                "input": inputRaster,
                "rules": "",
                "txtrules": expression,
                "output": outputRaster,
                "GRASS_REGION_PARAMETER": None,
                "GRASS_REGION_CELLSIZE_PARAMETER": 0,
                "GRASS_RASTER_FORMAT_OPT": "",
                "GRASS_RASTER_FORMAT_META": "",
            },
            context=context,
            feedback=feedback,
        )
        return output["output"]

    def runSieve(
        self,
        inputRaster,
        threshold,
        context,
        eightConectedness=False,
        feedback=None,
        outputRaster=None,
    ):
        outputRaster = "TEMPORARY_OUTPUT" if outputRaster is None else outputRaster
        output = processing.run(
            "gdal:sieve",
            {
                "INPUT": inputRaster,
                "THRESHOLD": threshold,
                "EIGHT_CONNECTEDNESS": eightConectedness,
                "NO_MASK": False,
                "MASK_LAYER": None,
                "EXTRA": "",
                "OUTPUT": outputRaster,
            },
            context=context,
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runChaikenSmoothing(
        self,
        inputLyr,
        threshold,
        context,
        feedback=None,
        snap=None,
        minArea=None,
        iterations=None,
        type=None,
        returnError=False,
        flags=None,
        is_child_algorithm=False,
    ):
        """
        Runs simplify GRASS algorithm
        :param inputLyr: (QgsVectorLayer) layer, or layers, to be dissolved.
        :param method: (QgsProcessingParameterEnum) which algorithm would be
            used to simplify lines, in this case, Douglas-Peucker Algorithm.
        :param threshold: (QgsProcessingParameterNumber) give in map units.
            For latitude-longitude locations give in decimal degree.
        :param context: (QgsProcessingContext) processing context.
        :param feedback: (QgsProcessingFeedback) QGIS object to keep track of
            progress/cancelling option.
        :param onlySelected: (QgsProcessingParameterBoolean) process only
            selected features.
        :param outputLyr: (str) URI to output layer.
        :return: (QgsVectorLayer) simplified output layer or layers.
        """
        snap = -1 if snap is None else snap
        minArea = 0.0001 if minArea is None else minArea
        iterations = 1 if iterations is None else iterations
        flags = "memory:" if flags is None else flags
        algType = [0, 1, 2] if type is None else type
        output, error = self.generateGrassOutputAndError()
        parameters = {
            "input": inputLyr,
            "type": algType,
            "cats": "",
            "where": "",
            "method": 8,
            "threshold": threshold,
            "look_ahead": 7,
            "reduction": 50,
            "slide": 0.5,
            "angle_thresh": 3,
            "degree_thresh": 0,
            "closeness_thresh": 0,
            "betweeness_thresh": 0,
            "alpha": 1,
            "beta": 1,
            "iterations": iterations,
            "-t": False,
            "-l": True,
            "output": output,
            "error": error,
            "GRASS_REGION_PARAMETER": None,
            "GRASS_SNAP_TOLERANCE_PARAMETER": snap,
            "GRASS_MIN_AREA_PARAMETER": minArea,
            "GRASS_OUTPUT_TYPE_PARAMETER": 0,
            "GRASS_VECTOR_DSCO": "",
            "GRASS_VECTOR_LCO": "",
        }
        outputDict = processing.run(
            "grass7:v.generalize",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return self.getGrassReturn(outputDict, context, returnError=returnError)

    def runGdalPolygonize(
        self,
        inputRaster,
        context,
        band=1,
        field=None,
        eightConectedness=False,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "TEMPORARY_OUTPUT" if outputLyr is None else outputLyr
        field = "DN" if field is None else field
        output = processing.run(
            "gdal:polygonize",
            {
                "INPUT": inputRaster,
                "BAND": band,
                "FIELD": field,
                "EIGHT_CONNECTEDNESS": eightConectedness,
                "EXTRA": "",
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runExtractSpecificVertices(
        self,
        inputLyr,
        vertices,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:extractspecificvertices",
            {
                "INPUT": inputLyr,
                "VERTICES": vertices,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runCreateGrid(
        self,
        extent,
        crs,
        hSpacing,
        vSpacing,
        context,
        type=2,
        feedback=None,
        outputLyr=None,
        hOverlay=0,
        vOverlay=0,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:creategrid",
            {
                "TYPE": type,
                "EXTENT": extent,
                "HSPACING": hSpacing,
                "VSPACING": vSpacing,
                "HOVERLAY": hOverlay,
                "VOVERLAY": vOverlay,
                "CRS": crs,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runExtendLines(
        self,
        inputLyr,
        startDistance,
        endDistance,
        context,
        feedback=None,
        outputLyr=None,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:extendlines",
            {
                "INPUT": inputLyr,
                "START_DISTANCE": startDistance,
                "END_DISTANCE": endDistance,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
        )
        return output["OUTPUT"]

    def runIdentifyUnsharedVertexOnIntersectionsAlgorithm(
        self,
        pointLayerList,
        lineLayerList,
        polygonLayerList,
        context,
        onlySelected=False,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:identifyunsharedvertexonintersectionsalgorithm",
            {
                "INPUT_POINTS": pointLayerList,
                "INPUT_LINES": lineLayerList,
                "INPUT_POLYGONS": polygonLayerList,
                "SELECTED": onlySelected,
                "FLAGS": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["FLAGS"]

    def runIdentifyUnsharedVertexOnSharedEdgesAlgorithm(
        self,
        lineLayerList,
        polygonLayerList,
        searchRadius,
        context,
        onlySelected=False,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:identifyunsharedvertexonsharededgesalgorithm",
            {
                "INPUT_LINES": lineLayerList,
                "INPUT_POLYGONS": polygonLayerList,
                "SELECTED": onlySelected,
                "SEARCH_RADIUS": searchRadius,
                "FLAGS": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["FLAGS"]

    def runShortestLine(
        self,
        sourceLayer,
        destinationLayer,
        context,
        method=0,
        neighbors=1,
        maxDistance=None,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:shortestline",
            {
                "SOURCE": sourceLayer,
                "DESTINATION": destinationLayer,
                "METHOD": method,
                "NEIGHBORS": neighbors,
                "DISTANCE": maxDistance,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runRetainFields(
        self,
        inputLayer,
        fields,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:retainfields",
            {"INPUT": inputLayer, "FIELDS": fields, "OUTPUT": "TEMPORARY_OUTPUT"},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runExtractByExtent(
        self,
        inputLayer,
        extent,
        context,
        clip=True,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:extractbyextent",
            {
                "INPUT": inputLayer,
                "EXTENT": extent,
                "CLIP": clip,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSelectByLocation(
        self,
        inputLyr,
        intersectLyr,
        context,
        predicate=None,
        method=None,
        feedback=None,
        is_child_algorithm=False,
    ):
        predicate = [0] if predicate is None else predicate
        method = [0] if method is None else method
        processing.run(
            "native:selectbylocation",
            {
                "INPUT": inputLyr,
                "INTERSECT": intersectLyr,
                "PREDICATE": predicate,
                "METHOD": method,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )

    def extractWithinDistance(
        self,
        inputLyr,
        referenceLyr,
        distance,
        context,
        outputLyr=None,
        feedback=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:extractwithindistance",
            {
                "INPUT": inputLyr,
                "REFERENCE": referenceLyr,
                "DISTANCE": distance,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runUnbuildPolygons(
        self,
        inputPolygonList,
        context,
        onlySelected=False,
        lineConstraintLayerList=None,
        polygonConstraintLayerList=None,
        geographicBoundary=None,
        feedback=None,
        outputCenterPointsLyr=None,
        outputBoundariesLyr=None,
        is_child_algorithm=False,
    ):
        lineConstraintLayerList = (
            [] if lineConstraintLayerList is None else lineConstraintLayerList
        )
        polygonConstraintLayerList = (
            [] if polygonConstraintLayerList is None else polygonConstraintLayerList
        )
        outputCenterPointsLyr = (
            "memory:" if outputCenterPointsLyr is None else outputCenterPointsLyr
        )
        outputBoundariesLyr = (
            "memory:" if outputBoundariesLyr is None else outputBoundariesLyr
        )
        output = processing.run(
            "dsgtools:unbuildpolygonsalgorithm",
            {
                "INPUT_POLYGONS": inputPolygonList,
                "SELECTED": onlySelected,
                "CONSTRAINT_LINE_LAYERS": lineConstraintLayerList,
                "CONSTRAINT_POLYGON_LAYERS": polygonConstraintLayerList,
                "GEOGRAPHIC_BOUNDARY": geographicBoundary,
                "OUTPUT_CENTER_POINTS": outputCenterPointsLyr,
                "OUTPUT_BOUNDARIES": outputBoundariesLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT_CENTER_POINTS"], output["OUTPUT_BOUNDARIES"]

    def runJoinByLocationSummary(
        self,
        inputLyr,
        joinLyr,
        predicateList,
        joinFields,
        summaries,
        context,
        discardNonMatching=True,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        predicateList = [0] if predicateList is None else predicateList
        joinFields = [] if joinFields is None else joinFields
        summaries = [] if summaries is None else summaries
        outputLyr = "memory:" if outputLyr is None else outputLyr
        parameters = {
            "INPUT": inputLyr,
            "PREDICATE": predicateList,
            "JOIN": joinLyr,
            "JOIN_FIELDS": joinFields,
            "SUMMARIES": summaries,
            "DISCARD_NONMATCHING": discardNonMatching,
            "PREFIX": "",
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "qgis:joinbylocationsummary",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runRefactorFields(
        self,
        inputLayer,
        fieldmap: List[dict],
        context,
        feedback=None,
        onlySelected=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        inputLayer = (
            QgsProcessingUtils.mapLayerFromString(inputLayer, context)
            if isinstance(inputLayer, str)
            else inputLayer
        )
        parameters = {
            "INPUT": QgsProcessingFeatureSourceDefinition(
                inputLayer.source(), selectedFeaturesOnly=onlySelected
            ),
            "FIELDS_MAPPING": fieldmap,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "native:refactorfields",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDifference(
        self,
        inputLyr: QgsVectorLayer,
        overlayLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        gridSize: Optional[float] = None,
        outputLyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:difference",
            {
                "INPUT": inputLyr,
                "OVERLAY": overlayLyr,
                "OUTPUT": outputLyr,
                "GRID_SIZE": gridSize,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runIdentifyLoops(
        self,
        inputLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        buildLocalCache: bool = False,
        outputLyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:identifydrainageloops",
            {
                "INPUT": inputLyr,
                "BUILD_CACHE": buildLocalCache,
                "FLAGS": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["FLAGS"]

    def runIdentifyDrainageFlowIssues(
        self,
        inputLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ):
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:identifydrainageflowissues",
            {
                "INPUT": inputLyr,
                "FLAGS": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["FLAGS"]

    def runIdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm(
        self,
        inputDrainagesLayer: QgsVectorLayer,
        context: QgsProcessingContext,
        waterBodyLayer: Optional[QgsVectorLayer] = None,
        waterBodyWithFlowExpression: Optional[str] = None,
        waterBodyWithoutFlowExpression: Optional[str] = None,
        oceanFilterExpression: Optional[str] = None,
        sinkAndSpillwayLayer: Optional[QgsVectorLayer] = None,
        sinkFilterExpression: Optional[str] = None,
        spillwayFilterExpression: Optional[str] = None,
        geographicBoundsLayer: Optional[QgsVectorLayer] = None,
        outputPointLyr: Optional[QgsVectorLayer] = None,
        outputLineLyr: Optional[QgsVectorLayer] = None,
        outputPolygonyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> Tuple[QgsVectorLayer, QgsVectorLayer, QgsVectorLayer]:
        outputPointLyr = "memory:" if outputPointLyr is None else outputPointLyr
        outputLineLyr = "memory:" if outputLineLyr is None else outputLineLyr
        outputPolygonyr = "memory:" if outputPolygonyr is None else outputPolygonyr
        output = processing.run(
            "dsgtools:identifydrainageflowissueswithhydrographyelementsalgorithm",
            {
                "INPUT_DRAINAGES": inputDrainagesLayer,
                "WATER_BODY_LAYER": waterBodyLayer,
                "WATER_BODY_WITH_FLOW_FILTER_EXPRESSION": waterBodyWithFlowExpression,
                "WATER_BODY_WITHOUT_FLOW_FILTER_EXPRESSION": waterBodyWithoutFlowExpression,
                "OCEAN_FILTER_EXPRESSION": oceanFilterExpression,
                "SINK_AND_SPILLWAY_LAYER": sinkAndSpillwayLayer,
                "SINK_FILTER_EXPRESSION": sinkFilterExpression,
                "SPILLWAY_FILTER_EXPRESSION": spillwayFilterExpression,
                "GEOGRAPHIC_BOUNDARY": geographicBoundsLayer,
                "POINT_FLAGS": outputPointLyr,
                "LINE_FLAGS": outputLineLyr,
                "POLYGON_FLAGS": outputPolygonyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["POINT_FLAGS"], output["LINE_FLAGS"], output["POLYGON_FLAGS"]

    def runIdentifySmallLines(
        self, inputLyr, tol, context, feedback=None, flagLyr=None, onlySelected=False
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        parameters = {
            "INPUT": inputLyr,
            "TOLERANCE": tol,
            "SELECTED": onlySelected,
            "FLAGS": flagLyr,
        }
        output = processing.run(
            "dsgtools:identifysmalllines",
            parameters,
            context=context,
            feedback=feedback,
        )
        return output["FLAGS"]

    def runAddUnsharedVertexOnSharedEdges(
        self,
        inputLinesList,
        inputPolygonsList,
        searchRadius,
        context,
        selected=False,
        geographicBoundsLayer=None,
        feedback=None,
        is_child_algorithm=False,
    ):
        processing.run(
            "dsgtools:addunsharedvertexonsharededgesalgorithm",
            {
                "INPUT_LINES": inputLinesList,
                "INPUT_POLYGONS": inputPolygonsList,
                "SELECTED": selected,
                "SEARCH_RADIUS": searchRadius,
                "GEOGRAPHIC_BOUNDARY": geographicBoundsLayer,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )

    def runIdentifySegmentErrorBetweenLines(
        self,
        inputLayer,
        referenceLineLayer,
        searchRadius,
        context,
        flagLyr=None,
        feedback=None,
        is_child_algorithm=False,
    ):
        flagLyr = "memory:" if flagLyr is None else flagLyr
        output = processing.run(
            "dsgtools:identifysegmenterrorsbetweenlines",
            {
                "INPUT": inputLayer,
                "REFERENCE_LINE": referenceLineLayer,
                "SEARCH_RADIUS": searchRadius,
                "FLAGS": flagLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["FLAGS"]

    def runDetectDatasetChanges(
        self,
        inputLayer: QgsVectorLayer,
        reviewedLayer: QgsVectorLayer,
        attributesList: List[str],
        matchComparation: int,
        context: QgsProcessingContext,
        feedback: Optional[QgsFeedback] = None,
        unchangedLayer: Optional[QgsVectorLayer] = None,
        addedLayer: Optional[QgsVectorLayer] = None,
        deletedLayer: Optional[QgsVectorLayer] = None,
        is_child_algorithm: bool = False,
    ) -> Union[
        Tuple[QgsVectorLayer, QgsVectorLayer, QgsVectorLayer], Tuple[str, str, str]
    ]:
        unchangedLayer = "memory:" if unchangedLayer is None else unchangedLayer
        addedLayer = "memory:" if addedLayer is None else addedLayer
        deletedLayer = "memory:" if deletedLayer is None else deletedLayer
        output = processing.run(
            "native:detectvectorchanges",
            {
                "ORIGINAL": inputLayer,
                "REVISED": reviewedLayer,
                "COMPARE_ATTRIBUTES": attributesList,
                "MATCH_TYPE": matchComparation,
                "UNCHANGED": unchangedLayer,
                "ADDED": addedLayer,
                "DELETED": deletedLayer,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["UNCHANGED"], output["ADDED"], output["DELETED"]

    def runRemoveDuplicateVertex(
        self,
        inputLyr,
        tolerance,
        context,
        useZValue=False,
        feedback=None,
        is_child_algorithm=False,
    ):
        output = processing.run(
            "native:removeduplicatevertices",
            {
                "INPUT": inputLyr,
                "TOLERANCE": tolerance,
                "USE_Z_VALUE": useZValue,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runJoinAttributesTable(
        self,
        layerA,
        fieldA,
        layerB,
        fieldB,
        context,
        method,
        fieldsToCopy=None,
        discardNonMatching=True,
        prefix=None,
        feedback=None,
        is_child_algorithm=False,
    ) -> QgsVectorLayer:
        fieldsToCopy = [] if fieldsToCopy is None else fieldsToCopy
        prefix = "" if prefix is None else prefix
        output = processing.run(
            "native:joinattributestable",
            {
                "INPUT": layerA,
                "FIELD": fieldA,
                "INPUT_2": layerB,
                "FIELD_2": fieldB,
                "FIELDS_TO_COPY": [],
                "METHOD": method,
                "DISCARD_NONMATCHING": discardNonMatching,
                "PREFIX": prefix,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDSGToolsMergeLines(
        self,
        inputLayer,
        context,
        onlySelected=False,
        attributeBlackList=None,
        ignoreVirtualFields=True,
        ignorePkFields=True,
        allowClosed=False,
        pointFilterLyrList=None,
        lineFilterLyrList=None,
        geographicBoundaryLyr=None,
        feedback=None,
    ) -> None:
        attributeBlackList = [] if attributeBlackList is None else attributeBlackList
        pointFilterLyrList = [] if pointFilterLyrList is None else pointFilterLyrList
        lineFilterLyrList = [] if lineFilterLyrList is None else lineFilterLyrList
        output = processing.run(
            "dsgtools:mergelineswithsameattributeset",
            {
                "INPUT": inputLayer,
                "SELECTED": onlySelected,
                "ATTRIBUTE_BLACK_LIST": attributeBlackList,
                "IGNORE_VIRTUAL_FIELDS": ignoreVirtualFields,
                "IGNORE_PK_FIELDS": ignorePkFields,
                "ALLOW_CLOSED": allowClosed,
                "POINT_FILTER_LAYERS": pointFilterLyrList,
                "LINE_FILTER_LAYERS": lineFilterLyrList,
                "GEOGRAPHIC_BOUNDARY": geographicBoundaryLyr,
            },
            context=context,
            feedback=feedback,
        )

    def runRenameField(
        self,
        inputLayer: QgsVectorLayer,
        field: str,
        newName: str,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:renametablefield",
            {
                "INPUT": inputLayer,
                "FIELD": field,
                "NEW_NAME": newName,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSplitLinesByLength(
        self,
        inputLayer: QgsVectorLayer,
        length: float,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:splitlinesbylength",
            {"INPUT": inputLayer, "LENGTH": length, "OUTPUT": outputLyr},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runInterpolatePoint(
        self,
        inputLayer: QgsVectorLayer,
        distance: float,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:interpolatepoint",
            {"INPUT": inputLayer, "DISTANCE": distance, "OUTPUT": outputLyr},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runPolygonFromLayerExtent(
        self,
        inputLayer: QgsMapLayer,
        context: QgsProcessingContext,
        roundTo: Optional[float] = 0.0,
        outputLyr: Optional[QgsVectorLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:polygonfromlayerextent",
            {"INPUT": inputLayer, "ROUND_TO": roundTo, "OUTPUT": outputLyr},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runGdalRasterizeOverFixedValue(
        self,
        inputLayer: QgsVectorLayer,
        inputRaster: QgsRasterLayer,
        value: int,
        context: QgsProcessingContext,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ):
        processing.run(
            "gdal:rasterize_over_fixed_value",
            {
                "INPUT": inputLayer,
                "INPUT_RASTER": inputRaster,
                "BURN": value,
                "ADD": False,
                "EXTRA": '',
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )

    def runDBScanClustering(
        self,
        inputLayer: QgsVectorLayer,
        min_size: int,
        tolerancia: float,
        context: QgsProcessingContext,
        outputLyr=None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsRasterLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:dbscanclustering",
            {
                "INPUT": inputLayer,
                "MIN_SIZE": min_size,
                "EPS": tolerancia,
                "DBSCAN*": False,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSkeletonVoronoi(
        self,
        inputLayer: QgsVectorLayer,
        smoothness: float,
        thin: float,
        context: QgsProcessingContext,
        outputLyr=None,
        feedback: QgsFeedback = None,
        is_child_algorithm: bool = False,
    ) -> QgsRasterLayer:
        outputLyr = "TEMPORARY_OUTPUT:" if outputLyr is None else outputLyr
        output = processing.run(
            "grass7:v.voronoi.skeleton",
            {
                "input": inputLayer,
                "smoothness": smoothness,
                "thin": thin,
                "-a": False,
                "-s": True,
                "-l": False,
                "-t": False,
                "output": "TEMPORARY_OUTPUT",
                "GRASS_REGION_PARAMETER": None,
                "GRASS_SNAP_TOLERANCE_PARAMETER": -1,
                "GRASS_MIN_AREA_PARAMETER": 0.0001,
                "GRASS_OUTPUT_TYPE_PARAMETER": 0,
                "GRASS_VECTOR_DSCO": "",
                "GRASS_VECTOR_LCO": "",
                "GRASS_VECTOR_EXPORT_NOCAT": False,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["output"]

    def runDSGToolsReclassifyGroupsOfPixels(
        self,
        inputRaster: QgsRasterLayer,
        minArea: float,
        nodataValue: int,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsRasterLayer:
        outputLyr = "TEMPORARY_OUTPUT" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:reclassifygroupsofpixelstonearestneighboralgorithm",
            {
                "INPUT": inputRaster,
                "MIN_AREA": minArea,
                "NODATA_VALUE": nodataValue,
                "OUTPUT": outputLyr,
            },
        )
        return output["OUTPUT"]

    def runRasterClipByExtent(
        self,
        inputRaster: QgsRasterLayer,
        extent: QgsRectangle,
        nodata,
        context,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsRasterLayer:
        outputLyr = "TEMPORARY_OUTPUT" if outputLyr is None else outputLyr
        output = processing.run(
            "gdal:cliprasterbyextent",
            {
                "INPUT": inputRaster,
                "PROJWIN": extent,
                "OVERCRS": False,
                "NODATA": nodata,
                "OPTIONS": "",
                "DATA_TYPE": 0,
                "EXTRA": "",
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runOverlapAnalysis(
        self,
        inputLayer: QgsVectorLayer,
        layerList: List[QgsVectorLayer],
        context: QgsProcessingContext,
        gridSize: Optional[float] = None,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:calculatevectoroverlaps",
            {
                "INPUT": inputLayer,
                "LAYERS": layerList,
                "OUTPUT": outputLyr,
                "GRID_SIZE": gridSize,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runReverseLineDirection(
        self,
        inputLayer: QgsVectorLayer,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        output = processing.run(
            "native:reverselinedirection",
            {"INPUT": inputLayer, "OUTPUT": "memory:"},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runSetLineOrientation(
        self,
        inputLayer: QgsVectorLayer,
        context: QgsProcessingContext,
        orientation: Optional[int] = 0,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        output = processing.run(
            "dsgtools:setlineorientation",
            {"INPUT": inputLayer, "ORIENTATION": orientation, "OUTPUT": "memory:"},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runGeneralizeNetworkEdgesFromLengthAlgorithm(
        self,
        inputLayer: QgsVectorLayer,
        context: QgsProcessingContext,
        min_length: float = 0.001,
        bounds_layer: Optional[QgsVectorLayer] = None,
        spatial_partition: Optional[bool] = False,
        pointlyr_list: Optional[List[QgsRasterLayer]] = None,
        linelyr_list: Optional[List[QgsRasterLayer]] = None,
        polygonlyr_list: Optional[List[QgsRasterLayer]] = None,
        method: Optional[int] = 0,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ):
        processing.run(
            "dsgtools:generalizenetworkedgeswithlengthalgorithm",
            {
                "NETWORK_LAYER": inputLayer,
                "MIN_LENGTH": min_length,
                "GEOGRAPHIC_BOUNDS_LAYER": bounds_layer,
                "GROUP_BY_SPATIAL_PARTITION": spatial_partition,
                "POINT_CONSTRAINT_LAYER_LIST": pointlyr_list,
                "LINE_CONSTRAINT_LAYER_LIST": linelyr_list,
                "POLYGON_CONSTRAINT_LAYER_LIST": polygonlyr_list,
                "METHOD": method,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )

    def runGdalWarp(
        self,
        rasterLayer: QgsRasterLayer,
        targetCrs: QgsCoordinateReferenceSystem,
        context: QgsProcessingContext,
        sourceCrs: Optional[QgsCoordinateReferenceSystem] = None,
        nodata: Optional[int] = None,
        options: Optional[str] = None,
        outputLyr: Optional[QgsRasterLayer] = None,
        targetResolution: Optional[float] = None,
        dataType: Optional[int] = None,
        multiThreading: Optional[bool] = False,
        targetExtent: Optional[list] = None,
        targetExtentCrs: Optional[QgsCoordinateReferenceSystem] = None,
        resampling: Optional[int] = 0,
        extra: Optional[str] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> Union[str, QgsRasterLayer]:
        outputLyr = "TEMPORARY_OUTPUT" if outputLyr is None else outputLyr
        extra = "" if extra is None else extra
        output = processing.run(
            "gdal:warpreproject",
            {
                "INPUT": rasterLayer,
                "SOURCE_CRS": sourceCrs,
                "TARGET_CRS": targetCrs,
                "RESAMPLING": resampling,
                "NODATA": nodata,
                "TARGET_RESOLUTION": targetResolution,
                "OPTIONS": options,
                "DATA_TYPE": dataType,
                "TARGET_EXTENT": targetExtent,
                "TARGET_EXTENT_CRS": targetExtentCrs,
                "MULTITHREADING": multiThreading,
                "EXTRA": extra,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runBuildVRT(
        self,
        inputRasterList: List[Union[str, QgsRasterLayer]],
        context: QgsProcessingContext,
        assignCrs: Optional[QgsCoordinateReferenceSystem] = None,
        separate: Optional[bool] = False,
        projDifference: Optional[bool] = False,
        addAlpha: Optional[bool] = False,
        outputLyr: Optional[QgsRasterLayer] = None,
        resolution: Optional[float] = 0,
        srcNodata: Optional[int] = None,
        resampling: Optional[int] = 0,
        extra: Optional[str] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> Union[str, QgsRasterLayer]:
        outputLyr = "TEMPORARY_OUTPUT" if outputLyr is None else outputLyr
        extra = "" if extra is None else extra
        srcNodata = "" if srcNodata is None else srcNodata
        output = processing.run(
            "gdal:buildvirtualraster",
            {
                "INPUT": inputRasterList,
                "RESOLUTION": resolution,
                "SEPARATE": separate,
                "PROJ_DIFFERENCE": projDifference,
                "ADD_ALPHA": addAlpha,
                "ASSIGN_CRS": assignCrs,
                "RESAMPLING": resampling,
                "SRC_NODATA": srcNodata,
                "EXTRA": extra,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runOrientedBoundingBox(
        self,
        inputLyr: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> QgsVectorLayer:
        output = processing.run(
            "qgis:orientedminimumboundingbox",
            {"INPUT": inputLyr, "OUTPUT": "TEMPORARY_OUTPUT"},
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDSGToolsGroupLayers(
        self,
        inputList: List[QgsVectorLayer],
        context: QgsProcessingContext,
        categoryExpression: Optional[str] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> None:
        categoryExpression = (
            "regexp_substr(@layer_name ,'([^_]+)')"
            if categoryExpression is None
            else categoryExpression
        )
        processing.run(
            "dsgtools:grouplayers",
            {
                "INPUT_LAYERS": inputList,
                "CATEGORY_EXPRESSION": categoryExpression,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )

    def runDSGToolsLoadShapefile(
        self,
        inputFolder: str,
        context: QgsProcessingContext,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> None:
        processing.run(
            "dsgtools:loadshapefilealgorithm",
            {
                "FOLDER_SHAPEFILES": inputFolder,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )

    def runDSGToolsExtractMiddleVertexOnLine(
        self,
        inputLayer: QgsVectorLayer,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:extractmiddlevertexonlinealgorithm",
            {
                "INPUT": inputLayer,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runRetainFields(
        self,
        inputLayer: QgsVectorLayer,
        fieldList: List[str],
        context: QgsProcessingContext,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:retainfields",
            {
                "INPUT": inputLayer,
                "FIELDS": fieldList,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDropFields(
        self,
        inputLayer: QgsVectorLayer,
        fieldList: List[str],
        context: QgsProcessingContext,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:deletecolumn",
            {
                "INPUT": inputLayer,
                "COLUMN": fieldList,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDSGToolsSplitLinesAtMaximumLengthAlgorithm(
        self,
        inputLayer: QgsVectorLayer,
        maxLength: float,
        context: QgsProcessingContext,
        outputLyr: Optional[QgsRasterLayer] = None,
        feedback: Optional[QgsFeedback] = None,
        is_child_algorithm: bool = False,
    ) -> QgsVectorLayer:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:splitlinesatmaximumlengthalgorithm",
            {
                "INPUT": inputLayer,
                "MAX_LENGTH": maxLength,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDSGToolsPolygonTiler(
        self,
        inputLayer: QgsVectorLayer,
        rows: int,
        columns: int,
        context: QgsProcessingContext,
        includePartial: bool,
        feedback: Optional[QgsFeedback] = None,
        outputLyr: Optional[QgsVectorLayer] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> Union[QgsVectorLayer, str]:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "dsgtools:polygontiler",
            {
                "INPUT": inputLayer,
                "ROWS": rows,
                "COLUMNS": columns,
                "INCLUDE_PARTIAL": includePartial,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runPolygonFromLayerExtent(
        self,
        inputLayer: QgsVectorLayer,
        context: QgsProcessingContext,
        roundTo: Optional[float] = 0.0,
        feedback: Optional[QgsFeedback] = None,
        outputLyr: Optional[QgsVectorLayer] = None,
        is_child_algorithm: Optional[bool] = False,
    ) -> Union[QgsVectorLayer, str]:
        outputLyr = "memory:" if outputLyr is None else outputLyr
        output = processing.run(
            "native:polygonfromlayerextent",
            {
                "INPUT": inputLayer,
                "ROUND_TO": roundTo,
                "OUTPUT": outputLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runRotateFeatures(
        self,
        inputLayer,
        angle,
        context,
        anchor=None,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        """
        Rotates vector features around specified points.

        Parameters:
            inputLayer: Input vector layer
            angle: Rotation angle in degrees (can be a fixed value or QgsProperty expression)
            context: Processing context
            anchor: Anchor point for rotation (can be a string expression like '$x || \',\' || $y')
            feedback: Processing feedback object
            outputLyr: Output layer path or URI
            is_child_algorithm: Whether this algorithm is being run as part of a larger algorithm

        Returns:
            The output layer with rotated features
        """
        outputLyr = "memory:" if outputLyr is None else outputLyr

        if anchor is None:
            anchor = QgsProperty.fromExpression("$x || ',' || $y")

        parameters = {
            "INPUT": inputLayer,
            "ANGLE": angle,
            "ANCHOR": anchor,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "native:rotatefeatures",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runExtentToLayer(
        self,
        inputLayer,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        """
        Creates a layer containing the extent of the input layer.

        Parameters:
            inputLayer: Input vector layer
            context: Processing context
            feedback: Processing feedback object
            outputLyr: Output layer path or URI
            is_child_algorithm: Whether this algorithm is being run as part of a larger algorithm

        Returns:
            The output layer containing the extent polygon
        """
        outputLyr = "memory:" if outputLyr is None else outputLyr

        parameters = {"INPUT": inputLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:extenttolayer",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runDeleteDuplicateGeometries(
        self,
        inputLayer,
        context,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        """
        Removes duplicate geometries from a layer.

        Parameters:
            inputLayer: Input vector layer
            context: Processing context
            feedback: Processing feedback object
            outputLyr: Output layer path or URI
            is_child_algorithm: Whether this algorithm is being run as part of a larger algorithm

        Returns:
            The output layer with duplicate geometries removed
        """
        outputLyr = "memory:" if outputLyr is None else outputLyr

        parameters = {"INPUT": inputLayer, "OUTPUT": outputLyr}
        output = processing.run(
            "native:deleteduplicategeometries",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runJoinByNearest(
        self,
        inputLayer,
        joinLayer,
        context,
        prefix=None,
        maxDistance=None,
        neighbors=1,
        joinFields=None,
        feedback=None,
        outputLyr=None,
        is_child_algorithm=False,
    ):
        """
        Joins attributes from the nearest feature in another layer.

        Parameters:
            inputLayer: Input vector layer
            joinLayer: Layer with attributes to join
            context: Processing context
            prefix: Prefix to add to joined fields
            maxDistance: Maximum distance to search for neighbors (None means no limit)
            neighbors: Number of neighbors to join
            joinFields: Fields to join (None means all fields)
            feedback: Processing feedback object
            outputLyr: Output layer path or URI
            is_child_algorithm: Whether this algorithm is being run as part of a larger algorithm

        Returns:
            The output layer with joined attributes
        """
        outputLyr = "memory:" if outputLyr is None else outputLyr
        joinFields = [] if joinFields is None else joinFields
        prefix = "" if prefix is None else prefix

        parameters = {
            "INPUT": inputLayer,
            "INPUT_2": joinLayer,
            "FIELDS_TO_COPY": joinFields,
            "PREFIX": prefix,
            "MAX_DISTANCE": maxDistance,
            "NEIGHBORS": neighbors,
            "OUTPUT": outputLyr,
        }
        output = processing.run(
            "qgis:joinbynearest",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT"]

    def runLineOnLineOverlayer(
        self,
        inputLyr: QgsVectorLayer,
        referenceLayers: List[QgsVectorLayer],
        tol: float,
        context: QgsProcessingContext,
        feedback: Optional[QgsFeedback] = None,
        outputSplitLinesLyr: Optional[QgsVectorLayer] = None,
        outputSplitReferenceLinesLyr: Optional[QgsVectorLayer] = None,
        is_child_algorithm: bool = False,
    ) -> Union[Tuple[QgsVectorLayer, QgsVectorLayer], Tuple[str, str]]:
        outputSplitLinesLyr = (
            "memory:" if outputSplitLinesLyr is None else outputSplitLinesLyr
        )
        outputSplitReferenceLinesLyr = (
            "memory:"
            if outputSplitReferenceLinesLyr is None
            else outputSplitReferenceLinesLyr
        )
        output = processing.run(
            "dsgtools:lineonlineoverlayer",
            {
                "INPUT": inputLyr,
                "REFERENCE_LINES": referenceLayers,
                "SNAP_TOLERANCE": tol,
                "OUTPUT_SPLIT_LINES": outputSplitLinesLyr,
                "OUTPUT_MODIFIED_REFERENCES": outputSplitReferenceLinesLyr,
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        return output["OUTPUT_SPLIT_LINES"], output["OUTPUT_MODIFIED_REFERENCES"]

    def runGdalTranslate(
        self,
        inputRaster,
        context,
        outputRaster=None,
        targetCrs=None,
        sourceCrs=None,
        nodata=None,
        options=None,
        dataType=None,
        targetExtent=None,
        targetResolution=None,
        scaleParams=None,
        outputSize=None,
        feedback=None,
        is_child_algorithm=False,
    ):
        """
        Runs GDAL translate algorithm to convert/copy raster data.
        
        :param inputRaster: (QgsRasterLayer or str) Input raster layer or path
        :param context: (QgsProcessingContext) Processing context
        :param outputRaster: (str) Output raster path. If None, uses "TEMPORARY_OUTPUT"
        :param targetCrs: (QgsCoordinateReferenceSystem) Target coordinate reference system
        :param sourceCrs: (QgsCoordinateReferenceSystem) Source coordinate reference system
        :param nodata: (float) NoData value to assign
        :param options: (str) Additional GDAL options
        :param dataType: (int) Output data type (0=Use Input Type, 1=Byte, 2=Int16, 3=UInt16, 4=Int32, 5=UInt32, 6=Float32, 7=Float64)
        :param targetExtent: (QgsRectangle or str) Target extent
        :param targetResolution: (float) Target resolution
        :param scaleParams: (str) Scale parameters in format "src_min,src_max,dst_min,dst_max"
        :param outputSize: (str) Output size in format "width,height"
        :param feedback: (QgsProcessingFeedback) Feedback object for progress reporting
        :param is_child_algorithm: (bool) Whether this is being run as a child algorithm
        :return: (str) Path to output raster
        """
        outputRaster = "TEMPORARY_OUTPUT" if outputRaster is None else outputRaster
        options = "" if options is None else options
        dataType = 0 if dataType is None else dataType
        
        parameters = {
            "INPUT": inputRaster,
            "OUTPUT": outputRaster,
            "TARGET_CRS": targetCrs,
            "SOURCE_CRS": sourceCrs,
            "NODATA": nodata,
            "OPTIONS": options,
            "DATA_TYPE": dataType,
            "PROJWIN": targetExtent,
            "TR": targetResolution,
            "SCALE": scaleParams,
            "OUTSIZE": outputSize,
            "EXTRA": "",
        }
        
        output = processing.run(
            "gdal:translate",
            parameters,
            context=context,
            feedback=feedback,
            is_child_algorithm=is_child_algorithm,
        )
        
        return output["OUTPUT"]
