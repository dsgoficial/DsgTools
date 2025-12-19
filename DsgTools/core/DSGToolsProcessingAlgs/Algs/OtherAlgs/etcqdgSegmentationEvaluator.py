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
    QgsProcessingParameterRasterLayer,
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
        Gera máscaras de segmentação e avalia métricas comparando com inferência.
        
        A máscara inferida é considerada o resultado de uma rede neural.
        As máscaras geradas são a verdade de campo (ground truth).
        
        IMPORTANTE: 
        - nodata = 255 (pixels ignorados)
        - classe 0 = Background (incluída nas métricas)
        
        Estrutura de saída:
        - ground_truth/{MI}/{MI}_{quadricula}.tif: Máscaras geradas
        - predicted_tiles/{MI}/{MI}_{quadricula}.tif: Inferência clipada
        - metrics/: CSVs com métricas de avaliação
        
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
        
        Métricas exportadas (3 CSVs):
        - metrics_per_tile.csv: Métricas gerais e por classe para cada tile
        - metrics_per_mi.csv: Métricas agregadas por MI
        - metrics_overall.csv: Métricas do conjunto completo
        
        Parâmetros:
        - Quadrículas: ET-CQDG (campos: mi, quadricula, fuso_utm)
        - Camada de Máscaras: Polígonos com classes (ground truth)
        - Campo de Classe: Campo inteiro com valores de classe (0 = Background)
        - Campo com Nome da Classe: Campo com nomes descritivos (padrão: class_name)
        - Máscara Inferida: Resultado da segmentação (será comparado com ground truth)
        - Pasta de Destino: Onde salvar tudo (ground_truth/, predicted_tiles/, metrics/)
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
            QgsProcessingParameterRasterLayer(
                self.SEGMENTATION_RASTER,
                self.tr("Máscara Inferida (Resultado da Segmentação)"),
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
        segmentation_raster = self.parameterAsRasterLayer(parameters, self.SEGMENTATION_RASTER, context)
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        # 2. Setup Pastas
        if not os.path.exists(output_folder): os.makedirs(output_folder)
        ground_truth_folder = os.path.join(output_folder, "ground_truth")
        predicted_folder = os.path.join(output_folder, "predicted_tiles")
        metrics_folder = os.path.join(output_folder, "metrics")
        for folder in [ground_truth_folder, predicted_folder, metrics_folder]:
            os.makedirs(folder, exist_ok=True)

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
        if 0 not in class_names: class_names[0] = "Background"

        # 4. Configurar Output Vector (Sink)
        source_fields = tiles_source.fields()
        output_fields = QgsFields(source_fields)
        
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
        if sink is None: raise QgsProcessingException("Erro ao criar camada de saída.")

        # 5. Planejamento
        tiles_by_mi = defaultdict(list)
        total_tiles_count = 0
        for tile_feat in tiles_source.getFeatures():
            tiles_by_mi[tile_feat["mi"]].append(tile_feat)
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

        tiles_crs = tiles_source.sourceCrs()
        
        # Referência segura para layers de entrada
        mask_layer_ref = context.getMapLayer(mask_source.sourceName()) or QgsVectorLayer(mask_source.sourceName(), "mask_ref", "ogr")

        algRunner = AlgRunner()
        processed_count = 0
        
        max_workers = os.cpu_count() or 4
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        futures_map = {} 
        tile_data_cache = {} 

        try:
            for mi, tile_features in tiles_by_mi.items():
                if multiStepFeedback.isCanceled():
                    break

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
                # Reprojetar Tiles do MI para UTM (1 chamada)
                reprojected_tiles_layer = algRunner.runReprojectLayer(
                    layer=mi_tiles_layer, targetCrs=utm_crs, context=context, feedback=multiStepFeedback
                )
                algRunner.runCreateSpatialIndex(reprojected_tiles_layer, context=context)
                
                # Recortar e Reprojetar Máscara Global para o MI (1 chamada de Extract, 1 de Reproject)
                # Usamos extract by extent para pegar só o que interessa da máscara global
                mi_extent_utm = reprojected_tiles_layer.extent()
                # Precisamos transformar o extent para o CRS da máscara para fazer o filtro inicial
                xform_utm_to_mask = QgsCoordinateTransform(utm_crs, mask_source.sourceCrs(), QgsProject.instance())
                mi_extent_mask_crs = xform_utm_to_mask.transformBoundingBox(mi_extent_utm)
                
                # Filtra máscara global para a área do MI
                mask_clipped_layer = algRunner.runExtractByExtent(
                    inputLayer=mask_layer_ref, extent=mi_extent_mask_crs, context=context, feedback=multiStepFeedback
                )
                
                # Reprojeta máscara filtrada para UTM
                reprojected_mask_layer = algRunner.runReprojectLayer(
                    layer=mask_clipped_layer, targetCrs=utm_crs, context=context, feedback=multiStepFeedback
                )
                
                algRunner.runCreateSpatialIndex(reprojected_mask_layer, context=context)
                intersected_layer = algRunner.runExtractByLocation(
                    inputLyr=reprojected_mask_layer,
                    intersectLyr=reprojected_tiles_layer,
                    context=context,
                    predicate=[0],
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
                # Agrupa polígonos por tile_id para acesso O(1) no loop
                gt_shapes_by_tile = defaultdict(list)
                
                for feat in intersected_layer.getFeatures():
                    v_class = feat[class_field]
                    v_quad = feat["quadricula"]
                    
                    if v_class is not None and v_quad:
                        tile_id_key = f"{mi}_{v_quad}"
                        try:
                            # Guarda geometria como GeoJSON para a thread
                            geom_json = json.loads(feat.geometry().asJson())
                            gt_shapes_by_tile[tile_id_key].append((geom_json, int(v_class)))
                        except:
                            pass
                            
                # --- FIM DA OTIMIZAÇÃO VETORIAL ---

                # Raster Prep (AlgRunner - Mantido conforme pedido)
                seg_raster_crs = segmentation_raster.crs()
                combined_extent = reprojected_tiles_layer.extent() # Já temos o extent em UTM

                # O AlgRunner espera extent no CRS do raster de entrada para o Clip
                if utm_crs != seg_raster_crs:
                     xform_utm_to_raster = QgsCoordinateTransform(utm_crs, seg_raster_crs, QgsProject.instance())
                     extent_raster_crs = xform_utm_to_raster.transformBoundingBox(combined_extent)
                else:
                    extent_raster_crs = combined_extent
                
                buf_x, buf_y = extent_raster_crs.width()*0.1, extent_raster_crs.height()*0.1
                buffered_extent = QgsRectangle(extent_raster_crs.xMinimum()-buf_x, extent_raster_crs.yMinimum()-buf_y, extent_raster_crs.xMaximum()+buf_x, extent_raster_crs.yMaximum()+buf_y)

                # Clip Raster
                clipped_raster = algRunner.runRasterClipByExtent(
                    inputRaster=segmentation_raster, extent=buffered_extent, nodata=None, context=context, feedback=multiStepFeedback
                )
                if isinstance(clipped_raster, str): pass 
                elif hasattr(clipped_raster, 'source'): clipped_raster = clipped_raster.source()

                # Warp Raster
                if seg_raster_crs != utm_crs:
                    reprojected_raster = algRunner.runGdalWarp(
                        rasterLayer=clipped_raster, targetCrs=utm_crs, context=context, resampling=0, feedback=multiStepFeedback
                    )
                else:
                    reprojected_raster = clipped_raster
                
                reprojected_raster_path = reprojected_raster if isinstance(reprojected_raster, str) else reprojected_raster.source()
                
                current_step_index += 1

                # --- LOOP DE SUBMISSÃO (Agora muito rápido) ---
                multiStepFeedback.pushInfo(f"Enviando tiles do MI {mi} para threads...")
                
                # Iterar sobre a camada de tiles JÁ reprojetada (para pegar a geometria de corte correta em UTM)
                for tile_feat_utm in reprojected_tiles_layer.getFeatures():
                    if multiStepFeedback.isCanceled():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    
                    multiStepFeedback.setCurrentStep(current_step_index)
                    
                    quadricula = tile_feat_utm["quadricula"]
                    tile_id = f"{mi}_{quadricula}"
                    
                    # Cache para o Sink (Atributos originais + geometria reprojetada para o sink)
                    tile_data_cache[tile_id] = {
                        'feat_geom': QgsGeometry(tile_feat_utm.geometry()), 
                        'attrs': tile_feat_utm.attributes()
                    }

                    try:
                        # Dados para Thread
                        tile_geom_json = json.loads(tile_feat_utm.geometry().asJson())
                        
                        # Recuperar máscaras do dicionário (O(1))
                        # Não há mais ExtractByLocation aqui!
                        gt_shapes = gt_shapes_by_tile.get(tile_id, [])

                        task_data = {
                            'mi': mi, 'quadricula': quadricula,
                            'raster_path': reprojected_raster_path,
                            'tile_geom': tile_geom_json,
                            'gt_shapes': gt_shapes,
                            'pred_path': os.path.join(mi_pred_folder, f"{tile_id}.tif"),
                            'gt_path': os.path.join(mi_gt_folder, f"{tile_id}.tif"),
                            'nodata': 255, 'class_names': class_names
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
                        # Accumulate
                        raw = m.pop("raw_counts", {})
                        self._updateCounts(global_counts, raw)
                        self._updateCounts(mi_accumulators[result['mi']]['counts'], raw)
                        
                        t_px, c_px = m.get("total_pixels", 0), m.get("correct_pixels", 0)
                        global_total_pixels += t_px; global_correct_pixels += c_px
                        mi_accumulators[result['mi']]['total_pixels'] += t_px
                        mi_accumulators[result['mi']]['correct_pixels'] += c_px
                        
                        m.update({"mi": result['mi'], "quadricula": result['quadricula'], "tile_id": tile_id})
                        metrics_by_tile.append(m)
                        processed_count += 1

                        # --- GRAVAR NO SINK ---
                        if tile_id in tile_data_cache:
                            cached = tile_data_cache[tile_id]
                            new_feat = QgsFeature(output_fields)
                            new_feat.setGeometry(cached['feat_geom'])
                            
                            # Cuidado: atributos do cache vieram do tile reprojetado.
                            # Precisamos garantir mapeamento correto se a ordem mudou ou usar nome
                            # Simplificação: copiamos os atributos na ordem do output fields que foi baseado no input
                            # Como reprojetamos apenas geometria, os atributos devem estar alinhados
                            for i, attr in enumerate(cached['attrs']):
                                # Proteção de índice caso reprojeção altere colunas (geralmente não altera)
                                if i < len(output_fields):
                                    new_feat.setAttribute(i, attr)
                            
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

                            sink.addFeature(new_feat)

                    else:
                        multiStepFeedback.reportError(f"Erro no worker {tile_id}: {result.get('error')}")

                except Exception as exc:
                    multiStepFeedback.reportError(f"Exceção {tile_id}: {exc}")

        finally:
            executor.shutdown(wait=False)

        # --- Final Report Completo (Todas as Métricas) ---
        multiStepFeedback.setCurrentStep(total_steps - 1)
        global_metrics = self._calculateFinalMetricsFromCounts(global_counts, global_correct_pixels, global_total_pixels, class_names)

        multiStepFeedback.pushInfo("\n" + "="*80)
        multiStepFeedback.pushInfo(f"RESUMO FINAL ({processed_count} tiles)")
        multiStepFeedback.pushInfo("-" * 80)
        
        # Métricas Globais Formatadas
        multiStepFeedback.pushInfo(f"Acurácia Global:   {global_metrics.get('accuracy', 0):.2%}")
        multiStepFeedback.pushInfo(f"Mean IoU:          {global_metrics.get('mean_iou', 0):.4f}")
        multiStepFeedback.pushInfo(f"Mean F1-Score:     {global_metrics.get('f1_score', 0):.4f}")
        multiStepFeedback.pushInfo(f"Mean Precision:    {global_metrics.get('precision', 0):.4f}")
        multiStepFeedback.pushInfo(f"Mean Recall:       {global_metrics.get('recall', 0):.4f}")
        
        # Tabela Detalhada Por Classe
        lines = []
        lines.append("-" * 80)
        lines.append(f"{'CLASSE':<30} | {'IoU':>8} | {'F1':>8} | {'PRECISION':>8} | {'RECALL':>8}")
        lines.append("-" * 80)

        for cls_id in sorted(class_names.keys()):
            c_name = class_names[cls_id]
            display_name = f"{cls_id}-{c_name}"
            if len(display_name) > 29:
                display_name = display_name[:26] + "..."
            
            prefix = f"class_{cls_id}_{c_name}"
            
            iou = global_metrics.get(f"{prefix}_iou", 0)
            f1 = global_metrics.get(f"{prefix}_f1_score", 0)
            prec = global_metrics.get(f"{prefix}_precision", 0)
            rec = global_metrics.get(f"{prefix}_recall", 0)
            
            lines.append(f"{display_name:<30} | {iou:>8.4f} | {f1:>8.4f} | {prec:>8.4f} | {rec:>8.4f}")

        lines.append("=" * 80)
        multiStepFeedback.pushInfo("\n".join(lines))
            
        multiStepFeedback.pushInfo("="*80 + "\n")

        # Export CSVs (Mantido)
        def write_csv_safe(path, data_list):
            if not data_list: return
            all_keys = set().union(*(d.keys() for d in data_list))
            priority = ["mi", "quadricula", "tile_id", "accuracy", "mean_iou"]
            header = [k for k in priority if k in all_keys] + sorted([k for k in all_keys if k not in priority])
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data_list)

        if metrics_by_tile: write_csv_safe(os.path.join(metrics_folder, "metrics_per_tile.csv"), metrics_by_tile)
        
        mi_list = []
        for mi, data in mi_accumulators.items():
            mm = self._calculateFinalMetricsFromCounts(data['counts'], data['correct_pixels'], data['total_pixels'], class_names)
            mm['mi'] = mi
            mi_list.append(mm)
        write_csv_safe(os.path.join(metrics_folder, "metrics_per_mi.csv"), mi_list)
        
        global_metrics.update({"num_tiles": processed_count, "num_mis": len(mi_accumulators)})
        write_csv_safe(os.path.join(metrics_folder, "metrics_overall.csv"), [global_metrics])

        return {
            self.OUTPUT_FOLDER: output_folder,
            self.OUTPUT_LAYER: dest_id
        }

    def _updateCounts(self, acc, new):
        for c, m in new.items():
            if c not in acc: acc[c] = {'tp': 0, 'fp': 0, 'fn': 0}
            acc[c]['tp'] += m['tp']; acc[c]['fp'] += m['fp']; acc[c]['fn'] += m['fn']
        return acc

    def _calculateFinalMetricsFromCounts(self, counts, correct, total, names):
        if total == 0: return {}
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
            
            ious.append(iou); f1s.append(f1); precs.append(p); recs.append(r)
            
            k = f"class_{c}_{names.get(c, f'C_{c}')}"
            m[f"{k}_iou"] = iou; m[f"{k}_precision"] = p
            m[f"{k}_recall"] = r; m[f"{k}_f1_score"] = f1
            
        m["mean_iou"] = sum(ious)/len(ious) if ious else 0
        m["f1_score"] = sum(f1s)/len(f1s) if f1s else 0
        m["precision"] = sum(precs)/len(precs) if precs else 0
        m["recall"] = sum(recs)/len(recs) if recs else 0
        return m

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
        return {'status': 'error', 'mi': data['mi'], 'quadricula': data['quadricula'], 'error': str(e)}
