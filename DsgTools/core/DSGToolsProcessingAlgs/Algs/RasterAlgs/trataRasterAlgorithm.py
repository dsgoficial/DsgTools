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
        return self.tr("Trata Raster (Consolidado)")

    def group(self):
        return self.tr("Raster Handling")

    def groupId(self):
        return "DSGTools - Raster Handling"

    def shortHelpString(self):
        return self.tr(
            "Algoritmo consolidado de tratamento de raster para classificacao "
            "de vegetacao.\n\n"
            "Realiza limpeza (sieve), correcao de classes (massa d'agua e "
            "area edificada), generalizacao e preenchimento de nodata.\n\n"
            "A correcao de classes funciona em etapas:\n"
            "1. Remove TODOS os pixels do raster que possuem os valores DN "
            "de massa d'agua e area edificada (torna nodata)\n"
            "2. Queima os poligonos de referencia com os valores corretos\n"
            "3. Preenche nodata adjacente por vizinho mais proximo\n\n"
            "Parametros:\n"
            "- Raster: Raster classificado de entrada (banda unica)\n"
            "- Area Edificada: Camada vetorial de poligonos\n"
            "- Massa d'Agua: Camada vetorial de poligonos\n"
            "- Valor Area Edificada: Valor DN da classe (ex: 4)\n"
            "- Valor Massa d'Agua: Valor DN da classe (ex: 1)\n"
            "- Valor NoData: (padrao: -9999)\n"
            "- Distancia Buffer: Buffer negativo em unidades do mapa "
            "(padrao: -0.0001)\n"
            "- Limiar Sieve: Pixels minimos por grupo (padrao: 50)\n"
            "- Area Minima Passo 1: m2 para passo 1 (padrao: 15625)\n"
            "- Area Minima Passo 2: m2 para passo 2 (padrao: 62500)\n"
            "- Regras de Generalizacao: JSON com restricoes de classe"
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr("Raster de Entrada"),
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.AREA_EDIFICADA,
                self.tr("Area Edificada (Poligonos)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.MASSA_DAGUA,
                self.tr("Massa d'Agua (Poligonos)"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.AREA_EDIFICADA_VALUE,
                self.tr("Valor DN da Classe Area Edificada"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=2,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MASSA_DAGUA_VALUE,
                self.tr("Valor DN da Classe Massa d'Agua"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NODATA_VALUE,
                self.tr("Valor NoData"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=-9999,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.BUFFER_DISTANCE,
                self.tr("Distancia do Buffer Negativo (unidades do CRS do raster)"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=-5,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SIEVE_THRESHOLD,
                self.tr("Limiar Sieve (pixels)"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=50,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.FIRST_PASS_MIN_AREA,
                self.tr("Area Minima - Passo 1 (m2)"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=15625,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.SECOND_PASS_MIN_AREA,
                self.tr("Area Minima - Passo 2 (m2)"),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=62500,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.GENERALIZATION_RULES_PASS1,
                self.tr(
                    "Regras de Generalizacao - Passo 1 (JSON). "
                    'Formato: {"class_restrictions": {...}, '
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
                    "Regras de Generalizacao - Passo 2 (JSON). "
                    "Usado no segundo passo de generalizacao."
                ),
                defaultValue=self.DEFAULT_RULES_PASS2,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Raster de Saida"),
                optional=False,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        try:
            from scipy.spatial import KDTree
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "Este algoritmo requer a biblioteca scipy. "
                    "Instale com: pip install scipy"
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
                self.tr("Raster de entrada invalido ou nao fornecido.")
            )

        self._tmpDir = tempfile.mkdtemp(prefix="trata_raster_")
        self._tmpCounter = 0

        multiStepFeedback = QgsProcessingMultiStepFeedback(10, feedback)
        step = 0

        try:
            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Etapa 1/10: Lendo raster de entrada...")
            )
            npRaster, geotransform, projection = self._readRaster(
                inputRaster.source()
            )
            multiStepFeedback.pushInfo(
                self.tr("  Dimensoes: %d x %d, dtype: %s")
                % (npRaster.shape[0], npRaster.shape[1], npRaster.dtype)
            )

            rasterCrs = inputRaster.crs()
            multiStepFeedback.pushInfo(
                self.tr("Preparando poligonos (reprojecao, dissolve, buffer)... CRS raster: %s")
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
                self.tr("Etapa 2/10: Sieve inicial (limiar=%d)...") % sieveThreshold
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
                    "Etapa 3/10: Removendo pixels de massa d'agua "
                    "e area edificada..."
                )
            )
            maskMassa = npRaster == massaDaguaValue
            maskEdif = npRaster == areaEdificadaValue
            multiStepFeedback.pushInfo(
                self.tr("  %d pixels massa d'agua (DN=%d), %d pixels area edificada (DN=%d) convertidos para nodata (%d).")
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
                self.tr("Etapa 4/10: Queimando poligonos com valores corretos...")
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
                self.tr("Etapa 5/10: Reclassificando %d pixels nodata por vizinho mais proximo...") % nNodataPixels
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
                self.tr("Etapa 6/10: Generalizacao passo 1 (min_area=%d m2)...") % firstPassMinArea
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
                self.tr("Etapa 7/10: Sieve pos-generalizacao (limiar=%d)...") % sieveThreshold
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
                self.tr("Etapa 8/10: Generalizacao passo 2 (min_area=%d m2)...") % secondPassMinArea
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
                self.tr("Etapa 9/10: Sieve final (limiar=%d)...") % sieveThreshold
            )
            npRaster = self._runSieve(
                npRaster, geotransform, projection, sieveThreshold,
                nodata, context, multiStepFeedback,
            )
            step += 1

            multiStepFeedback.setCurrentStep(step)
            multiStepFeedback.pushInfo(
                self.tr("Etapa 10/10: Escrevendo raster de saida...")
            )
            self._writeRaster(
                npRaster, geotransform, projection, outputRaster, nodata
            )

            multiStepFeedback.pushInfo(
                self.tr("Processamento concluido com sucesso!")
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
                        "Sieve nao produziu saida. Retornando sem alteracao."
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
                self.tr(
                    f"  Reprojetando de "
                    f"{polygonLayer.crs().authid()} para "
                    f"{targetCrs.authid()}..."
                )
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
                self.tr("Nao foi possivel abrir: %s") % rasterPath
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
                    self.tr("  Queimando DN=%d...") % burnValue
                )
                rasterLayer = QgsRasterLayer(tmpPath, "temp_burn")
                if not rasterLayer.isValid():
                    raise QgsProcessingException(
                        self.tr(
                            "Erro ao carregar raster temporario para rasterizacao."
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
                        "Generalizacao nao produziu arquivo de saida. "
                        "Retornando sem alteracao."
                    )
                )
                return npRaster

            result, _, _ = self._readRaster(tmpOutput)

            if result.shape != npRaster.shape:
                feedback.pushWarning(
                    self.tr(
                        f"Generalizacao produziu raster com dimensoes diferentes: "
                        f"{result.shape} vs {npRaster.shape}. "
                        f"Retornando sem alteracao."
                    )
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
