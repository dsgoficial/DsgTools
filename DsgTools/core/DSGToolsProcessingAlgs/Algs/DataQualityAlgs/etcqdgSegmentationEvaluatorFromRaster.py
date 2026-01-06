# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-01-06
        git sha              : $Format:%H$
        copyright            : (C) 2026 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import os
import csv
import concurrent.futures
from collections import defaultdict
import numpy as np

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterVectorDestination,
    QgsProcessingParameterString,
    QgsProcessingException,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsProcessingContext,
    QgsRectangle,
    QgsProcessingMultiStepFeedback,
    QgsFields,
    QgsField,
    QgsFeature,
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class ETCQDGSegmentationEvaluatorFromRaster(QgsProcessingAlgorithm):
    INPUT_TILES = "INPUT_TILES"
    INPUT_GT_RASTER = "INPUT_GT_RASTER"
    SEGMENTATION_RASTER = "SEGMENTATION_RASTER"
    CLASS_NAMES_JSON = "CLASS_NAMES_JSON"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"
    OUTPUT_LAYER = "OUTPUT_LAYER"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ETCQDGSegmentationEvaluatorFromRaster()

    def name(self):
        return "etcqdgsegmentationevaluatorfromraster"

    def displayName(self):
        return self.tr("Avaliador de Segmentação a partir de Raster GT (ET-CQDG)")

    def group(self):
        return self.tr("Data Quality")

    def groupId(self):
        return "DSGTools - Data Quality"

    def shortHelpString(self):
        return self.tr(
            """
        Avalia segmentação comparando raster Ground Truth com inferências de múltiplos experimentos.
        
        Diferente da versão vetorial, esta versão trabalha diretamente com raster de GT.
        
        IMPORTANTE:
        - nodata = 255 (pixels ignorados)
        - classe 0 = Background (incluída nas métricas)
        - GT é a referência para resolução espacial e alinhamento
        - Rasters de comparação são reamostrados (vizinho mais próximo) se necessário
        
        Processamento por MI:
        1. Agrupa tiles por MI
        2. Calcula extent combinado no CRS do MI (UTM)
        3. Clipa e reprojeta GT para o extent do MI
        4. Para cada tile:
           - Clipa GT para o tile
           - Clipa e alinha predicted para o tile (usando GT como referência)
           - Calcula métricas: Accuracy, IoU, Precision, Recall, F1
        
        Estrutura de saída:
        Para cada experimento:
        - {experimento}/ground_truth/{MI}/{MI}_{quadricula}.tif: GT clipado
        - {experimento}/predicted_tiles/{MI}/{MI}_{quadricula}.tif: Inferência clipada e alinhada
        - {experimento}/metrics/: CSVs com métricas
        
        Consolidado (raiz):
        - consolidated_all_metrics.csv
        - per_class_metrics.csv
        - consolidated_tile_metrics.csv
        - consolidated_mi_metrics.csv
        
        Parâmetros:
        - Quadrículas: ET-CQDG (campos: mi, quadricula, fuso_utm)
        - Raster Ground Truth: Raster com classes (valores inteiros)
        - Máscaras Inferidas: Resultados de segmentação de múltiplos experimentos
        - Mapeamento de Classes (opcional): JSON com {classe_id: "nome"} ex: {"0": "Background", "1": "Edificacao"}
        - Pasta de Destino: Onde salvar resultados
        """
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_TILES,
                self.tr("Camada de Quadrículas ET-CQDG"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_GT_RASTER,
                self.tr("Raster Ground Truth (Verdade de Campo)"),
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.SEGMENTATION_RASTER,
                self.tr("Máscaras Inferidas (Resultados de Experimentos)"),
                QgsProcessing.TypeRaster,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.CLASS_NAMES_JSON,
                self.tr('Mapeamento de Classes (JSON opcional, ex: {"0": "Background", "1": "Edificacao"})'),
                optional=True,
                defaultValue="",
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_FOLDER, self.tr("Pasta de Destino")
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT_LAYER,
                self.tr("Camada de Saída (Tiles com Métricas)"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # 1. Parâmetros
        tiles_source = self.parameterAsSource(parameters, self.INPUT_TILES, context)
        gt_raster = self.parameterAsRasterLayer(parameters, self.INPUT_GT_RASTER, context)
        segmentation_rasters = self.parameterAsLayerList(parameters, self.SEGMENTATION_RASTER, context)
        class_names_json = self.parameterAsString(parameters, self.CLASS_NAMES_JSON, context)
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 2. Descobrir classes do GT
        class_names = self._discoverClassesFromRaster(gt_raster, class_names_json, feedback)

        # 3. Configurar Output Vector (Sink)
        output_fields = self._createOutputFields(tiles_source.fields(), class_names)

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_LAYER,
            context,
            output_fields,
            tiles_source.wkbType(),
            tiles_source.sourceCrs(),
        )
        if sink is None:
            raise QgsProcessingException("Erro ao criar camada de saída.")

        # 4. Estruturas para consolidação
        all_experiments_tile_metrics = []
        all_experiments_mi_metrics = []
        all_experiments_overall_metrics = []

        tiles_crs = tiles_source.sourceCrs()

        # 5. Loop por experimento
        num_experiments = len(segmentation_rasters)
        multiStepFeedback = QgsProcessingMultiStepFeedback(num_experiments, feedback)

        for exp_idx, segmentation_raster in enumerate(segmentation_rasters):
            multiStepFeedback.setCurrentStep(exp_idx)
            experiment_name = os.path.splitext(os.path.basename(segmentation_raster.source()))[0]

            feedback.pushInfo(f"\n{'=' * 80}")
            multiStepFeedback.setProgressText(f"Processando experimento {exp_idx + 1}/{num_experiments}: {experiment_name}")
            feedback.pushInfo(f"Processando experimento {exp_idx + 1}/{num_experiments}: {experiment_name}")
            feedback.pushInfo(f"{'=' * 80}\n")

            # Criar pasta do experimento
            experiment_folder = os.path.join(output_folder, experiment_name)
            ground_truth_folder = os.path.join(experiment_folder, "ground_truth")
            predicted_folder = os.path.join(experiment_folder, "predicted_tiles")
            metrics_folder = os.path.join(experiment_folder, "metrics")

            for folder in [experiment_folder, ground_truth_folder, predicted_folder, metrics_folder]:
                os.makedirs(folder, exist_ok=True)

            # Processar este experimento
            exp_metrics, featuresToAdd = self._processExperiment(
                experiment_name=experiment_name,
                segmentation_raster=segmentation_raster,
                gt_raster=gt_raster,
                tiles_source=tiles_source,
                class_names=class_names,
                ground_truth_folder=ground_truth_folder,
                predicted_folder=predicted_folder,
                metrics_folder=metrics_folder,
                output_fields=output_fields,
                context=context,
                feedback=multiStepFeedback,
                tiles_crs=tiles_crs,
            )

            list(map(lambda x: sink.addFeature(x), featuresToAdd))

            # Coletar métricas para consolidação
            all_experiments_tile_metrics.extend(exp_metrics["tile_metrics"])
            all_experiments_mi_metrics.extend(exp_metrics["mi_metrics"])
            all_experiments_overall_metrics.append(exp_metrics["overall_metrics"])

        # 6. Gerar CSVs consolidados
        self._writeConsolidatedMetrics(
            output_folder=output_folder,
            tile_metrics=all_experiments_tile_metrics,
            mi_metrics_list=all_experiments_mi_metrics,
            overall_metrics_list=all_experiments_overall_metrics,
            class_names=class_names,
        )

        return {self.OUTPUT_FOLDER: output_folder, self.OUTPUT_LAYER: dest_id}

    def _discoverClassesFromRaster(self, gt_raster, class_names_json, feedback):
        """Descobre classes únicas do GT e monta dicionário de nomes"""
        import json
        
        feedback.pushInfo("Descobrindo classes do raster GT...")
        
        # Ler amostra do raster para descobrir classes
        try:
            import rasterio
            with rasterio.open(gt_raster.source()) as src:
                # Ler amostra (primeira janela 1000x1000 ou todo o raster se menor)
                window_size = min(1000, src.width, src.height)
                sample = src.read(1, window=(0, 0, window_size, window_size))
                
                # Encontrar valores únicos (excluindo nodata)
                unique_values = np.unique(sample[sample != 255])
                
        except Exception as e:
            feedback.reportError(f"Erro ao ler raster GT: {e}")
            # Fallback: assumir classes 0-10
            unique_values = np.arange(11)
        
        # Parsear JSON de nomes se fornecido
        user_class_names = {}
        if class_names_json:
            try:
                user_class_names = json.loads(class_names_json)
                # Converter chaves para int
                user_class_names = {int(k): v for k, v in user_class_names.items()}
            except Exception as e:
                feedback.reportError(f"Erro ao parsear JSON de classes: {e}")
        
        # Montar dicionário final
        class_names = {}
        for val in unique_values:
            val_int = int(val)
            if val_int in user_class_names:
                class_names[val_int] = user_class_names[val_int]
            else:
                class_names[val_int] = f"Classe_{val_int}"
        
        if 0 not in class_names:
            class_names[0] = "Background"
        
        feedback.pushInfo(f"Classes descobertas: {class_names}")
        return class_names

    def _createOutputFields(self, source_fields, class_names):
        """Cria campos da camada de saída"""
        source_fields = [f for f in source_fields if f.name() != "fid"]
        output_fields = QgsFields(source_fields)

        output_fields.append(QgsField("experimento", QVariant.String))
        output_fields.append(QgsField("gt_path", QVariant.String))
        output_fields.append(QgsField("pred_path", QVariant.String))
        output_fields.append(QgsField("accuracy", QVariant.Double))
        output_fields.append(QgsField("mean_iou", QVariant.Double))
        output_fields.append(QgsField("f1_score", QVariant.Double))
        output_fields.append(QgsField("precision", QVariant.Double))
        output_fields.append(QgsField("recall", QVariant.Double))
        output_fields.append(QgsField("total_px", QVariant.Int))
        output_fields.append(QgsField("correct_px", QVariant.Int))

        sorted_classes = sorted(class_names.keys())
        for cid in sorted_classes:
            cname = class_names[cid].replace(" ", "_")
            prefix = f"cl_{cid}_{cname}"[:20]
            output_fields.append(QgsField(f"{prefix}_iou", QVariant.Double))
            output_fields.append(QgsField(f"{prefix}_f1", QVariant.Double))
            output_fields.append(QgsField(f"{prefix}_prec", QVariant.Double))
            output_fields.append(QgsField(f"{prefix}_rec", QVariant.Double))

        return output_fields

    def _processExperiment(
        self,
        experiment_name,
        segmentation_raster,
        gt_raster,
        tiles_source,
        class_names,
        ground_truth_folder,
        predicted_folder,
        metrics_folder,
        output_fields,
        context,
        feedback,
        tiles_crs,
    ):
        """Processa um único experimento"""

        # Planejamento: agrupar tiles por MI
        tiles_by_mi = defaultdict(dict)
        total_tiles_count = 0
        for tile_feat in tiles_source.getFeatures():
            mi = tile_feat["mi"]
            quadricula = tile_feat["quadricula"]
            tile_id = f"{mi}_{quadricula}"
            tiles_by_mi[mi][tile_id] = tile_feat
            total_tiles_count += 1

        total_steps = 1 + len(tiles_by_mi) + total_tiles_count + 1
        multiStepFeedback = QgsProcessingMultiStepFeedback(total_steps, feedback)
        current_step_index = 0
        multiStepFeedback.setCurrentStep(current_step_index)
        current_step_index += 1

        global_counts = {}
        global_total_pixels = 0
        global_correct_pixels = 0
        mi_accumulators = defaultdict(lambda: {"counts": {}, "total_pixels": 0, "correct_pixels": 0})
        metrics_by_tile = []

        algRunner = AlgRunner()
        processed_count = 0

        max_workers = os.cpu_count() or 4
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        futures_map = {}
        tile_data_cache = {}
        featsToAdd = []
        output_fields_names = [f.name() for f in output_fields]
        sorted_classes = sorted(class_names.keys())

        try:
            for mi, tile_feature_dict in tiles_by_mi.items():
                if multiStepFeedback.isCanceled():
                    break

                tile_features = list(tile_feature_dict.values())
                multiStepFeedback.setCurrentStep(current_step_index)
                multiStepFeedback.pushInfo(f"Processando MI: {mi}")

                mi_gt_folder = os.path.join(ground_truth_folder, mi)
                mi_pred_folder = os.path.join(predicted_folder, mi)
                os.makedirs(mi_gt_folder, exist_ok=True)
                os.makedirs(mi_pred_folder, exist_ok=True)

                # CRS do MI
                fuso_utm = tile_features[0]["fuso_utm"]
                utm_crs = QgsCoordinateReferenceSystem(fuso_utm)
                if not utm_crs.isValid():
                    multiStepFeedback.reportError(f"Fuso UTM inválido: {fuso_utm}. Pulando MI {mi}.")
                    current_step_index += 1 + len(tile_features)
                    continue

                # Calcular extent combinado dos tiles no CRS do MI
                mi_extent_utm = self._calculateMIExtent(tile_features, tiles_crs, utm_crs, feedback)

                # Preparar GT para este MI (clipar e reprojetar)
                gt_mi_path = os.path.join(mi_gt_folder, f"gt_{mi}_full.tif")
                gt_mi_raster = self._prepareGTForMI(
                    gt_raster=gt_raster,
                    mi_extent_utm=mi_extent_utm,
                    utm_crs=utm_crs,
                    output_path=gt_mi_path,
                    algRunner=algRunner,
                    context=context,
                    feedback=multiStepFeedback,
                )

                # Preparar Predicted para este MI (clipar e reprojetar)
                pred_mi_path = os.path.join(mi_pred_folder, f"pred_{mi}_full.tif")
                pred_mi_raster = self._preparePredictedForMI(
                    predicted_raster=segmentation_raster,
                    gt_raster_path=gt_mi_path,
                    mi_extent_utm=mi_extent_utm,
                    utm_crs=utm_crs,
                    output_path=pred_mi_path,
                    algRunner=algRunner,
                    context=context,
                    feedback=multiStepFeedback,
                )

                current_step_index += 1

                # Processar cada tile
                for tile_feat in tile_features:
                    if multiStepFeedback.isCanceled():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break

                    multiStepFeedback.setCurrentStep(current_step_index)

                    quadricula = tile_feat["quadricula"]
                    tile_id = f"{mi}_{quadricula}"

                    # Obter geometria do tile no CRS UTM
                    tile_geom_utm = self._getTileGeometryInUTM(tile_feat, tiles_crs, utm_crs)
                    tile_bbox_utm = tile_geom_utm.boundingBox()

                    task_data = {
                        "mi": mi,
                        "quadricula": quadricula,
                        "gt_raster_path": gt_mi_path,
                        "pred_raster_path": pred_mi_path,
                        "tile_bbox": tile_bbox_utm,
                        "gt_tile_path": os.path.join(mi_gt_folder, f"{tile_id}.tif"),
                        "pred_tile_path": os.path.join(mi_pred_folder, f"{tile_id}.tif"),
                        "nodata": 255,
                        "class_names": class_names,
                    }

                    future = executor.submit(process_tile_worker_raster, task_data)
                    futures_map[future] = tile_id

                    current_step_index += 1

            # Coletar resultados
            multiStepFeedback.pushInfo(f"\nColetando resultados...")

            for future in concurrent.futures.as_completed(futures_map):
                tile_id = futures_map[future]
                if multiStepFeedback.isCanceled():
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

                try:
                    result = future.result()
                    if result["status"] == "success":
                        m = result["metrics"]
                        raw = m.pop("raw_counts", {})
                        self._updateCounts(global_counts, raw)
                        self._updateCounts(mi_accumulators[result["mi"]]["counts"], raw)

                        t_px, c_px = m.get("total_pixels", 0), m.get("correct_pixels", 0)
                        global_total_pixels += t_px
                        global_correct_pixels += c_px
                        mi_accumulators[result["mi"]]["total_pixels"] += t_px
                        mi_accumulators[result["mi"]]["correct_pixels"] += c_px

                        m.update(
                            {
                                "experiment": experiment_name,
                                "mi": result["mi"],
                                "quadricula": result["quadricula"],
                                "tile_id": tile_id,
                            }
                        )
                        metrics_by_tile.append(m)
                        processed_count += 1

                        # Gravar no sink
                        tile_data_cache = tiles_by_mi.get(result["mi"], {})
                        if tile_id in tile_data_cache:
                            cached = tile_data_cache[tile_id]
                            new_feat = self._createOutputFeature(
                                cached,
                                output_fields,
                                output_fields_names,
                                experiment_name,
                                result,
                                m,
                                t_px,
                                c_px,
                                sorted_classes,
                                class_names,
                            )
                            featsToAdd.append(new_feat)

                    else:
                        multiStepFeedback.reportError(f"Erro no worker {tile_id}: {result.get('error')}")

                except Exception as exc:
                    multiStepFeedback.reportError(f"Exceção {tile_id}: {exc}")

        finally:
            executor.shutdown(wait=False)

        # Métricas finais
        multiStepFeedback.setCurrentStep(total_steps - 1)
        global_metrics = self._calculateFinalMetricsFromCounts(
            global_counts, global_correct_pixels, global_total_pixels, class_names
        )
        global_metrics["experiment_name"] = experiment_name
        global_metrics.update({"num_tiles": processed_count, "num_mis": len(mi_accumulators)})

        multiStepFeedback.pushInfo("\n" + "=" * 80)
        multiStepFeedback.pushInfo(f"RESUMO {experiment_name} ({processed_count} tiles)")
        multiStepFeedback.pushInfo("-" * 80)
        multiStepFeedback.pushInfo(f"Acurácia Global:   {global_metrics.get('accuracy', 0):.2%}")
        multiStepFeedback.pushInfo(f"Mean IoU:          {global_metrics.get('mean_iou', 0):.4f}")
        multiStepFeedback.pushInfo(f"Mean F1-Score:     {global_metrics.get('f1_score', 0):.4f}")
        multiStepFeedback.pushInfo("=" * 80 + "\n")

        # Export CSVs por experimento
        self._write_csv_safe(os.path.join(metrics_folder, "metrics_per_tile.csv"), metrics_by_tile)

        mi_list = []
        for mi, data in mi_accumulators.items():
            mm = self._calculateFinalMetricsFromCounts(data["counts"], data["correct_pixels"], data["total_pixels"], class_names)
            mm["experiment"] = experiment_name
            mm["mi"] = mi
            mi_list.append(mm)

        self._write_csv_safe(os.path.join(metrics_folder, "metrics_per_mi.csv"), mi_list)
        self._write_csv_safe(os.path.join(metrics_folder, "metrics_overall.csv"), [global_metrics])

        return {"tile_metrics": metrics_by_tile, "mi_metrics": mi_list, "overall_metrics": global_metrics}, featsToAdd

    def _calculateMIExtent(self, tile_features, tiles_crs, utm_crs, feedback):
        """Calcula o extent combinado dos tiles no CRS do MI"""
        xform = QgsCoordinateTransform(tiles_crs, utm_crs, QgsProject.instance())
        
        combined_extent = None
        for tile_feat in tile_features:
            geom = tile_feat.geometry()
            geom.transform(xform)
            bbox = geom.boundingBox()
            
            if combined_extent is None:
                combined_extent = bbox
            else:
                combined_extent.combineExtentWith(bbox)
        
        # Buffer de segurança
        buffer = max(combined_extent.width(), combined_extent.height()) * 0.1
        combined_extent = QgsRectangle(
            combined_extent.xMinimum() - buffer,
            combined_extent.yMinimum() - buffer,
            combined_extent.xMaximum() + buffer,
            combined_extent.yMaximum() + buffer,
        )
        
        return combined_extent

    def _prepareGTForMI(self, gt_raster, mi_extent_utm, utm_crs, output_path, algRunner, context, feedback):
        """Clipa e reprojeta GT para o extent do MI"""
        gt_crs = gt_raster.crs()
        
        # Transformar extent para CRS do GT
        xform = QgsCoordinateTransform(utm_crs, gt_crs, QgsProject.instance())
        gt_extent = xform.transformBoundingBox(mi_extent_utm)
        
        # Clipar
        clipped_gt = algRunner.runRasterClipByExtent(
            inputRaster=gt_raster,
            extent=gt_extent,
            nodata=255,
            context=context,
            feedback=feedback,
        )
        
        # Reprojetar para UTM do MI
        if gt_crs != utm_crs:
            reprojected_gt = algRunner.runGdalWarp(
                rasterLayer=clipped_gt,
                targetCrs=utm_crs,
                context=context,
                resampling=0,  # Nearest neighbor
                feedback=feedback,
                outputLyr=output_path,
            )
        else:
            # Copiar para output_path
            reprojected_gt = algRunner.runGdalTranslate(
                inputRaster=clipped_gt,
                context=context,
                outputRaster=output_path,
                feedback=feedback,
            )
        
        return reprojected_gt if isinstance(reprojected_gt, str) else reprojected_gt.source()

    def _preparePredictedForMI(self, predicted_raster, gt_raster_path, mi_extent_utm, utm_crs, output_path, algRunner, context, feedback):
        """Clipa e reprojeta Predicted para o extent do MI, alinhando com GT"""
        pred_crs = predicted_raster.crs()
        
        # Transformar extent para CRS do predicted
        xform = QgsCoordinateTransform(utm_crs, pred_crs, QgsProject.instance())
        pred_extent = xform.transformBoundingBox(mi_extent_utm)
        
        # Clipar
        clipped_pred = algRunner.runRasterClipByExtent(
            inputRaster=predicted_raster,
            extent=pred_extent,
            nodata=255,
            context=context,
            feedback=feedback,
        )
        
        # Reprojetar e alinhar ao GT usando gdal.Warp
        # O GT é a referência: mesma resolução, mesmo grid
        try:
            import rasterio
            
            # Ler parâmetros do GT
            with rasterio.open(gt_raster_path) as gt_src:
                gt_res_x, gt_res_y = gt_src.res
                gt_bounds = gt_src.bounds
                gt_width, gt_height = gt_src.width, gt_src.height
            
            # Warp predicted alinhado ao GT
            reprojected_pred = algRunner.runGdalWarp(
                rasterLayer=clipped_pred,
                targetCrs=utm_crs,
                context=context,
                resampling=0,  # Nearest neighbor
                targetResolution=gt_res_x,  # Usar resolução do GT
                targetExtent=[gt_bounds.left, gt_bounds.bottom, gt_bounds.right, gt_bounds.top],
                feedback=feedback,
                outputLyr=output_path,
            )
            
        except ImportError:
            feedback.reportError("rasterio não disponível, alinhamento pode não ser perfeito")
            # Fallback sem alinhamento garantido
            reprojected_pred = algRunner.runGdalWarp(
                rasterLayer=clipped_pred,
                targetCrs=utm_crs,
                context=context,
                resampling=0,
                feedback=feedback,
                outputLyr=output_path,
            )
        
        return reprojected_pred if isinstance(reprojected_pred, str) else reprojected_pred.source()

    def _getTileGeometryInUTM(self, tile_feat, tiles_crs, utm_crs):
        """Transforma geometria do tile para CRS UTM"""
        geom = tile_feat.geometry()
        xform = QgsCoordinateTransform(tiles_crs, utm_crs, QgsProject.instance())
        geom.transform(xform)
        return geom

    def _createOutputFeature(self, cached, output_fields, output_fields_names, experiment_name, result, m, t_px, c_px, sorted_classes, class_names):
        """Cria feature de saída com métricas"""
        new_feat = QgsFeature(output_fields)
        new_feat.setGeometry(cached.geometry())

        for field in cached.fields():
            if field.name() not in output_fields_names:
                continue
            new_feat[field.name()] = cached[field.name()]

        new_feat.setAttribute("experimento", experiment_name)
        new_feat.setAttribute("gt_path", result["gt_path"])
        new_feat.setAttribute("pred_path", result["pred_path"])
        new_feat.setAttribute("accuracy", m.get("accuracy"))
        new_feat.setAttribute("mean_iou", m.get("mean_iou"))
        new_feat.setAttribute("f1_score", m.get("f1_score"))
        new_feat.setAttribute("precision", m.get("precision"))
        new_feat.setAttribute("recall", m.get("recall"))
        new_feat.setAttribute("total_px", t_px)
        new_feat.setAttribute("correct_px", c_px)

        for cid in sorted_classes:
            cname = class_names[cid]
            src_prefix = f"class_{cid}_{cname}"
            dest_prefix = f"cl_{cid}_{cname.replace(' ', '_')}"[:20]
            new_feat.setAttribute(f"{dest_prefix}_iou", m.get(f"{src_prefix}_iou"))
            new_feat.setAttribute(f"{dest_prefix}_f1", m.get(f"{src_prefix}_f1_score"))
            new_feat.setAttribute(f"{dest_prefix}_prec", m.get(f"{src_prefix}_precision"))
            new_feat.setAttribute(f"{dest_prefix}_rec", m.get(f"{src_prefix}_recall"))

        return new_feat

    def _updateCounts(self, acc, new):
        for c, m in new.items():
            if c not in acc:
                acc[c] = {"tp": 0, "fp": 0, "fn": 0}
            acc[c]["tp"] += m["tp"]
            acc[c]["fp"] += m["fp"]
            acc[c]["fn"] += m["fn"]
        return acc

    def _calculateFinalMetricsFromCounts(self, counts, correct, total, names):
        if total == 0:
            return {}
        m = {"accuracy": correct / total}
        ious, f1s, precs, recs = [], [], [], []

        for c in sorted(counts.keys()):
            v = counts[c]
            tp, fp, fn = v["tp"], v["fp"], v["fn"]
            u = tp + fp + fn
            iou = tp / u if u > 0 else 0
            p = tp / (tp + fp) if (tp + fp) > 0 else 0
            r = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (p * r) / (p + r) if (p + r) > 0 else 0

            ious.append(iou)
            f1s.append(f1)
            precs.append(p)
            recs.append(r)

            k = f"class_{c}_{names.get(c, f'C_{c}')}"
            m[f"{k}_iou"] = iou
            m[f"{k}_precision"] = p
            m[f"{k}_recall"] = r
            m[f"{k}_f1_score"] = f1

        m["mean_iou"] = sum(ious) / len(ious) if ious else 0
        m["f1_score"] = sum(f1s) / len(f1s) if f1s else 0
        m["precision"] = sum(precs) / len(precs) if precs else 0
        m["recall"] = sum(recs) / len(recs) if recs else 0
        return m

    def _write_csv_safe(self, path, data_list):
        if not data_list:
            return
        all_keys = set().union(*(d.keys() for d in data_list))
        priority = [
            "experiment",
            "mi",
            "quadricula",
            "tile_id",
            "class_id",
            "class_name",
            "accuracy",
            "mean_iou",
            "precision",
            "recall",
            "f1_score",
            "iou",
            "num_tiles",
            "num_mis",
        ]
        header = [k for k in priority if k in all_keys] + sorted([k for k in all_keys if k not in priority])
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(data_list)

    def _writeConsolidatedMetrics(self, output_folder, tile_metrics, mi_metrics_list, overall_metrics_list, class_names):
        """Escreve CSVs consolidados no formato esperado"""

        # consolidated_all_metrics.csv (overall de todos experimentos)
        consolidated_overall = []
        for metrics in overall_metrics_list:
            row = {
                "experiment": metrics.get("experiment_name", ""),
                "num_tiles": metrics.get("num_tiles", 0),
                "num_mis": metrics.get("num_mis", 0),
                "accuracy": metrics.get("accuracy", 0),
                "mean_iou": metrics.get("mean_iou", 0),
                "precision": metrics.get("precision", 0),
                "recall": metrics.get("recall", 0),
                "f1_score": metrics.get("f1_score", 0),
            }

            # Adicionar métricas por classe
            for cls_id in sorted(class_names.keys()):
                c_name = class_names[cls_id]
                prefix = f"class_{cls_id}_{c_name}"
                row[f"{prefix}_iou"] = metrics.get(f"{prefix}_iou", 0)
                row[f"{prefix}_precision"] = metrics.get(f"{prefix}_precision", 0)
                row[f"{prefix}_recall"] = metrics.get(f"{prefix}_recall", 0)
                row[f"{prefix}_f1_score"] = metrics.get(f"{prefix}_f1_score", 0)

            consolidated_overall.append(row)

        self._write_csv_safe(os.path.join(output_folder, "consolidated_all_metrics.csv"), consolidated_overall)

        # per_class_metrics.csv
        per_class_consolidated = []
        for metrics in overall_metrics_list:
            exp_name = metrics.get("experiment_name", "")
            for cls_id in sorted(class_names.keys()):
                c_name = class_names[cls_id]
                prefix = f"class_{cls_id}_{c_name}"

                row = {
                    "experiment": exp_name,
                    "class_id": cls_id,
                    "class_name": c_name,
                    "iou": metrics.get(f"{prefix}_iou", 0),
                    "precision": metrics.get(f"{prefix}_precision", 0),
                    "recall": metrics.get(f"{prefix}_recall", 0),
                    "f1_score": metrics.get(f"{prefix}_f1_score", 0),
                }
                per_class_consolidated.append(row)

        self._write_csv_safe(os.path.join(output_folder, "per_class_metrics.csv"), per_class_consolidated)

        # Tile metrics consolidados
        self._write_csv_safe(os.path.join(output_folder, "consolidated_tile_metrics.csv"), tile_metrics)

        # MI metrics consolidados
        self._write_csv_safe(os.path.join(output_folder, "consolidated_mi_metrics.csv"), mi_metrics_list)


def process_tile_worker_raster(data):
    """Worker para processar um tile (versão raster)"""
    try:
        import rasterio
        from rasterio.warp import reproject, Resampling
        from DsgTools.core.GeometricTools.rasterHandler import calculateSegmentationMetricsFromArrays

        gt_raster_path = data["gt_raster_path"]
        pred_raster_path = data["pred_raster_path"]
        tile_bbox = data["tile_bbox"]
        gt_tile_path = data["gt_tile_path"]
        pred_tile_path = data["pred_tile_path"]
        nodata = data["nodata"]
        class_names = data["class_names"]

        # Abrir rasters do MI
        with rasterio.open(gt_raster_path) as gt_src:
            # Calcular window para o tile
            window = rasterio.windows.from_bounds(
                tile_bbox.xMinimum(),
                tile_bbox.yMinimum(),
                tile_bbox.xMaximum(),
                tile_bbox.yMaximum(),
                transform=gt_src.transform,
            )

            # Ler GT para o tile
            gt_tile_array = gt_src.read(1, window=window)
            gt_transform = rasterio.windows.transform(window, gt_src.transform)
            gt_meta = gt_src.meta.copy()
            gt_meta.update(
                {
                    "height": gt_tile_array.shape[0],
                    "width": gt_tile_array.shape[1],
                    "transform": gt_transform,
                    "compress": "lzw",
                }
            )

            # Salvar GT tile
            with rasterio.open(gt_tile_path, "w", **gt_meta) as gt_dst:
                gt_dst.write(gt_tile_array, 1)

        # Abrir predicted e alinhar ao GT
        with rasterio.open(pred_raster_path) as pred_src:
            # Ler extent do predicted correspondente
            window_pred = rasterio.windows.from_bounds(
                tile_bbox.xMinimum(),
                tile_bbox.yMinimum(),
                tile_bbox.xMaximum(),
                tile_bbox.yMaximum(),
                transform=pred_src.transform,
            )

            pred_tile_array_raw = pred_src.read(1, window=window_pred)

            # Verificar se precisa alinhar
            if (
                pred_tile_array_raw.shape != gt_tile_array.shape
                or pred_src.res != gt_src.res
            ):
                # Reamostrar predicted para alinhar com GT
                pred_tile_array = np.empty_like(gt_tile_array, dtype=pred_tile_array_raw.dtype)

                reproject(
                    source=pred_tile_array_raw,
                    destination=pred_tile_array,
                    src_transform=rasterio.windows.transform(window_pred, pred_src.transform),
                    src_crs=pred_src.crs,
                    dst_transform=gt_transform,
                    dst_crs=gt_src.crs,
                    resampling=Resampling.nearest,
                    src_nodata=nodata,
                    dst_nodata=nodata,
                )
            else:
                pred_tile_array = pred_tile_array_raw

            # Salvar predicted tile alinhado
            pred_meta = gt_meta.copy()
            with rasterio.open(pred_tile_path, "w", **pred_meta) as pred_dst:
                pred_dst.write(pred_tile_array, 1)

        # Calcular métricas
        metrics = calculateSegmentationMetricsFromArrays(
            gt_tile_array, pred_tile_array, nodata, class_names
        )

        return {
            "status": "success",
            "mi": data["mi"],
            "quadricula": data["quadricula"],
            "metrics": metrics,
            "gt_path": gt_tile_path,
            "pred_path": pred_tile_path,
        }

    except Exception as e:
        import traceback
        return {
            "status": "error",
            "mi": data["mi"],
            "quadricula": data["quadricula"],
            "error": f"{str(e)}\n{traceback.format_exc()}",
        }
