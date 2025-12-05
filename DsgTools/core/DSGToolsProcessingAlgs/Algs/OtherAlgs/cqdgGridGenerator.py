# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-12-05
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

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature, QgsGeometry, QgsPointXY,
                       QgsField, QgsFields, QgsWkbTypes,
                       QgsProcessingException, QgsRectangle,
                       QgsCoordinateTransform, QgsProject,
                       QgsCoordinateReferenceSystem)
import random
import math
from itertools import product

class ETCQDGGridGenerator(QgsProcessingAlgorithm):
    # Parâmetros
    INPUT_MOLDURA = 'INPUT_MOLDURA'
    ESCALA = 'ESCALA'
    LQA = 'LQA'
    TIPO_LOTE = 'TIPO_LOTE'
    OUTPUT_GRID = 'OUTPUT_GRID'
    OUTPUT_AMOSTRA = 'OUTPUT_AMOSTRA'
    
    # Tabela 44 - Letra código ISO 2859-1
    TABELA_44 = [
        (2, 8, 'A', 'A', 'B'),
        (9, 15, 'A', 'B', 'C'),
        (16, 25, 'B', 'C', 'D'),
        (26, 50, 'C', 'D', 'E'),
        (51, 90, 'C', 'E', 'F'),
        (91, 150, 'D', 'F', 'G'),
        (151, 280, 'E', 'G', 'H'),
        (281, 500, 'F', 'H', 'J'),
        (501, 1200, 'G', 'J', 'K'),
        (1201, 3200, 'H', 'K', 'L'),
        (3201, 10000, 'J', 'L', 'M'),
        (10001, 35000, 'K', 'M', 'N'),
        (35001, 150000, 'L', 'N', 'P'),
        (150001, 500000, 'M', 'P', 'Q'),
        (500001, float('inf'), 'N', 'Q', 'R')
    ]
    
    # Tabela 45 - Tamanho amostra e Ac - ISO 2859-1 (inspeção normal, nível II)
    TABELA_45 = {
        'A': {1.0: (2, 0), 4.0: (2, 0), 10: (2, 1)},
        'B': {1.0: (3, 0), 4.0: (3, 0), 10: (3, 1)},
        'C': {1.0: (5, 0), 4.0: (5, 0), 10: (5, 2)},
        'D': {1.0: (8, 0), 4.0: (8, 1), 10: (8, 2)},
        'E': {1.0: (13, 0), 4.0: (13, 1), 10: (13, 3)},
        'F': {1.0: (20, 0), 4.0: (20, 2), 10: (20, 5)},
        'G': {1.0: (32, 1), 4.0: (32, 3), 10: (32, 7)},
        'H': {1.0: (50, 1), 4.0: (50, 5), 10: (50, 10)},
        'J': {1.0: (80, 2), 4.0: (80, 7), 10: (80, 14)},
        'K': {1.0: (125, 3), 4.0: (125, 10), 10: (125, 21)},
        'L': {1.0: (200, 5), 4.0: (200, 14), 10: (200, 21)},
        'M': {1.0: (315, 7), 4.0: (315, 21), 10: (315, 21)},
        'N': {1.0: (500, 10), 4.0: (500, 21), 10: (500, 21)},
        'P': {1.0: (800, 14), 4.0: (800, 21), 10: (800, 21)},
        'Q': {1.0: (1250, 21), 4.0: (1250, 21), 10: (1250, 21)},
        'R': {1.0: (2000, 21), 4.0: (2000, 21), 10: (2000, 21)}
    }
    
    # Tabela 47 - Lote isolado ISO 2859-2
    TABELA_47 = {
        (16, 25): {20: (13, 0), 32: (9, 0)},
        (26, 50): {20: (22, 0), 32: (15, 0)},
        (51, 90): {20: (24, 0), 32: (16, 0)},
        (91, 150): {20: (26, 0), 32: (18, 0)},
        (151, 280): {20: (28, 0), 32: (20, 1)},
        (281, 500): {20: (32, 1), 32: (20, 1)},
        (501, 1200): {20: (32, 1), 32: (32, 3)},
        (1201, 3200): {20: (50, 3), 32: (50, 5)},
        (3201, 10000): {20: (80, 5), 32: (80, 10)},
        (10001, 35000): {20: (125, 10), 32: (125, 18)},
        (35001, 150000): {20: (200, 18), 32: (200, 18)},
        (150001, float('inf')): {20: (200, 18), 32: (200, 18)}
    }

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ETCQDGGridGenerator()

    def name(self):
        return 'cqdggridgenerator'

    def displayName(self):
        return self.tr('Gerador de Quadrículas ET-CQDG')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr("Data Quality")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to.
        """
        return "DSGTools - Data Quality"
    
    def getSirgasAuthIdByPointLatLong(self, lat, long):
        """
        Calculates SIRGAS 2000 epsg.
        """
        zone_number = math.floor(((long + 180) / 6) % 60) + 1
        if lat >= 0:
            zone_letter = "N"
        else:
            zone_letter = "S"
        return self.getSirgasEpsg(f"{zone_number}{zone_letter}")

    def getSirgasEpsg(self, key):
        """
        Returns SIRGAS 2000 EPSG code for a given UTM zone.
        """
        options = {
            "11N": "EPSG:31965", "12N": "EPSG:31966", "13N": "EPSG:31967",
            "14N": "EPSG:31968", "15N": "EPSG:31969", "16N": "EPSG:31970",
            "17N": "EPSG:31971", "18N": "EPSG:31972", "19N": "EPSG:31973",
            "20N": "EPSG:31974", "21N": "EPSG:31975", "22N": "EPSG:31976",
            "17S": "EPSG:31977", "18S": "EPSG:31978", "19S": "EPSG:31979",
            "20S": "EPSG:31980", "21S": "EPSG:31981", "22S": "EPSG:31982",
            "23S": "EPSG:31983", "24S": "EPSG:31984", "25S": "EPSG:31985",
            "26S": "EPSG:5396",
        }
        return options.get(key, "")

    def getUtmRefSysFromGeometry(self, geometry, source_crs):
        """
        Determina o sistema de referência UTM apropriado baseado no centroide da geometria.
        """
        # Fazer cópia para não modificar original
        centroid = geometry.centroid()
        
        if not source_crs.isGeographic():
            # Transformar para WGS84 para calcular lat/long
            wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
            transform = QgsCoordinateTransform(source_crs, wgs84, QgsProject.instance())
            centroid.transform(transform)
        
        point = QgsPointXY(centroid.constGet())
        utmString = self.getSirgasAuthIdByPointLatLong(point.y(), point.x())
        if not utmString:
            return None
        utm = QgsCoordinateReferenceSystem(utmString)
        return utm

    def shortHelpString(self):
        return self.tr("""
        Gera quadrículas de avaliação conforme ET-CQDG (DSG/EB).
        
        IMPORTANTE: Apenas quadrículas COMPLETAMENTE dentro da moldura são 
        consideradas (quadrículas cortadas pela borda são descartadas).
        
        Cada moldura é processada individualmente com seu fuso UTM específico.
        
        Parâmetros:
        - Camada de Moldura: Camada vetorial com as molduras (MI)
        - Escala: Escala de trabalho (1:25.000, 1:50.000, 1:100.000, 1:250.000)
        - LQA (%): Limite de Qualidade Aceitável (1%, 4% ou 10%)
        - Tipo de Lote: Lote a lote (10+ produtos) ou Isolado (1-9 produtos)
        
        Saídas:
        - Grid completo: Todas as quadrículas inteiras dentro da moldura
        - Amostra: Quadrículas selecionadas aleatoriamente para avaliação
        """)

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_MOLDURA,
                self.tr('Camada de Moldura (MI)'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterEnum(
                self.ESCALA,
                self.tr('Escala'),
                options=['1:25.000', '1:50.000', '1:100.000', '1:250.000'],
                defaultValue=0
            )
        )
        
        self.addParameter(
            QgsProcessingParameterEnum(
                self.LQA,
                self.tr('LQA - Limite de Qualidade Aceitável (%)'),
                options=['1%', '4%', '10%'],
                defaultValue=1
            )
        )
        
        self.addParameter(
            QgsProcessingParameterEnum(
                self.TIPO_LOTE,
                self.tr('Tipo de Lote'),
                options=['Lote a Lote (10+ produtos)', 'Isolado (1-9 produtos)'],
                defaultValue=1
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_GRID,
                self.tr('Grid Completo de Quadrículas')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_AMOSTRA,
                self.tr('Quadrículas Amostradas')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Obter parâmetros
        moldura_layer = self.parameterAsVectorLayer(parameters, self.INPUT_MOLDURA, context)
        escala_idx = self.parameterAsEnum(parameters, self.ESCALA, context)
        lqa_idx = self.parameterAsEnum(parameters, self.LQA, context)
        tipo_lote = self.parameterAsEnum(parameters, self.TIPO_LOTE, context)
        
        # Converter parâmetros
        escalas = [25000, 50000, 100000, 250000]
        escala = escalas[escala_idx]
        
        lqas = [1.0, 4.0, 10.0]
        lqa = lqas[lqa_idx]
        
        # Calcular tamanho da quadrícula (em metros)
        grid_size = 4 * escala / 100  # 4 cm na escala
        
        # Obter CRS original
        original_crs = moldura_layer.crs()
        
        feedback.pushInfo(f'Sistema de referência original: {original_crs.authid()}')
        feedback.pushInfo(f'Escala: 1:{escala}')
        feedback.pushInfo(f'Tamanho da quadrícula: {grid_size} metros')
        feedback.pushInfo(f'LQA: {lqa}%')
        
        # Criar campos de saída
        fields = QgsFields()
        fields.append(QgsField('mi', QVariant.String))
        fields.append(QgsField('quadricula', QVariant.String))
        fields.append(QgsField('grid_x', QVariant.Int))
        fields.append(QgsField('grid_y', QVariant.Int))
        fields.append(QgsField('area_m2', QVariant.Double))
        fields.append(QgsField('selecionada', QVariant.Int))
        fields.append(QgsField('fuso_utm', QVariant.String))
        
        # Criar sinks (no CRS original)
        (sink_grid, dest_id_grid) = self.parameterAsSink(
            parameters, self.OUTPUT_GRID, context,
            fields, QgsWkbTypes.Polygon, original_crs
        )
        
        (sink_amostra, dest_id_amostra) = self.parameterAsSink(
            parameters, self.OUTPUT_AMOSTRA, context,
            fields, QgsWkbTypes.Polygon, original_crs
        )
        
        # Processar cada MI
        total_features = moldura_layer.featureCount()
        
        for current, moldura_feat in enumerate(moldura_layer.getFeatures()):
            if feedback.isCanceled():
                break
                
            feedback.setProgress(int(current * 100 / total_features))
            
            # Identificar MI
            mi_nome = moldura_feat.attribute('mi') if moldura_feat.fieldNameIndex('mi') >= 0 else f'MI_{current+1}'
            feedback.pushInfo(f'\nProcessando {mi_nome}...')
            
            # Obter geometria da moldura (cópia para não modificar o original)
            moldura_geom_original = moldura_feat.geometry()
            
            # Determinar fuso UTM específico para esta moldura
            utm_crs = self.getUtmRefSysFromGeometry(moldura_geom_original, original_crs)
            
            if utm_crs is None or not utm_crs.isValid():
                feedback.pushWarning(f'Não foi possível determinar o sistema UTM para {mi_nome}. Ignorando...')
                continue
            
            feedback.pushInfo(f'Fuso UTM para esta moldura: {utm_crs.authid()}')
            
            # Criar transformadores específicos para esta moldura
            transform_to_utm = QgsCoordinateTransform(
                original_crs, 
                utm_crs, 
                QgsProject.instance()
            )
            transform_from_utm = QgsCoordinateTransform(
                utm_crs, 
                original_crs, 
                QgsProject.instance()
            )
            
            # Reprojetar moldura para UTM (fazer cópia para não modificar original)
            moldura_geom_utm = QgsGeometry(moldura_geom_original)
            moldura_geom_utm.transform(transform_to_utm)
            
            bbox = moldura_geom_utm.boundingBox()
            
            # Ajustar bbox para grid UTM (valores inteiros baseados no grid_size)
            xmin = math.floor(bbox.xMinimum() / grid_size) * grid_size
            ymin = math.floor(bbox.yMinimum() / grid_size) * grid_size
            xmax = math.ceil(bbox.xMaximum() / grid_size) * grid_size
            ymax = math.ceil(bbox.yMaximum() / grid_size) * grid_size
            
            # Gerar quadrículas em UTM
            quadriculas_utm = []
            quadriculas_descartadas = 0
            
            # Calcular número de células em cada direção
            n_cols = int((xmax - xmin) / grid_size)
            n_rows = int((ymax - ymin) / grid_size)
            total_celulas = n_cols * n_rows
            
            # Usar itertools.product para gerar todas as combinações de índices
            for grid_x_idx, grid_y_idx in product(range(n_cols), range(n_rows)):
                x = xmin + grid_x_idx * grid_size
                y = ymin + grid_y_idx * grid_size
                
                # Criar geometria da quadrícula em UTM
                rect = QgsRectangle(x, y, x + grid_size, y + grid_size)
                quad_geom_utm = QgsGeometry.fromRect(rect)
                
                # Verificar se a quadrícula está COMPLETAMENTE dentro da moldura (em UTM)
                if moldura_geom_utm.contains(quad_geom_utm):
                    # Identificador da quadrícula (ex: K1, K2, L1, L2...)
                    col_letter = chr(65 + grid_x_idx)  # A, B, C...
                    quad_id = f'{col_letter}{grid_y_idx + 1}'
                    
                    # Armazenar informações da quadrícula em UTM
                    quadriculas_utm.append({
                        'geom_utm': quad_geom_utm,
                        'mi': mi_nome,
                        'quadricula': quad_id,
                        'grid_x': grid_x_idx,
                        'grid_y': grid_y_idx,
                        'area_m2': grid_size * grid_size,
                        'fuso_utm': utm_crs.authid()
                    })
                else:
                    quadriculas_descartadas += 1
            
            # Calcular tamanho da amostra
            n_total = len(quadriculas_utm)
            feedback.pushInfo(f'Células do grid: {total_celulas}')
            feedback.pushInfo(f'Quadrículas completas: {n_total}')
            feedback.pushInfo(f'Quadrículas descartadas (parciais): {quadriculas_descartadas}')
            
            if n_total == 0:
                feedback.pushWarning(f'Nenhuma quadrícula gerada para {mi_nome}')
                continue
            
            # Determinar tamanho da amostra
            if tipo_lote == 0:  # Lote a lote
                n_amostra, ac = self._calcular_amostra_lote(n_total, lqa)
            else:  # Isolado
                n_amostra, ac = self._calcular_amostra_isolado(n_total, lqa)
            
            feedback.pushInfo(f'Tamanho da amostra: {n_amostra}')
            feedback.pushInfo(f'Número de aceitação: {ac}')
            
            # Selecionar aleatoriamente os índices
            indices_amostra = set(random.sample(range(n_total), min(n_amostra, n_total)))
            
            # Reprojetar quadrículas de volta para CRS original e adicionar aos sinks
            for idx, quad_info in enumerate(quadriculas_utm):
                # Reprojetar geometria de volta para CRS original
                quad_geom_original = QgsGeometry(quad_info['geom_utm'])
                quad_geom_original.transform(transform_from_utm)
                
                # Criar feature
                feat = QgsFeature(fields)
                feat.setGeometry(quad_geom_original)
                feat.setAttribute('mi', quad_info['mi'])
                feat.setAttribute('quadricula', quad_info['quadricula'])
                feat.setAttribute('grid_x', quad_info['grid_x'])
                feat.setAttribute('grid_y', quad_info['grid_y'])
                feat.setAttribute('area_m2', quad_info['area_m2'])
                feat.setAttribute('fuso_utm', quad_info['fuso_utm'])
                
                # Verificar se foi selecionada na amostra
                selecionada = 1 if idx in indices_amostra else 0
                feat.setAttribute('selecionada', selecionada)
                
                # Adicionar ao grid completo
                sink_grid.addFeature(feat)
                
                # Se foi selecionada, adicionar também à amostra
                if selecionada:
                    sink_amostra.addFeature(feat)
        
        feedback.pushInfo('\nProcessamento concluído!')
        
        return {
            self.OUTPUT_GRID: dest_id_grid,
            self.OUTPUT_AMOSTRA: dest_id_amostra
        }
    
    def _calcular_amostra_lote(self, tamanho_lote, lqa):
        """Calcula tamanho da amostra para lote a lote (ISO 2859-1)"""
        # Encontrar letra código (Tabela 44, nível II)
        letra = None
        for min_val, max_val, nivel_i, nivel_ii, nivel_iii in self.TABELA_44:
            if min_val <= tamanho_lote <= max_val:
                letra = nivel_ii
                break
        
        if not letra:
            raise QgsProcessingException(f'Não foi possível determinar letra código para lote de tamanho {tamanho_lote}')
        
        # Buscar na tabela 45
        if letra in self.TABELA_45 and lqa in self.TABELA_45[letra]:
            return self.TABELA_45[letra][lqa]
        
        raise QgsProcessingException(f'Combinação letra={letra}, LQA={lqa} não encontrada na tabela')
    
    def _calcular_amostra_isolado(self, tamanho_lote, lqa):
        """Calcula tamanho da amostra para lote isolado (ISO 2859-2)"""
        # Converter LQA para QL usando Tabela 46 (simplificada)
        ql_map = {1.0: 20, 4.0: 20, 10.0: 32}
        ql = ql_map.get(lqa, 20)
        
        # Encontrar faixa na Tabela 47
        for (min_val, max_val), valores in self.TABELA_47.items():
            if min_val <= tamanho_lote <= max_val:
                if ql in valores:
                    return valores[ql]
        
        # Padrão conservador
        return (min(tamanho_lote, 50), 1)
    
    def getUtmRefSys(self, frameLayer):
        features = frameLayer.getFeatures()
        first_feature = next(features, None)

        # Se não houver feições, retorna None
        if first_feature is None:
            return None

        geom = first_feature.geometry()
        centroid = geom.centroid()
        point = QgsPointXY(centroid.constGet())
        utmString = getSirgasAuthIdByPointLatLong(point.y(), point.x())
        utm = QgsCoordinateReferenceSystem(utmString)
        return utm

def getSirgasAuthIdByPointLatLong(lat, long):
    """
    Calculates SIRGAS 2000 epsg.
    <h2>Example usage:</h2>
    <ul>
    <li>Found: getSirgarAuthIdByPointLatLong(-8.05389, -34.881111) -> 'ESPG:31985'</li>
    <li>Not found: getSirgarAuthIdByPointLatLong(lat, long) -> ''</li>
    </ul>
    """
    zone_number = math.floor(((long + 180) / 6) % 60) + 1
    if lat >= 0:
        zone_letter = "N"
    else:
        zone_letter = "S"
    return getSirgasEpsg("{0}{1}".format(zone_number, zone_letter))


def getSirgasEpsg(key):
    options = {
        "11N": "EPSG:31965",
        "12N": "EPSG:31966",
        "13N": "EPSG:31967",
        "14N": "EPSG:31968",
        "15N": "EPSG:31969",
        "16N": "EPSG:31970",
        "17N": "EPSG:31971",
        "18N": "EPSG:31972",
        "19N": "EPSG:31973",
        "20N": "EPSG:31974",
        "21N": "EPSG:31975",
        "22N": "EPSG:31976",
        "17S": "EPSG:31977",
        "18S": "EPSG:31978",
        "19S": "EPSG:31979",
        "20S": "EPSG:31980",
        "21S": "EPSG:31981",
        "22S": "EPSG:31982",
        "23S": "EPSG:31983",
        "24S": "EPSG:31984",
        "25S": "EPSG:31985",
        "26S": "EPSG:5396",
    }
    return options[key] if key in options else ""