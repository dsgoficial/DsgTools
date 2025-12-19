# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-12-18
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

import os
import csv
import json
import concurrent.futures
from collections import defaultdict
import numpy as np
import processing 

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterVectorDestination,
    QgsProcessingException,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsVectorLayer,
    QgsProcessingContext,
    QgsRectangle,
    QgsProcessingMultiStepFeedback,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsGeometry
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

class ETCQDGSegmentationEvaluator(QgsProcessingAlgorithm):
    INPUT_TILES = "INPUT_TILES"
    INPUT_MASK_LAYER = "INPUT_MASK_LAYER"
    CLASS_FIELD = "CLASS_FIELD"
    CLASS_NAME_FIELD = "CLASS_NAME_FIELD"
    SEGMENTATION_RASTER = "SEGMENTATION_RASTER"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"
    OUTPUT_LAYER = "OUTPUT_LAYER"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ETCQDGSegmentationEvaluator()

    def name(self):
        return "etcqdgsegmentationevaluator"

    def displayName(self):
        return self.tr("Avaliador de Segmentação segundo a ET-CQDG")

    def group(self):
        return self.tr("Data Quality")

    def groupId(self):
        return "DSGTools - Data Quality"

    def shortHelpString(self):
        return self.tr(
            """
        Gera máscaras de segmentação e avalia métricas comparando com inferências de múltiplos experimentos.
        
        A máscara inferida é considerada o resultado de uma rede neural.
        As máscaras geradas são a verdade de campo (ground truth).
        
        IMPORTANTE: 
        - nodata = 255 (pixels ignorados)
        - classe 0 = Background (incluída nas métricas)
        
        Estrutura de saída:
        Para cada experimento (raster inferido):
        - {experimento}/ground_truth/{MI}/{MI}_{quadricula}.tif: Máscaras geradas
        - {experimento}/predicted_tiles/{MI}/{MI}_{quadricula}.tif: Inferência clipada
        - {experimento}/metrics/: CSVs com métricas de avaliação
        
        Consolidado (raiz da pasta de destino):
        - consolidated_all_metrics.csv: Métricas gerais de todos experimentos
        - per_class_metrics.csv: Métricas por classe de todos experimentos
        - consolidated_tile_metrics.csv: Métricas de todos tiles de todos experimentos
        
        Para cada MI:
        1. Calcula extent combinado e clipa máscara inferida
        2. Reprojeta para o fuso UTM correspondente
        3. Usa o tamanho do pixel do raster reprojetado
        
        Para cada tile:
        1. Extrai polígonos que intersectam
        2. Gera ground truth (rasterização)
        3. Clipa tile da máscara inferida
        4. Calcula métricas: Accuracy, IoU, Precision, Recall, F1
        5. Calcula métricas por classe (incluindo Background)
        
        Parâmetros:
        - Quadrículas: ET-CQDG (campos: mi, quadricula, fuso_utm)
        - Camada de Máscaras: Polígonos com classes (ground truth)
        - Campo de Classe: Campo inteiro com valores de classe (0 = Background)
        - Campo com Nome da Classe: Campo com nomes descritivos (padrão: class_name)
        - Máscaras Inferidas: Resultados de segmentação de múltiplos experimentos
        - Pasta de Destino: Onde salvar tudo
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
            QgsProcessingParameterFeatureSource(
                self.INPUT_MASK_LAYER,
                self.tr("Camada de Polígonos para Máscaras"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CLASS_FIELD,
                self.tr("Campo de Classe (valores inteiros)"),
                parentLayerParameterName=self.INPUT_MASK_LAYER,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CLASS_NAME_FIELD,
                self.tr("Campo com Nome da Classe"),
                parentLayerParameterName=self.INPUT_MASK_LAYER,
                type=QgsProcessingParameterField.String,
                defaultValue="class_name",
                optional=True,
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
        mask_source = self.parameterAsSource(parameters, self.INPUT_MASK_LAYER, context)
        class_field = self.parameterAsString(parameters, self.CLASS_FIELD, context)
        class_name_field = self.parameterAsString(parameters, self.CLASS_NAME_FIELD, context)
        segmentation_rasters = self.parameterAsLayerList(parameters, self.SEGMENTATION_RASTER, context)
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        # 2. Setup Pasta Base
        if not os.path.exists(output_folder): 
            os.makedirs(output_folder)

        # 3. Mapear Classes
        class_names = {}
        has_class_name_field = (class_name_field and class_name_field in [f.name() for f in mask_source.fields()])
        for feature in mask_source.getFeatures():
            class_value = feature[class_field]
            if class_value is not None and class_value not in class_names:
                if has_class_name_field:
                    class_name = feature[class_name_field]
                    class_names[int(class_value)] = str(class_name) if class_name else f"Classe_{class_value}"
                else:
                    class_names[int(class_value)] = f"Classe_{class_value}"
        if 0 not in class_names: 
            class_names[0] = "Background"

        # 4. Configurar Output Vector (Sink)
        source_fields = tiles_source.fields()
        source_fields = [f for f in tiles_source.fields() if f.name() != "fid"]
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

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT_LAYER, context, output_fields, tiles_source.wkbType(), tiles_source.sourceCrs()
        )
        if sink is None: 
            raise QgsProcessingException("Erro ao criar camada de saída.")

        # 5. Estruturas para consolidação
        all_experiments_tile_metrics = []
        all_experiments_mi_metrics = []
        all_experiments_overall_metrics = []

        # Referência segura para layers de entrada
        mask_layer_ref = context.getMapLayer(mask_source.sourceName()) or QgsVectorLayer(mask_source.sourceName(), "mask_ref", "ogr")
        tiles_crs = tiles_source.sourceCrs()

        # 6. Loop por experimento
        num_experiments = len(segmentation_rasters)
        multiStepFeedback = QgsProcessingMultiStepFeedback(num_experiments, feedback)
        
        for exp_idx, segmentation_raster in enumerate(segmentation_rasters):
            multiStepFeedback.setCurrentStep(exp_idx)
            experiment_name = os.path.splitext(os.path.basename(segmentation_raster.source()))[0]
            
            feedback.pushInfo(f"\n{'='*80}")
            multiStepFeedback.setProgressText(f"Processando experimento {exp_idx+1}/{num_experiments}: {experiment_name}")
            feedback.pushInfo(f"Processando experimento {exp_idx+1}/{num_experiments}: {experiment_name}")
            feedback.pushInfo(f"{'='*80}\n")
            
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
                tiles_source=tiles_source,
                mask_source=mask_source,
                class_field=class_field,
                class_names=class_names,
                ground_truth_folder=ground_truth_folder,
                predicted_folder=predicted_folder,
                metrics_folder=metrics_folder,
                output_fields=output_fields,
                sorted_classes=sorted_classes,
                context=context,
                feedback=multiStepFeedback,
                tiles_crs=tiles_crs,
                mask_layer_ref=mask_layer_ref,
            )
            list(map(lambda x: sink.addFeature(x), featuresToAdd))
            # Coletar métricas para consolidação
            all_experiments_tile_metrics.extend(exp_metrics['tile_metrics'])
            all_experiments_mi_metrics.extend(exp_metrics['mi_metrics'])
            all_experiments_overall_metrics.append(exp_metrics['overall_metrics'])

        # 7. Gerar CSVs consolidados
        self._writeConsolidatedMetrics(
            output_folder=output_folder,
            tile_metrics=all_experiments_tile_metrics,
            mi_metrics_list=all_experiments_mi_metrics,
            overall_metrics_list=all_experiments_overall_metrics,
            class_names=class_names,
        )

        return {
            self.OUTPUT_FOLDER: output_folder,
            self.OUTPUT_LAYER: dest_id
        }

    def _processExperiment(
        self,
        experiment_name,
        segmentation_raster,
        tiles_source,
        mask_source,
        class_field,
        class_names,
        ground_truth_folder,
        predicted_folder,
        metrics_folder,
        output_fields,
        sorted_classes,
        context,
        feedback,
        tiles_crs,
        mask_layer_ref,
    ):
        """Processa um único experimento"""
        
        # Planejamento
        tiles_by_mi = defaultdict(dict)
        total_tiles_count = 0
        for tile_feat in tiles_source.getFeatures():
            tiles_by_mi[tile_feat["mi"]][f"{tile_feat['mi']}_{tile_feat['quadricula']}"] = tile_feat
            total_tiles_count += 1
        
        total_steps = 1 + (total_tiles_count + len(tiles_by_mi)) + 1
        multiStepFeedback = QgsProcessingMultiStepFeedback(total_steps, feedback)
        current_step_index = 0
        multiStepFeedback.setCurrentStep(current_step_index)
        current_step_index += 1

        global_counts = {}
        global_total_pixels = 0
        global_correct_pixels = 0
        mi_accumulators = defaultdict(lambda: {'counts': {}, 'total_pixels': 0, 'correct_pixels': 0})
        metrics_by_tile = []

        algRunner = AlgRunner()
        processed_count = 0
        
        max_workers = os.cpu_count() or 4
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        futures_map = {} 
        tile_data_cache = {} 
        featsToAdd = []
        output_fields_names = [f.name() for f in output_fields]

        try:
            for mi, tile_feature_dict in tiles_by_mi.items():
                if multiStepFeedback.isCanceled():
                    break
                tile_features = list(tile_feature_dict.values())
                # --- OTIMIZAÇÃO: PROCESSAMENTO EM LOTE POR MI ---
                multiStepFeedback.setCurrentStep(current_step_index)
                multiStepFeedback.pushInfo(f"Processando MI: {mi} (Preparando geometrias em lote...)")
                
                mi_gt_folder = os.path.join(ground_truth_folder, mi)
                mi_pred_folder = os.path.join(predicted_folder, mi)
                os.makedirs(mi_gt_folder, exist_ok=True)
                os.makedirs(mi_pred_folder, exist_ok=True)

                fuso_utm = tile_features[0]["fuso_utm"]
                utm_crs = QgsCoordinateReferenceSystem(fuso_utm)
                if not utm_crs.isValid():
                    multiStepFeedback.reportError(f"Fuso UTM inválido. Pulando MI {mi}.")
                    current_step_index += 1 + len(tile_features)
                    continue

                # 1. Criar camada temporária com TODOS os tiles deste MI
                mi_tiles_layer = QgsVectorLayer(f"Polygon?crs={tiles_crs.authid()}", f"tiles_{mi}", "memory")
                miDataProvider = mi_tiles_layer.dataProvider()
                miDataProvider.addAttributes(tile_features[0].fields())
                mi_tiles_layer.updateFields()
                mi_tiles_layer.dataProvider().addFeatures(tile_features)
                
                # 2. Preparar Máscara e Tiles (REPROJEÇÃO EM LOTE)
                reprojected_tiles_layer = algRunner.runReprojectLayer(
                    layer=mi_tiles_layer, targetCrs=utm_crs, context=context, feedback=multiStepFeedback
                )
                algRunner.runCreateSpatialIndex(reprojected_tiles_layer, context=context)
                
                # Recortar e Reprojetar Máscara Global para o MI
                mi_extent_utm = reprojected_tiles_layer.extent()
                xform_utm_to_mask = QgsCoordinateTransform(utm_crs, mask_source.sourceCrs(), QgsProject.instance())
                mi_extent_mask_crs = xform_utm_to_mask.transformBoundingBox(mi_extent_utm)
                
                mask_clipped_layer = algRunner.runExtractByExtent(
                    inputLayer=mask_layer_ref, extent=mi_extent_mask_crs, context=context, feedback=multiStepFeedback
                )
                
                reprojected_mask_layer = algRunner.runReprojectLayer(
                    layer=mask_clipped_layer, targetCrs=utm_crs, context=context, feedback=multiStepFeedback
                )
                
                algRunner.runCreateSpatialIndex(reprojected_mask_layer, context=context)
                intersected_layer = algRunner.runClip(
                    inputLayer=reprojected_mask_layer,
                    overlayLayer=reprojected_tiles_layer,
                    context=context,
                    feedback=multiStepFeedback
                )
                
                intersected_layer = algRunner.runJoinAttributesByLocation(
                    inputLyr=intersected_layer,
                    joinLyr=reprojected_tiles_layer,
                    predicateList=[0],
                    method=1,
                    context=context,
                    feedback=multiStepFeedback,
                )

                # 4. Construir Dicionário de Formas (Memória)
                gt_shapes_by_tile = defaultdict(list)
                
                for feat in intersected_layer.getFeatures():
                    v_class = feat[class_field]
                    v_quad = feat["quadricula"]
                    
                    if v_class is not None and v_quad:
                        tile_id_key = f"{mi}_{v_quad}"
                        try:
                            geom_json = json.loads(feat.geometry().asJson())
                            gt_shapes_by_tile[tile_id_key].append((geom_json, int(v_class)))
                        except:
                            pass
                            
                # --- FIM DA OTIMIZAÇÃO VETORIAL ---

                # Raster Prep (AlgRunner)
                seg_raster_crs = segmentation_raster.crs()
                combined_extent = reprojected_tiles_layer.extent()

                if utm_crs != seg_raster_crs:
                     xform_utm_to_raster = QgsCoordinateTransform(utm_crs, seg_raster_crs, QgsProject.instance())
                     extent_raster_crs = xform_utm_to_raster.transformBoundingBox(combined_extent)
                else:
                    extent_raster_crs = combined_extent
                
                buf_x, buf_y = extent_raster_crs.width()*0.1, extent_raster_crs.height()*0.1
                buffered_extent = QgsRectangle(
                    extent_raster_crs.xMinimum()-buf_x, 
                    extent_raster_crs.yMinimum()-buf_y, 
                    extent_raster_crs.xMaximum()+buf_x, 
                    extent_raster_crs.yMaximum()+buf_y
                )

                # Clip Raster
                clipped_raster = algRunner.runRasterClipByExtent(
                    inputRaster=segmentation_raster, extent=buffered_extent, nodata=None, context=context, feedback=multiStepFeedback
                )
                if isinstance(clipped_raster, str): 
                    pass 
                elif hasattr(clipped_raster, 'source'): 
                    clipped_raster = clipped_raster.source()

                # Warp Raster
                if seg_raster_crs != utm_crs:
                    reprojected_raster = algRunner.runGdalWarp(
                        rasterLayer=clipped_raster, targetCrs=utm_crs, context=context, resampling=0, feedback=multiStepFeedback
                    )
                else:
                    reprojected_raster = clipped_raster
                
                reprojected_raster_path = reprojected_raster if isinstance(reprojected_raster, str) else reprojected_raster.source()
                
                current_step_index += 1

                # --- LOOP DE SUBMISSÃO ---
                multiStepFeedback.pushInfo(f"Enviando tiles do MI {mi} para threads...")
                
                for tile_feat_utm in reprojected_tiles_layer.getFeatures():
                    if multiStepFeedback.isCanceled():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    
                    multiStepFeedback.setCurrentStep(current_step_index)
                    
                    quadricula = tile_feat_utm["quadricula"]
                    tile_id = f"{mi}_{quadricula}"

                    try:
                        tile_geom_json = json.loads(tile_feat_utm.geometry().asJson())
                        gt_shapes = gt_shapes_by_tile.get(tile_id, [])

                        task_data = {
                            'mi': mi, 
                            'quadricula': quadricula,
                            'raster_path': reprojected_raster_path,
                            'tile_geom': tile_geom_json,
                            'gt_shapes': gt_shapes,
                            'pred_path': os.path.join(mi_pred_folder, f"{tile_id}.tif"),
                            'gt_path': os.path.join(mi_gt_folder, f"{tile_id}.tif"),
                            'nodata': 255, 
                            'class_names': class_names
                        }
                        
                        future = executor.submit(process_tile_worker, task_data)
                        futures_map[future] = tile_id
                        
                    except Exception as e:
                        multiStepFeedback.reportError(f"Erro tile {quadricula}: {e}")

                    current_step_index += 1
                
                # Limpeza de memória do MI
                mi_tiles_layer = None
                reprojected_tiles_layer = None
                mask_clipped_layer = None
                reprojected_mask_layer = None
                intersected_layer = None

            # --- Collect Results ---
            multiStepFeedback.pushInfo(f"\nColetando resultados...")
            
            for future in concurrent.futures.as_completed(futures_map):
                tile_id = futures_map[future]
                if multiStepFeedback.isCanceled():
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                
                try:
                    result = future.result()
                    if result['status'] == 'success':
                        m = result['metrics']
                        raw = m.pop("raw_counts", {})
                        self._updateCounts(global_counts, raw)
                        self._updateCounts(mi_accumulators[result['mi']]['counts'], raw)
                        
                        t_px, c_px = m.get("total_pixels", 0), m.get("correct_pixels", 0)
                        global_total_pixels += t_px
                        global_correct_pixels += c_px
                        mi_accumulators[result['mi']]['total_pixels'] += t_px
                        mi_accumulators[result['mi']]['correct_pixels'] += c_px
                        
                        m.update({
                            "experiment": experiment_name,
                            "mi": result['mi'], 
                            "quadricula": result['quadricula'], 
                            "tile_id": tile_id
                        })
                        metrics_by_tile.append(m)
                        processed_count += 1

                        # --- GRAVAR NO SINK ---
                        tile_data_cache = tiles_by_mi.get(result['mi'], {})
                        if tile_id in tile_data_cache:
                            cached = tile_data_cache[tile_id]
                            new_feat = QgsFeature(output_fields)
                            new_feat.setGeometry(cached.geometry())
                            
                            for field in cached.fields():
                                if field.name() not in output_fields_names:
                                    continue
                                new_feat[field.name()] = cached[field.name()]
                            
                            new_feat.setAttribute("experimento", experiment_name)
                            new_feat.setAttribute("gt_path", result['gt_path'])
                            new_feat.setAttribute("pred_path", result['pred_path'])
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

                            featsToAdd.append(new_feat)

                    else:
                        multiStepFeedback.reportError(f"Erro no worker {tile_id}: {result.get('error')}")

                except Exception as exc:
                    multiStepFeedback.reportError(f"Exceção {tile_id}: {exc}")

        finally:
            executor.shutdown(wait=False)

        # --- Final Report ---
        multiStepFeedback.setCurrentStep(total_steps - 1)
        global_metrics = self._calculateFinalMetricsFromCounts(
            global_counts, global_correct_pixels, global_total_pixels, class_names
        )
        global_metrics['experiment_name'] = experiment_name
        global_metrics.update({"num_tiles": processed_count, "num_mis": len(mi_accumulators)})

        multiStepFeedback.pushInfo("\n" + "="*80)
        multiStepFeedback.pushInfo(f"RESUMO {experiment_name} ({processed_count} tiles)")
        multiStepFeedback.pushInfo("-" * 80)
        multiStepFeedback.pushInfo(f"Acurácia Global:   {global_metrics.get('accuracy', 0):.2%}")
        multiStepFeedback.pushInfo(f"Mean IoU:          {global_metrics.get('mean_iou', 0):.4f}")
        multiStepFeedback.pushInfo(f"Mean F1-Score:     {global_metrics.get('f1_score', 0):.4f}")
        multiStepFeedback.pushInfo("="*80 + "\n")

        # Export CSVs por experimento
        self._write_csv_safe(
            os.path.join(metrics_folder, "metrics_per_tile.csv"), 
            metrics_by_tile
        )
        
        mi_list = []
        for mi, data in mi_accumulators.items():
            mm = self._calculateFinalMetricsFromCounts(
                data['counts'], data['correct_pixels'], data['total_pixels'], class_names
            )
            mm['experiment'] = experiment_name
            mm['mi'] = mi
            mi_list.append(mm)
        
        self._write_csv_safe(
            os.path.join(metrics_folder, "metrics_per_mi.csv"), 
            mi_list
        )
        
        self._write_csv_safe(
            os.path.join(metrics_folder, "metrics_overall.csv"), 
            [global_metrics]
        )

        return {
            'tile_metrics': metrics_by_tile,
            'mi_metrics': mi_list,
            'overall_metrics': global_metrics
        }, featsToAdd

    def _updateCounts(self, acc, new):
        for c, m in new.items():
            if c not in acc: 
                acc[c] = {'tp': 0, 'fp': 0, 'fn': 0}
            acc[c]['tp'] += m['tp']
            acc[c]['fp'] += m['fp']
            acc[c]['fn'] += m['fn']
        return acc

    def _calculateFinalMetricsFromCounts(self, counts, correct, total, names):
        if total == 0: 
            return {}
        m = {"accuracy": correct / total}
        ious, f1s, precs, recs = [], [], [], []
        
        for c in sorted(counts.keys()):
            v = counts[c]
            tp, fp, fn = v['tp'], v['fp'], v['fn']
            u = tp + fp + fn
            iou = tp/u if u>0 else 0
            p = tp/(tp+fp) if (tp+fp)>0 else 0
            r = tp/(tp+fn) if (tp+fn)>0 else 0
            f1 = 2*(p*r)/(p+r) if (p+r)>0 else 0
            
            ious.append(iou)
            f1s.append(f1)
            precs.append(p)
            recs.append(r)
            
            k = f"class_{c}_{names.get(c, f'C_{c}')}"
            m[f"{k}_iou"] = iou
            m[f"{k}_precision"] = p
            m[f"{k}_recall"] = r
            m[f"{k}_f1_score"] = f1
            
        m["mean_iou"] = sum(ious)/len(ious) if ious else 0
        m["f1_score"] = sum(f1s)/len(f1s) if f1s else 0
        m["precision"] = sum(precs)/len(precs) if precs else 0
        m["recall"] = sum(recs)/len(recs) if recs else 0
        return m

    def _write_csv_safe(self, path, data_list):
        if not data_list: 
            return
        all_keys = set().union(*(d.keys() for d in data_list))
        priority = ["experiment", "mi", "quadricula", "tile_id", "class_id", "class_name", 
                    "accuracy", "mean_iou", "precision", "recall", "f1_score", "iou", "num_tiles", "num_mis"]
        header = [k for k in priority if k in all_keys] + sorted([k for k in all_keys if k not in priority])
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(data_list)

    def _writeConsolidatedMetrics(self, output_folder, tile_metrics, mi_metrics_list, overall_metrics_list, class_names):
        """Escreve CSVs consolidados no formato esperado"""
        
        # consolidated_all_metrics.csv (overall de todos experimentos)
        consolidated_overall = []
        for metrics in overall_metrics_list:
            row = {
                'experiment': metrics.get('experiment_name', ''),
                'num_tiles': metrics.get('num_tiles', 0),
                'num_mis': metrics.get('num_mis', 0),
                'accuracy': metrics.get('accuracy', 0),
                'mean_iou': metrics.get('mean_iou', 0),
                'precision': metrics.get('precision', 0),
                'recall': metrics.get('recall', 0),
                'f1_score': metrics.get('f1_score', 0),
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
        
        self._write_csv_safe(
            os.path.join(output_folder, "consolidated_all_metrics.csv"),
            consolidated_overall
        )
        
        # per_class_metrics.csv (agregado por classe através de todos experimentos)
        per_class_consolidated = []
        for metrics in overall_metrics_list:
            exp_name = metrics.get('experiment_name', '')
            for cls_id in sorted(class_names.keys()):
                c_name = class_names[cls_id]
                prefix = f"class_{cls_id}_{c_name}"
                
                row = {
                    'experiment': exp_name,
                    'class_id': cls_id,
                    'class_name': c_name,
                    'iou': metrics.get(f"{prefix}_iou", 0),
                    'precision': metrics.get(f"{prefix}_precision", 0),
                    'recall': metrics.get(f"{prefix}_recall", 0),
                    'f1_score': metrics.get(f"{prefix}_f1_score", 0),
                }
                per_class_consolidated.append(row)
        
        self._write_csv_safe(
            os.path.join(output_folder, "per_class_metrics.csv"),
            per_class_consolidated
        )
        
        # Tile metrics consolidados (todos os tiles de todos experimentos)
        self._write_csv_safe(
            os.path.join(output_folder, "consolidated_tile_metrics.csv"),
            tile_metrics
        )
        
        # MI metrics consolidados
        self._write_csv_safe(
            os.path.join(output_folder, "consolidated_mi_metrics.csv"),
            mi_metrics_list
        )


def process_tile_worker(data):
    try:
        import rasterio
        from rasterio.mask import mask
        from rasterio.features import rasterize
        from DsgTools.core.GeometricTools.rasterHandler import calculateSegmentationMetrics
        
        reprojected_raster_path = data['raster_path']
        tile_mask_geom = data['tile_geom']
        gt_shapes = data['gt_shapes']
        predicted_path = data['pred_path']
        gt_path = data['gt_path']
        nodata = data['nodata']
        class_names = data['class_names']
        
        # 1. CLIP DO RASTER PREDITO
        with rasterio.open(reprojected_raster_path) as src:
            out_image, out_transform = mask(src, [tile_mask_geom], crop=True, nodata=nodata)
            out_meta = src.meta.copy()
            
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": nodata,
            "compress": "lzw"
        })
        
        with rasterio.open(predicted_path, "w", **out_meta) as dest:
            dest.write(out_image)
            
        # 2. RASTERIZAR GROUND TRUTH
        height, width = out_image.shape[1], out_image.shape[2]
        
        if not gt_shapes:
            raster_array = np.full((height, width), nodata, dtype=np.uint8)
        else:
            raster_array = rasterize(
                shapes=gt_shapes,
                out_shape=(height, width),
                transform=out_transform,
                fill=nodata,
                dtype=np.uint8, 
                all_touched=True
            )
            
        with rasterio.open(gt_path, 'w', driver='GTiff', height=height, width=width,
                           count=1, dtype=raster_array.dtype, crs=out_meta['crs'], 
                           transform=out_transform, nodata=nodata, compress='lzw') as dst:
            dst.write(raster_array, 1)

        # 3. CALCULAR MÉTRICAS
        metrics = calculateSegmentationMetrics(gt_path, predicted_path, nodata, class_names)
        
        return {
            'status': 'success',
            'mi': data['mi'],
            'quadricula': data['quadricula'],
            'metrics': metrics,
            'gt_path': gt_path,
            'pred_path': predicted_path
        }

    except Exception as e:
        return {
            'status': 'error', 
            'mi': data['mi'], 
            'quadricula': data['quadricula'], 
            'error': str(e)
        }
