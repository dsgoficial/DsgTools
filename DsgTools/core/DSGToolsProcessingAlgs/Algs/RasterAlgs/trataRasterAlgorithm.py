# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-07-17
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import gc
import json
import os
import shutil
import tempfile
import numpy as np
from osgeo import gdal

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterRasterDestination,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsRasterLayer,
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

import processing


class TrataRasterAlgorithm(QgsProcessingAlgorithm):
    """
    Algoritmo consolidado de tratamento de raster para classificacao de vegetacao.

    Substitui o modelo "02-Trata_Raster" por um unico algoritmo Python.

    Fluxo:
     1. Leitura do raster
     2. Sieve inicial
     3. Remover pixels de massa d'agua e area edificada (torna nodata por valor DN)
     4. Queimar poligonos de referencia com valores corretos das classes
     5. Reclassificar pixels adjacentes com valor nodata
     6. Generalizacao passo 1 (15625 m2)
     7. Sieve pos-generalizacao
     8. Generalizacao passo 2 (62500 m2)
     9. Sieve final
    10. Escrita do raster de saida
    """

    INPUT_RASTER = "INPUT_RASTER"
    AREA_EDIFICADA = "AREA_EDIFICADA"
    MASSA_DAGUA = "MASSA_DAGUA"
    AREA_EDIFICADA_VALUE = "AREA_EDIFICADA_VALUE"
    MASSA_DAGUA_VALUE = "MASSA_DAGUA_VALUE"
    NODATA_VALUE = "NODATA_VALUE"
    BUFFER_DISTANCE = "BUFFER_DISTANCE"
    SIEVE_THRESHOLD = "SIEVE_THRESHOLD"
    FIRST_PASS_MIN_AREA = "FIRST_PASS_MIN_AREA"
    SECOND_PASS_MIN_AREA = "SECOND_PASS_MIN_AREA"
    GENERALIZATION_RULES_PASS1 = "GENERALIZATION_RULES_PASS1"
    GENERALIZATION_RULES_PASS2 = "GENERALIZATION_RULES_PASS2"
    OUTPUT_RASTER = "OUTPUT_RASTER"

    DEFAULT_RULES_PASS1 = json.dumps(
        {
            "class_restrictions": {"4": [2, 3, 6]},
            "size_thresholds": {"1": 2500},
            "non_growing_classes": [1],
        }
    )

    DEFAULT_RULES_PASS2 = json.dumps(
        {
            "class_restrictions": {"4": [2, 3, 6]},
            "size_thresholds": {"1": 10000},
            "non_growing_classes": [1],
        }
    )

    def __init__(self):
        super().__init__()
        self.algRunner = AlgRunner()
        self._tmpDir = None
        self._tmpCounter = 0

    def tr(self, string):
        return QCoreApplication.translate("TrataRasterAlgorithm", string)

    def createInstance(self):
        return TrataRasterAlgorithm()

    def name(self):
        return "trataraster"

    def displayName(self):
        return self.tr("Raster Treatment (Consolidated)")

    def group(self):
        return self.tr("Raster Handling")

    def groupId(self):
        return "DSGTools - Raster Handling"

    def shortHelpString(self):
        return self.tr(
            "Consolidated raster treatment algorithm for vegetation "
            "classification.\n\n"
            "Performs cleanup (sieve), class correction (water body and "
            "built-up area), generalization and nodata filling.\n\n"
            "Class correction works in steps:\n"
            "1. Removes ALL pixels from the raster that have the DN values "
            "of water body and built-up area (converts to nodata)\n"
            "2. Burns reference polygons with correct values\n"
            "3. Fills adjacent nodata by nearest neighbor\n\n"
            "Parameters:\n"
            "- Raster: Classified input raster (single band)\n"
            "- Built-up Area: Vector polygon layer\n"
            "- Water Body: Vector polygon layer\n"
            "- Built-up Area Value: Class DN value (e.g.: 4)\n"
            "- Water Body Value: Class DN value (e.g.: 1)\n"
            "- NoData Value: (default: -9999)\n"
            "- Buffer Distance: Negative buffer in map units "
            "(default: -0.0001)\n"
            "- Sieve Threshold: Minimum pixels per group (default: 50)\n"
            "- Minimum Area Pass 1: m2 for pass 1 (default: 15625)\n"
            "- Minimum Area Pass 2: m2 for pass 2 (default: 62500)\n"
            "- Generalization Rules: JSON with class restrictions"
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr("Input Raster"),
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.AREA_EDIFICADA,
                self.tr("Built-up Area (Polygons)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.MASSA_DAGUA,
                self.tr("Water Body (Polygons)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.AREA_EDIFICADA_VALUE,
                self.tr("DN Value for Built-up Area Class"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=2,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MASSA_DAGUA_VALUE,
                self.tr("DN Value for Water Body Class"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NODATA_VALUE,
                self.tr("NoData Value"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=-9999,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.BUFFER_DISTANCE,
                self.tr("Negative Buffer Distance (raster CRS units)"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=-5,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SIEVE_THRESHOLD,
                self.tr("Sieve Threshold (pixels)"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=50,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.FIRST_PASS_MIN_AREA,
                self.tr("Minimum Area - Pass 1 (m2)"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=15625,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SECOND_PASS_MIN_AREA,
                self.tr("Minimum Area - Pass 2 (m2)"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=62500,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.GENERALIZATION_RULES_PASS1,
                self.tr(
                    "Generalization Rules - Pass 1 (JSON). "
                    'Format: {"class_restrictions": {...}, '
                    '"size_thresholds": {...}, '
                    '"non_growing_classes": [...]}'
                ),
                defaultValue=self.DEFAULT_RULES_PASS1,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.GENERALIZATION_RULES_PASS2,
                self.tr(
                    "Generalization Rules - Pass 2 (JSON). "
                    "Used in the second generalization pass."
                ),
                defaultValue=self.DEFAULT_RULES_PASS2,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output Raster"),
                optional=False,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        try:
            from scipy.spatial import KDTree
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the scipy library. "
                    "Install with: pip install scipy"
                )
            )

        inputRaster = self.parameterAsRasterLayer(
            parameters, self.INPUT_RASTER, context
        )
        areaEdificada = self.parameterAsVectorLayer(
            parameters, self.AREA_EDIFICADA, context
        )
        massaDagua = self.parameterAsVectorLayer(
            parameters, self.MASSA_DAGUA, context
        )
        areaEdificadaValue = self.parameterAsInt(
            parameters, self.AREA_EDIFICADA_VALUE, context
        )
        massaDaguaValue = self.parameterAsInt(
            parameters, self.MASSA_DAGUA_VALUE, context
        )
        nodata = self.parameterAsInt(parameters, self.NODATA_VALUE, context)
        bufferDist = self.parameterAsDouble(parameters, self.BUFFER_DISTANCE, context)
        sieveThreshold = self.parameterAsInt(parameters, self.SIEVE_THRESHOLD, context)
        firstPassMinArea = self.parameterAsInt(
            parameters, self.FIRST_PASS_MIN_AREA, context
        )
        secondPassMinArea = self.parameterAsInt(
            parameters, self.SECOND_PASS_MIN_AREA, context
        )
        rulesPass1 = self.parameterAsString(
            parameters, self.GENERALIZATION_RULES_PASS1, context
        )
        rulesPass2 = self.parameterAsString(
            parameters, self.GENERALIZATION_RULES_PASS2, context
        )
        outputRaster = self.parameterAsOutputLayer(
            parameters, self.OUTPUT_RASTER, context
        )

        if not inputRaster or not inputRaster.isValid():
            raise QgsProcessingException(
                self.tr("Invalid or not provided input raster.")
            )

        self._tmpDir = tempfile.mkdtemp(prefix="trata_raster_")
        self._tmpCounter = 0

        multiStepFeedback = QgsProcessingMultiStepFeedback(10, feedback)
        step = 0

        try:
            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 1/10: Reading input raster...")
            )
            npRaster, geotransform, projection = self._readRaster(
                inputRaster.source()
            )
            multiStepFeedback.pushInfo(
                self.tr("  Dimensions: %d x %d, dtype: %s")
                % (npRaster.shape[0], npRaster.shape[1], npRaster.dtype)
            )

            rasterCrs = inputRaster.crs()
            multiStepFeedback.pushInfo(
                self.tr("Preparing polygons (reprojection, dissolve, buffer)... Raster CRS: %s")
                % rasterCrs.authid()
            )
            massaDaguaBuffered = self._prepareSinglePolygonLayer(
                massaDagua, bufferDist, rasterCrs, context, multiStepFeedback
            )
            areaEdificadaBuffered = self._prepareSinglePolygonLayer(
                areaEdificada, bufferDist, rasterCrs, context, multiStepFeedback
            )
            step += 1

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 2/10: Initial sieve (threshold=%d)...") % sieveThreshold
            )
            npRaster = self._runSieve(
                npRaster, geotransform, projection, sieveThreshold,
                nodata, context, multiStepFeedback,
            )
            step += 1
            if multiStepFeedback.isCanceled():
                return {}

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr(
                    "Step 3/10: Removing water body "
                    "and built-up area pixels..."
                )
            )
            maskMassa = npRaster == massaDaguaValue
            maskEdif = npRaster == areaEdificadaValue
            multiStepFeedback.pushInfo(
                self.tr("  %d water body pixels (DN=%d), %d built-up area pixels (DN=%d) converted to nodata (%d).")
                % (int(np.sum(maskMassa)), massaDaguaValue, int(np.sum(maskEdif)), areaEdificadaValue, nodata)
            )
            npRaster[maskMassa] = nodata
            npRaster[maskEdif] = nodata
            del maskMassa, maskEdif
            step += 1
            if multiStepFeedback.isCanceled():
                return {}

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 4/10: Burning polygons with correct values...")
            )
            npRaster = self._burnMultipleValues(
                npRaster, geotransform, projection,
                [(massaDaguaBuffered, massaDaguaValue),
                 (areaEdificadaBuffered, areaEdificadaValue)],
                nodata, context, multiStepFeedback,
            )
            step += 1
            if multiStepFeedback.isCanceled():
                return {}

            multiStepFeedback.setCurrentStep(step)
            nNodataPixels = int(np.sum(npRaster == nodata))
            multiStepFeedback.pushInfo(
                self.tr("Step 5/10: Reclassifying %d nodata pixels to nearest neighbor...") % nNodataPixels
            )
            if nNodataPixels > 0:
                self._reclassifyValuesToNearestInPlace(
                    npRaster, valuesToReclassify=[nodata]
                )
            step += 1
            if multiStepFeedback.isCanceled():
                return {}

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 6/10: Generalization pass 1 (min_area=%d m2)...") % firstPassMinArea
            )
            npRaster = self._runGeneralization(
                npRaster, geotransform, projection, nodata,
                firstPassMinArea, rulesPass1, context, multiStepFeedback,
            )
            gc.collect()
            step += 1
            if multiStepFeedback.isCanceled():
                return {}

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 7/10: Post-generalization sieve (threshold=%d)...") % sieveThreshold
            )
            npRaster = self._runSieve(
                npRaster, geotransform, projection, sieveThreshold,
                nodata, context, multiStepFeedback,
            )
            step += 1
            if multiStepFeedback.isCanceled():
                return {}

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 8/10: Generalization pass 2 (min_area=%d m2)...") % secondPassMinArea
            )
            npRaster = self._runGeneralization(
                npRaster, geotransform, projection, nodata,
                secondPassMinArea, rulesPass2, context, multiStepFeedback,
            )
            gc.collect()
            step += 1
            if multiStepFeedback.isCanceled():
                return {}

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 9/10: Final sieve (threshold=%d)...") % sieveThreshold
            )
            npRaster = self._runSieve(
                npRaster, geotransform, projection, sieveThreshold,
                nodata, context, multiStepFeedback,
            )
            step += 1

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Step 10/10: Writing output raster...")
            )
            self._writeRaster(
                npRaster, geotransform, projection, outputRaster, nodata
            )

            multiStepFeedback.pushInfo(
                self.tr("Processing completed successfully!")
            )
            return {self.OUTPUT_RASTER: outputRaster}

        finally:
            if self._tmpDir and os.path.exists(self._tmpDir):
                shutil.rmtree(self._tmpDir, ignore_errors=True)

    def _runSieve(
        self, npRaster, geotransform, projection, threshold,
        nodata, context, feedback,
    ):
        tmpInput = self._uniqueTmpPath("sieve_in")
        tmpOutput = self._uniqueTmpPath("sieve_out")

        try:
            self._writeRaster(
                npRaster, geotransform, projection, tmpInput, nodata
            )

            outputPath = self.algRunner.runSieve(
                inputRaster=tmpInput,
                threshold=threshold,
                context=context,
                feedback=feedback,
                outputRaster=tmpOutput,
            )

            if not os.path.exists(outputPath):
                feedback.pushWarning(
                    self.tr(
                        "Sieve did not produce output. Returning without changes."
                    )
                )
                return npRaster

            result, _, _ = self._readRaster(outputPath)
            return result

        finally:
            self._safeRemove(tmpInput)
            self._safeRemove(tmpOutput)

    def _reclassifyValuesToNearestInPlace(self, npRaster, valuesToReclassify):
        """Reclassifica pixels com valores especificos para o vizinho mais
        proximo usando KDTree (scipy). Modifica npRaster in-place."""
        from scipy.spatial import KDTree

        fillMask = np.isin(npRaster, valuesToReclassify)
        sourceMask = ~fillMask

        if not np.any(fillMask) or not np.any(sourceMask):
            return

        sourceCoords = np.argwhere(sourceMask)
        fillCoords = np.argwhere(fillMask)

        nearestIndices = KDTree(sourceCoords).query(fillCoords)[1]
        npRaster[fillMask] = npRaster[sourceMask][nearestIndices]

    def _prepareSinglePolygonLayer(
        self, polygonLayer, bufferDist, targetCrs, context, feedback
    ):
        needsReproject = polygonLayer.crs() != targetCrs
        nSteps = 3 if needsReproject else 2
        innerFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0

        layerToProcess = polygonLayer
        if needsReproject:
            innerFeedback.setCurrentStep(currentStep)
            innerFeedback.pushInfo(
                self.tr("  Reprojecting from %s to %s...")
                % (polygonLayer.crs().authid(), targetCrs.authid())
            )
            layerToProcess = self.algRunner.runReprojectLayer(
                layer=polygonLayer,
                targetCrs=targetCrs,
                context=context,
                feedback=innerFeedback,
                is_child_algorithm=True,
            )
            currentStep += 1

        innerFeedback.setCurrentStep(currentStep)
        dissolved = self.algRunner.runDissolve(
            inputLyr=layerToProcess,
            context=context,
            feedback=innerFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1

        innerFeedback.setCurrentStep(currentStep)
        buffered = self.algRunner.runBuffer(
            inputLayer=dissolved,
            distance=bufferDist,
            context=context,
            feedback=innerFeedback,
            is_child_algorithm=True,
        )

        return buffered

    def _uniqueTmpPath(self, label, ext="tif"):
        self._tmpCounter += 1
        name = f"{label}_{self._tmpCounter}.{ext}"
        return os.path.join(self._tmpDir, name)

    def _readRaster(self, rasterPath):
        ds = gdal.Open(rasterPath)
        if ds is None:
            raise QgsProcessingException(
                self.tr("Could not open: %s") % rasterPath
            )
        npRaster = ds.GetRasterBand(1).ReadAsArray().astype(np.int16)
        geotransform = ds.GetGeoTransform()
        projection = ds.GetProjection()
        ds = None
        return npRaster, geotransform, projection

    def _burnMultipleValues(
        self, npRaster, geotransform, projection,
        layerValuePairs, nodata, context, feedback,
    ):
        """Queima multiplos valores sobre o raster em um unico round-trip de I/O."""
        tmpPath = self._uniqueTmpPath("burn")

        try:
            self._writeRaster(npRaster, geotransform, projection, tmpPath, nodata)

            for vectorLayer, burnValue in layerValuePairs:
                feedback.pushInfo(
                    self.tr("  Burning DN=%d...") % burnValue
                )
                rasterLayer = QgsRasterLayer(tmpPath, "temp_burn")
                if not rasterLayer.isValid():
                    raise QgsProcessingException(
                        self.tr(
                            "Error loading temporary raster for rasterization."
                        )
                    )

                self.algRunner.runGdalRasterizeOverFixedValue(
                    inputLayer=vectorLayer,
                    inputRaster=rasterLayer,
                    value=burnValue,
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

                del rasterLayer

            gc.collect()
            result, _, _ = self._readRaster(tmpPath)
            return result

        finally:
            self._safeRemove(tmpPath)

    def _runGeneralization(
        self, npRaster, geotransform, projection, nodata,
        minArea, rulesJson, context, feedback,
    ):
        tmpInput = self._uniqueTmpPath("gen_in")
        tmpOutput = self._uniqueTmpPath("gen_out")

        try:
            self._writeRaster(
                npRaster, geotransform, projection, tmpInput, nodata
            )

            processing.run(
                "dsgtools:reclassifygroupsofpixelstonearestneighboralgorithm",
                {
                    "INPUT": tmpInput,
                    "MIN_AREA": minArea,
                    "NODATA_VALUE": nodata,
                    "GENERALIZATION_RULES": rulesJson if rulesJson else "",
                    "OUTPUT": tmpOutput,
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )

            if not os.path.exists(tmpOutput):
                feedback.pushWarning(
                    self.tr(
                        "Generalization did not produce output file. "
                        "Returning without changes."
                    )
                )
                return npRaster

            result, _, _ = self._readRaster(tmpOutput)

            if result.shape != npRaster.shape:
                feedback.pushWarning(
                    self.tr(
                        "Generalization produced raster with different dimensions: "
                        "%s vs %s. Returning without changes."
                    )
                    % (result.shape, npRaster.shape)
                )
                return npRaster

            return result

        finally:
            self._safeRemove(tmpInput)
            self._safeRemove(tmpOutput)

    def _writeRaster(
        self, npRaster, geotransform, projection, outputPath, nodata=-9999
    ):
        rows, cols = npRaster.shape
        driver = gdal.GetDriverByName("GTiff")
        ds = driver.Create(
            outputPath, cols, rows, 1, gdal.GDT_Int16,
            options=["COMPRESS=LZW", "TILED=YES"],
        )
        ds.SetGeoTransform(geotransform)
        ds.SetProjection(projection)
        band = ds.GetRasterBand(1)
        band.WriteArray(npRaster)
        band.SetNoDataValue(nodata)
        band.FlushCache()
        ds.FlushCache()
        band = None
        ds = None

    def _safeRemove(self, path):
        if not path:
            return
        try:
            os.remove(path)
        except OSError:
            pass
