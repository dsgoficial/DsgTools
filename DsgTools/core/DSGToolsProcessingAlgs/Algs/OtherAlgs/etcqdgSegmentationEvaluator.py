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
from collections import defaultdict
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterFolderDestination,
    QgsProcessingException,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsVectorLayer,
    QgsProcessingContext,
    QgsRectangle,
    QgsRasterLayer,
    QgsProcessingMultiStepFeedback,
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.rasterHandler import (
    clipRasterByVectorMask,
    rasterizePolygonsToFile,
    calculateSegmentationMetrics,
)


class ETCQDGSegmentationEvaluator(QgsProcessingAlgorithm):
    """
    Avalia segmentação semântica comparando ground truth com inferência segundo ET-CQDG.
    """

    INPUT_TILES = "INPUT_TILES"
    INPUT_MASK_LAYER = "INPUT_MASK_LAYER"
    CLASS_FIELD = "CLASS_FIELD"
    CLASS_NAME_FIELD = "CLASS_NAME_FIELD"
    SEGMENTATION_RASTER = "SEGMENTATION_RASTER"
    OUTPUT_FOLDER = "OUTPUT_FOLDER"

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

    def processAlgorithm(self, parameters, context, feedback):
        # Obter parâmetros
        tiles_source = self.parameterAsSource(parameters, self.INPUT_TILES, context)
        mask_source = self.parameterAsSource(parameters, self.INPUT_MASK_LAYER, context)
        class_field = self.parameterAsString(parameters, self.CLASS_FIELD, context)
        class_name_field = self.parameterAsString(
            parameters, self.CLASS_NAME_FIELD, context
        )
        segmentation_raster = self.parameterAsRasterLayer(
            parameters, self.SEGMENTATION_RASTER, context
        )
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        # Criar estrutura de pastas
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        ground_truth_folder = os.path.join(output_folder, "ground_truth")
        predicted_folder = os.path.join(output_folder, "predicted_tiles")
        metrics_folder = os.path.join(output_folder, "metrics")

        for folder in [ground_truth_folder, predicted_folder, metrics_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        feedback.pushInfo(f"Máscara inferida: {segmentation_raster.name()}")
        feedback.pushInfo(f"Estrutura de saída criada em: {output_folder}")

        # Coletar nomes das classes dos polígonos
        class_names = {}
        
        # Verificar se o campo de nome de classe existe
        has_class_name_field = (
            class_name_field
            and class_name_field in [f.name() for f in mask_source.fields()]
        )
        
        if not has_class_name_field and class_name_field:
            feedback.pushWarning(
                f"Campo '{class_name_field}' não encontrado. "
                f"Usando valores de classe como nomes."
            )
        
        for feature in mask_source.getFeatures():
            class_value = feature[class_field]
            if class_value is not None and class_value not in class_names:
                # Obter nome da classe do campo selecionado
                if has_class_name_field:
                    class_name = feature[class_name_field]
                    if class_name:
                        class_names[int(class_value)] = str(class_name)
                    else:
                        class_names[int(class_value)] = f"Classe_{class_value}"
                else:
                    # Se não tem campo de nome, usar o valor da classe
                    class_names[int(class_value)] = f"Classe_{class_value}"
        
        # Adicionar classe 0 (background) se não estiver presente
        if 0 not in class_names:
            if has_class_name_field:
                # Tentar encontrar o nome para classe 0 nos polígonos
                for feature in mask_source.getFeatures():
                    if feature[class_field] == 0:
                        class_name = feature[class_name_field] if has_class_name_field else None
                        if class_name:
                            class_names[0] = str(class_name)
                        else:
                            class_names[0] = "Background"
                        break
                else:
                    class_names[0] = "Background"
            else:
                class_names[0] = "Background"

        feedback.pushInfo(f"Classes encontradas: {class_names}")

        # Estruturas para armazenar métricas
        global_counts = {} # {class_id: {tp, fp, fn}}
        global_total_pixels = 0
        global_correct_pixels = 0
        
        # Acumulador por MI
        mi_accumulators = defaultdict(lambda: {
            'counts': {}, 
            'total_pixels': 0, 
            'correct_pixels': 0
        })

        metrics_by_tile = []
        metrics_by_mi = defaultdict(list)

        # Obter CRS das camadas
        tiles_crs = tiles_source.sourceCrs()
        mask_crs = mask_source.sourceCrs()

        # Criar camadas temporárias para processamento
        tiles_layer = context.getMapLayer(tiles_source.sourceName())
        if tiles_layer is None:
            tiles_layer = QgsVectorLayer(
                f"Polygon?crs={tiles_crs.authid()}", "tiles_temp", "memory"
            )
            tiles_layer.dataProvider().addFeatures(list(tiles_source.getFeatures()))

        mask_layer = context.getMapLayer(mask_source.sourceName())
        if mask_layer is None:
            mask_layer = QgsVectorLayer(
                f"Polygon?crs={mask_crs.authid()}", "mask_temp", "memory"
            )
            mask_layer.dataProvider().addFeatures(list(mask_source.getFeatures()))

        # Validar campos necessários
        tiles_fields = [field.name() for field in tiles_source.fields()]
        required_fields = ["mi", "quadricula", "fuso_utm"]
        for field in required_fields:
            if field not in tiles_fields:
                raise QgsProcessingException(
                    f'Campo "{field}" não encontrado na camada de quadrículas'
                )

        mask_fields = [field.name() for field in mask_source.fields()]
        if class_field not in mask_fields:
            raise QgsProcessingException(
                f'Campo "{class_field}" não encontrado na camada de máscaras'
            )

        # Agrupar tiles por MI
        tiles_by_mi = defaultdict(list)
        for tile_feat in tiles_source.getFeatures():
            mi = tile_feat["mi"]
            tiles_by_mi[mi].append(tile_feat)

        feedback.pushInfo(f"Total de MIs: {len(tiles_by_mi)}")

        algRunner = AlgRunner()
        total_tiles = tiles_source.featureCount()
        processed = 0

        # Processar cada MI
        # multiStepFeedback = QgsProcessingMultiStepFeedback(total_tiles, feedback)
        for mi, tile_features in tiles_by_mi.items():
            if feedback.isCanceled():
                break

            feedback.pushInfo(f"\nProcessando MI: {mi} ({len(tile_features)} tiles)")

            # Criar subpastas para o MI em ground_truth e predicted_tiles
            mi_gt_folder = os.path.join(ground_truth_folder, mi)
            mi_pred_folder = os.path.join(predicted_folder, mi)

            for folder in [mi_gt_folder, mi_pred_folder]:
                if not os.path.exists(folder):
                    os.makedirs(folder)

            feedback.pushInfo(f"  Criadas pastas para MI: {mi}")

            # Obter fuso UTM do primeiro tile
            fuso_utm = tile_features[0]["fuso_utm"]
            utm_crs = QgsCoordinateReferenceSystem(fuso_utm)
            if not utm_crs.isValid():
                feedback.pushWarning(
                    f"  Fuso UTM inválido: {fuso_utm}. Pulando MI {mi}"
                )
                continue

            feedback.pushInfo(f"  Fuso UTM: {fuso_utm}")

            # Obter CRS do raster de segmentação
            seg_raster_crs = segmentation_raster.crs()
            feedback.pushInfo(f"  CRS do raster de segmentação: {seg_raster_crs.authid()}")

            # Calcular extent combinado de todos os tiles do MI (no CRS original)
            combined_extent = QgsRectangle()
            combined_extent.setMinimal()
            for tile_feat in tile_features:
                tile_geom = tile_feat.geometry()
                combined_extent.combineExtentWith(tile_geom.boundingBox())

            # Transformar extent para o CRS do raster de segmentação
            if tiles_crs != seg_raster_crs:
                transform_to_raster = QgsCoordinateTransform(
                    tiles_crs, seg_raster_crs, QgsProject.instance()
                )
                combined_extent = transform_to_raster.transformBoundingBox(combined_extent)
                feedback.pushInfo(
                    f"  Extent transformado para {seg_raster_crs.authid()}: "
                    f"{combined_extent.toString()}"
                )

            # Adicionar buffer de 10% ao extent
            buffer_x = combined_extent.width() * 0.1
            buffer_y = combined_extent.height() * 0.1
            buffered_extent = QgsRectangle(
                combined_extent.xMinimum() - buffer_x,
                combined_extent.yMinimum() - buffer_y,
                combined_extent.xMaximum() + buffer_x,
                combined_extent.yMaximum() + buffer_y,
            )

            feedback.pushInfo(f"  Clipando raster de segmentação...")

            # Clipar raster com o extent combinado (agora no CRS correto)
            clipped_raster = algRunner.runRasterClipByExtent(
                inputRaster=segmentation_raster,
                extent=buffered_extent,
                nodata=None,
                context=context,
                feedback=feedback,
                is_child_algorithm=False,
            )

            feedback.pushInfo(f"  Raster clipado com sucesso")

            # Verificar se precisa reprojetar para UTM
            if seg_raster_crs != utm_crs:
                feedback.pushInfo(f"  Reprojetando raster para {fuso_utm}...")

                reprojected_raster = algRunner.runGdalWarp(
                    rasterLayer=clipped_raster,
                    targetCrs=utm_crs,
                    context=context,
                    resampling=0,  # Nearest neighbor para preservar valores de classe
                    feedback=feedback,
                    is_child_algorithm=False,
                )
            else:
                feedback.pushInfo(f"  Raster já está no CRS correto (UTM)")
                reprojected_raster = clipped_raster

            # Obter pixel size do raster reprojetado usando rasterio
            try:
                import rasterio
            except ImportError:
                raise QgsProcessingException(
                    "A biblioteca 'rasterio' não está instalada. "
                    "Instale com: pip install rasterio"
                )

            reprojected_raster_path = (
                reprojected_raster
                if isinstance(reprojected_raster, str)
                else reprojected_raster.source()
            )

            with rasterio.open(reprojected_raster_path) as src:
                pixel_size_x, pixel_size_y = src.res
                pixel_size = abs(pixel_size_x)  # Usar valor absoluto

            feedback.pushInfo(
                f"  Tamanho do pixel no UTM: {pixel_size:.6f} metros "
                f"(X: {pixel_size_x:.6f}, Y: {pixel_size_y:.6f})"
            )

            # Processar cada tile do MI
            for tile_feat in tile_features:
                if feedback.isCanceled():
                    break

                processed += 1
                feedback.setProgress(int(processed * 100 / total_tiles))

                quadricula = tile_feat["quadricula"]
                feedback.pushInfo(f"  Processando tile {quadricula}")

                # Inicializar variáveis para garantir limpeza no finally
                tile_layer = None
                intersected_layer = None
                reprojected_mask = None
                reprojected_tile = None

                try:
                    # 1. Criar camada temporária do tile
                    tile_layer = QgsVectorLayer(
                        f"Polygon?crs={tiles_crs.authid()}", "single_tile", "memory"
                    )
                    tile_layer.dataProvider().addFeatures([tile_feat])

                    # 2. Extrair polígonos (Intersect)
                    intersected_layer = algRunner.runExtractByLocation(
                        inputLyr=mask_layer,
                        intersectLyr=tile_layer,
                        context=context,
                        predicate=[0],  # Intersects
                        feedback=feedback,
                        is_child_algorithm=False,
                    )

                    # Verificar se a camada intermediária é válida
                    if intersected_layer is None or not intersected_layer.isValid():
                         # Pode acontecer se não houver interseção ou erro no algRunner
                        if intersected_layer is None or intersected_layer.featureCount() == 0:
                            feedback.pushInfo(f"    Nenhum polígono intersecta o tile {quadricula}")
                            continue
                        else:
                            raise QgsProcessingException("Erro ao criar camada de interseção (camada inválida).")

                    if intersected_layer.featureCount() == 0:
                        feedback.pushInfo(f"    Nenhum polígono intersecta o tile {quadricula}")
                        continue

                    # 3. Reprojetar MÁSCARA para UTM
                    reprojected_mask = algRunner.runReprojectLayer(
                        layer=intersected_layer,
                        targetCrs=utm_crs,
                        context=context,
                        feedback=feedback,
                        is_child_algorithm=False,
                    )
                    
                    # Checagem de segurança crítica para o erro "C++ object deleted"
                    if not reprojected_mask or not reprojected_mask.isValid():
                        raise QgsProcessingException(f"Falha ao reprojetar máscara para o tile {quadricula}")

                    # 4. Reprojetar TILE para UTM (para clipar o raster)
                    reprojected_tile = algRunner.runReprojectLayer(
                        layer=tile_layer,
                        targetCrs=utm_crs,
                        context=context,
                        feedback=feedback,
                        is_child_algorithm=False,
                    )

                    # --- Bloco de Geração de Rasters ---

                    # A. Clipar Raster Predito
                    predicted_filename = f"{mi}_{quadricula}.tif"
                    predicted_path = os.path.join(mi_pred_folder, predicted_filename)
                    
                    clipRasterByVectorMask(
                        input_raster_path=reprojected_raster_path,
                        mask_layer=reprojected_tile,
                        output_path=predicted_path,
                        nodata_value=255,
                    )

                    # Ler metadados do predito
                    with rasterio.open(predicted_path) as pred_src:
                        pred_width = pred_src.width
                        pred_height = pred_src.height
                        pred_transform = pred_src.transform

                    # B. Rasterizar Ground Truth (Onde o erro ocorria)
                    output_filename = f"{mi}_{quadricula}.tif"
                    output_path = os.path.join(mi_gt_folder, output_filename)

                    # Passamos a camada reprojected_mask que validamos acima
                    rasterizePolygonsToFile(
                        vectorLayer=reprojected_mask,
                        classField=class_field,
                        outputPath=output_path,
                        crs=utm_crs,
                        nodataValue=255,
                        width=pred_width,
                        height=pred_height,
                        transform_affine=pred_transform,
                    )

                    # C. Calcular Métricas
                    tile_result = calculateSegmentationMetrics(
                        ground_truth_path=output_path,
                        prediction_path=predicted_path,
                        nodata_value=255,
                        class_names=class_names,
                    )

                    # Processar resultados (igual ao anterior)
                    raw_counts = tile_result.pop("raw_counts", {})
                    tile_total_pixels = tile_result.get("total_pixels", 0)
                    tile_correct_pixels = tile_result.get("correct_pixels", 0)

                    self._updateCounts(global_counts, raw_counts)
                    global_total_pixels += tile_total_pixels
                    global_correct_pixels += tile_correct_pixels

                    self._updateCounts(mi_accumulators[mi]['counts'], raw_counts)
                    mi_accumulators[mi]['total_pixels'] += tile_total_pixels
                    mi_accumulators[mi]['correct_pixels'] += tile_correct_pixels

                    tile_result["mi"] = mi
                    tile_result["quadricula"] = quadricula
                    tile_result["tile_id"] = f"{mi}_{quadricula}"
                    metrics_by_tile.append(tile_result)

                except Exception as e:
                    # Captura erros de tiles específicos e continua o processamento
                    feedback.reportError(f"    ERRO CRÍTICO no tile {quadricula}: {str(e)}")
                    import traceback
                    feedback.reportError(traceback.format_exc())
                    continue
                
                finally:
                    # LIMPEZA EXPLÍCITA DE MEMÓRIA
                    # Isso evita o erro "wrapped C/C++ object has been deleted" na próxima iteração
                    # pois removemos as referências Python, permitindo que o QGIS limpe o C++ corretamente.
                    if tile_layer: del tile_layer
                    if intersected_layer: del intersected_layer
                    if reprojected_mask: del reprojected_mask
                    if reprojected_tile: del reprojected_tile

        feedback.pushInfo(f"\nProcessamento concluído! Total de tiles: {processed}")

        # --- CALCULAR MÉTRICAS GLOBAIS REAIS (Soma de TP/FP/FN) ---
        # Usamos a função auxiliar que já existe na sua classe
        global_metrics = self._calculateFinalMetricsFromCounts(
            global_counts,
            global_correct_pixels,
            global_total_pixels,
            class_names
        )

        # --- EXIBIR NO FEEDBACK ---
        feedback.pushInfo("\n" + "="*60)
        feedback.pushInfo(f"RESUMO DA AVALIAÇÃO (Global - {processed} tiles)")
        feedback.pushInfo("="*60)
        
        # 1. Métricas Gerais
        acc = global_metrics.get('accuracy', 0)
        miou = global_metrics.get('mean_iou', 0)
        mprec = global_metrics.get('precision', 0)
        mrec = global_metrics.get('recall', 0)
        mf1 = global_metrics.get('f1_score', 0)

        feedback.pushInfo(f"Acurácia Global:   {acc:.2%}")
        feedback.pushInfo(f"Mean IoU:          {miou:.4f}")
        feedback.pushInfo(f"Mean F1-Score:     {mf1:.4f}")
        feedback.pushInfo(f"Mean Precision:    {mprec:.4f}")
        feedback.pushInfo(f"Mean Recall:       {mrec:.4f}")
        feedback.pushInfo("-" * 60)

        # 2. Métricas Por Classe
        feedback.pushInfo(f"{'CLASSE':<30} | {'IoU':<8} | {'F1':<8} | {'PREC':<8} | {'REC':<8}")
        feedback.pushInfo("-" * 60)

        sorted_ids = sorted(class_names.keys())
        for cls_id in sorted_ids:
            cls_name = class_names[cls_id]
            # Montar a chave usada no dicionário global_metrics
            prefix = f"class_{cls_id}_{cls_name}"
            
            c_iou = global_metrics.get(f"{prefix}_iou", 0)
            c_f1 = global_metrics.get(f"{prefix}_f1_score", 0)
            c_prec = global_metrics.get(f"{prefix}_precision", 0)
            c_rec = global_metrics.get(f"{prefix}_recall", 0)
            
            # Formatar nome para não quebrar tabela
            display_name = f"{cls_id}-{cls_name}"[:29] 
            
            feedback.pushInfo(
                f"{display_name:<30} | {c_iou:.4f}   | {c_f1:.4f}   | {c_prec:.4f}   | {c_rec:.4f}"
            )
        
        feedback.pushInfo("="*60 + "\n")

        # --- EXPORTAÇÃO PARA CSV (Código ajustado para usar as métricas calculadas acima) ---
        feedback.pushInfo("Exportando métricas...")

        # Função auxiliar de escrita segura (mantida do passo anterior)
        def write_csv_safe(path, data_list):
            if not data_list: return
            all_keys = set().union(*(d.keys() for d in data_list))
            priority = ["mi", "quadricula", "tile_id", "num_tiles", "accuracy", "mean_iou", "f1_score"]
            header = [k for k in priority if k in all_keys] + sorted([k for k in all_keys if k not in priority])
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data_list)

        # 1. Métricas por Tile
        tile_metrics_path = os.path.join(metrics_folder, "metrics_per_tile.csv")
        if metrics_by_tile:
            write_csv_safe(tile_metrics_path, metrics_by_tile)
            feedback.pushInfo(f"  -> {tile_metrics_path}")

        # 2. Métricas por MI
        mi_metrics_path = os.path.join(metrics_folder, "metrics_per_mi.csv")
        mi_metrics_list = []
        for mi, data in mi_accumulators.items():
            # Calcula métricas REAIS baseadas na soma dos contadores do MI
            mi_m = self._calculateFinalMetricsFromCounts(
                data['counts'], 
                data['correct_pixels'], 
                data['total_pixels'], 
                class_names
            )
            mi_m['mi'] = mi
            mi_metrics_list.append(mi_m)
            
        if mi_metrics_list:
            write_csv_safe(mi_metrics_path, mi_metrics_list)
            feedback.pushInfo(f"  -> {mi_metrics_path}")

        # 3. Métricas Gerais (Usa o calculation que acabamos de fazer para o log)
        overall_metrics_path = os.path.join(metrics_folder, "metrics_overall.csv")
        if metrics_by_tile:
            # Adiciona contagem de tiles/mis ao dict de métricas
            global_metrics["num_tiles"] = processed
            global_metrics["num_mis"] = len(mi_accumulators)
            write_csv_safe(overall_metrics_path, [global_metrics])
            feedback.pushInfo(f"  -> {overall_metrics_path}")

        return {self.OUTPUT_FOLDER: output_folder}

    def _aggregateMetrics(self, metrics_list, class_names):
        """
        Agrega métricas de múltiplos tiles calculando a média.

        Args:
            metrics_list: Lista de dicionários com métricas
            class_names: Dicionário com nomes das classes

        Returns:
            Dicionário com métricas agregadas
        """
        if not metrics_list:
            return {}

        # Campos numéricos gerais para agregar
        general_fields = [
            "accuracy",
            "mean_iou",
            "precision",
            "recall",
            "f1_score",
        ]

        aggregated = {}

        # Agregar métricas gerais
        for field in general_fields:
            values = [m[field] for m in metrics_list if field in m]
            if values:
                aggregated[field] = sum(values) / len(values)

        # Agregar métricas por classe
        for class_value, class_name in class_names.items():
            class_prefix = f"class_{class_value}_{class_name}"

            # Campos de métricas por classe
            class_fields = ["iou", "precision", "recall", "f1_score"]

            for metric in class_fields:
                field_name = f"{class_prefix}_{metric}"
                values = [m[field_name] for m in metrics_list if field_name in m]
                if values:
                    aggregated[field_name] = sum(values) / len(values)

        return aggregated

    def _updateCounts(self, accumulated_counts, new_counts):
        """Acumula TP, FP, FN de um tile no acumulador global/MI."""
        for cls, metrics in new_counts.items():
            if cls not in accumulated_counts:
                accumulated_counts[cls] = {'tp': 0, 'fp': 0, 'fn': 0}
            
            accumulated_counts[cls]['tp'] += metrics['tp']
            accumulated_counts[cls]['fp'] += metrics['fp']
            accumulated_counts[cls]['fn'] += metrics['fn']
        return accumulated_counts

    def _calculateFinalMetricsFromCounts(self, counts_dict, total_correct, total_pixels, class_names):
        """Calcula métricas finais baseadas na soma total de TP/FP/FN."""
        if total_pixels == 0:
            return {}

        metrics = {}
        metrics["accuracy"] = total_correct / total_pixels
        
        ious = []
        precisions = []
        recalls = []
        f1_scores = []
        
        # Ordenar classes para manter consistência
        all_classes = sorted(counts_dict.keys())
        
        for cls in all_classes:
            vals = counts_dict[cls]
            tp = vals['tp']
            fp = vals['fp']
            fn = vals['fn']
            
            union = tp + fp + fn
            iou = tp / union if union > 0 else 0.0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            ious.append(iou)
            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1)
            
            # Nomes
            class_name = class_names.get(cls, f"Classe_{cls}")
            prefix = f"class_{cls}_{class_name}"
            
            metrics[f"{prefix}_iou"] = iou
            metrics[f"{prefix}_precision"] = precision
            metrics[f"{prefix}_recall"] = recall
            metrics[f"{prefix}_f1_score"] = f1
            # Opcional: exportar contadores brutos globais pode ser útil para debug
            # metrics[f"{prefix}_tp"] = tp 
            
        metrics["mean_iou"] = sum(ious) / len(ious) if ious else 0.0
        metrics["precision"] = sum(precisions) / len(precisions) if precisions else 0.0
        metrics["recall"] = sum(recalls) / len(recalls) if recalls else 0.0
        metrics["f1_score"] = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0
        
        return metrics