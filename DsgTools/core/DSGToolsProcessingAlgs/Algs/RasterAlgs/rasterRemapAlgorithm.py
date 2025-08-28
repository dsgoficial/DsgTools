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

import json
import numpy as np
from osgeo import gdal, osr
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterFile,
    QgsProcessingParameterRasterDestination,
    QgsProcessingException,
    QgsRasterLayer,
    QgsMessageLog,
    Qgis
)

class RasterRemapAlgorithm(QgsProcessingAlgorithm):
    INPUT_RASTER = 'INPUT_RASTER'
    MAPPING_FILE = 'MAPPING_FILE'
    OUTPUT_RASTER = 'OUTPUT_RASTER'

    def createInstance(self):
        return RasterRemapAlgorithm()

    def tr(self, string):
        return QCoreApplication.translate("RasterRemapAlgorithm", string)

    def name(self):
        return "rasterremapalgorithm"

    def displayName(self):
        return self.tr("Remap raster values from json")

    def group(self):
        return self.tr("Raster Handling")

    def groupId(self):
        return "DSGTools - Raster Handling"

    def shortHelpString(self):
        return """
        Remapeia valores de raster usando arquivo JSON de mapeamento.
        
        Parâmetros:
        - Input Raster: Raster de entrada
        - Mapping File: Arquivo JSON com mapeamento de valores
        - Output Raster: Raster de saída remapeado
        
        O algoritmo automaticamente escolhe o tipo de dados adequado
        para a saída baseado nos valores mapeados.
        
        FORMATO DO ARQUIVO JSON:
        
        O arquivo JSON deve ter a seguinte estrutura:
        
        {
          "description": "Descrição do mapeamento",
          "source": "nome_do_raster_origem",
          "target": "tabela_destino",
          "nodata_value": -9999,
          "mapping": {
            "valor_origem": valor_destino,
            "0": -9999,
            "3": 601,
            "15": 901
          },
          "class_descriptions": {
            "0": "Descrição da classe 0",
            "3": "Descrição da classe 3"
          }
        }
        
        CAMPOS OBRIGATÓRIOS:
        - mapping: Objeto com pares "valor_origem": valor_destino
        - nodata_value: Valor para pixels sem dados (-9999 recomendado)
        
        CAMPOS OPCIONAIS:
        - description: Descrição do mapeamento
        - source: Nome do dataset origem
        - target: Nome do dataset destino
        - class_descriptions: Descrições das classes
        
        EXEMPLO PRÁTICO:
        
        {
          "description": "Mapeamento Sentinel para Vegetação",
          "nodata_value": -9999,
          "mapping": {
            "0": -9999,
            "3": 601,
            "5": 201,
            "9": 1296,
            "15": 901,
            "24": -9999,
            "33": -9999
          },
          "class_descriptions": {
            "0": "Sem dados",
            "3": "Forest Formation -> Floresta densa",
            "5": "Mangrove -> Mangue",
            "9": "Forest Plantation -> Reflorestamento",
            "15": "Pasture -> Campo",
            "24": "Urban Area -> NoData",
            "33": "River, Lake and Ocean -> NoData"
          }
        }
        
        NOTAS IMPORTANTES:
        - Valores de origem devem ser strings no JSON
        - Valores de destino devem ser números inteiros
        - Classes não mapeadas serão definidas como nodata_value
        - O algoritmo escolhe automaticamente o tipo de dados de saída
        - Georreferenciamento é preservado automaticamente
        """

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                'Input Raster',
                [QgsProcessing.TypeRaster]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFile(
                self.MAPPING_FILE,
                'Mapping JSON File',
                extension='json'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                'Output Raster'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        try:
            # Obter parâmetros
            input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
            mapping_file = self.parameterAsString(parameters, self.MAPPING_FILE, context)
            output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
            
            if not input_raster or not input_raster.isValid():
                raise QgsProcessingException('Raster de entrada inválido')
            
            # Carregar arquivo de mapeamento
            feedback.pushInfo('Carregando arquivo de mapeamento...')
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    mapping_data = json.load(f)
                
                # Validar estrutura do JSON
                if 'mapping' not in mapping_data:
                    raise QgsProcessingException(
                        'Arquivo JSON deve conter o campo "mapping". '
                        'Exemplo: {"mapping": {"0": -9999, "3": 601}, "nodata_value": -9999}'
                    )
                
                mapping = mapping_data['mapping']
                nodata_value = mapping_data.get('nodata_value', -9999)
                
                # Verificar se mapping não está vazio
                if not mapping:
                    raise QgsProcessingException(
                        'O campo "mapping" não pode estar vazio. '
                        'Deve conter pelo menos um par "valor_origem": valor_destino'
                    )
                
                feedback.pushInfo(f'Mapeamento carregado: {len(mapping)} classes')
                feedback.pushInfo(f'Valor NoData: {nodata_value}')
                
            except json.JSONDecodeError as e:
                raise QgsProcessingException(
                    f'Erro ao decodificar JSON: {str(e)}. '
                    'Verifique se o arquivo está em formato JSON válido.'
                )
            except FileNotFoundError:
                raise QgsProcessingException(
                    f'Arquivo não encontrado: {mapping_file}'
                )
            except Exception as e:
                raise QgsProcessingException(f'Erro ao carregar arquivo JSON: {str(e)}')
            
            # Converter mapping para tipos numéricos
            mapping_numeric = {}
            invalid_mappings = []
            
            for key, value in mapping.items():
                try:
                    input_val = int(key)
                    output_val = int(value)
                    mapping_numeric[input_val] = output_val
                except ValueError:
                    invalid_mappings.append(f'{key} -> {value}')
            
            if invalid_mappings:
                feedback.pushWarning(
                    f'Valores inválidos ignorados no mapeamento: {", ".join(invalid_mappings)}. '
                    'Valores devem ser números inteiros.'
                )
            
            if not mapping_numeric:
                raise QgsProcessingException(
                    'Nenhum mapeamento válido encontrado. '
                    'Verifique se os valores são números inteiros.'
                )
            
            feedback.pushInfo(f'Mapeamentos válidos: {len(mapping_numeric)}')
            
            # Abrir raster com GDAL
            feedback.pushInfo('Abrindo raster de entrada...')
            input_path = input_raster.source()
            dataset = gdal.Open(input_path, gdal.GA_ReadOnly)
            
            if dataset is None:
                raise QgsProcessingException('Não foi possível abrir o raster de entrada')
            
            # Obter informações do raster
            cols = dataset.RasterXSize
            rows = dataset.RasterYSize
            bands = dataset.RasterCount
            geotransform = dataset.GetGeoTransform()
            projection = dataset.GetProjection()
            
            # Determinar tipo de dados de saída
            input_band = dataset.GetRasterBand(1)
            input_nodata = input_band.GetNoDataValue()
            
            # Verificar valores mapeados para determinar tipo adequado
            mapped_values = list(mapping_numeric.values())
            min_val = min(mapped_values + [nodata_value])
            max_val = max(mapped_values + [nodata_value])
            
            # Escolher tipo de dados baseado no range dos valores
            if min_val >= -128 and max_val <= 127:
                output_dtype = gdal.GDT_Byte if min_val >= 0 else gdal.GDT_Int16
                numpy_dtype = np.uint8 if min_val >= 0 else np.int16
            elif min_val >= -32768 and max_val <= 32767:
                output_dtype = gdal.GDT_Int16
                numpy_dtype = np.int16
            elif min_val >= 0 and max_val <= 65535:
                output_dtype = gdal.GDT_UInt16
                numpy_dtype = np.uint16
            elif min_val >= -2147483648 and max_val <= 2147483647:
                output_dtype = gdal.GDT_Int32
                numpy_dtype = np.int32
            else:
                output_dtype = gdal.GDT_Float32
                numpy_dtype = np.float32
            
            feedback.pushInfo(f'Tipo de dados de saída: {gdal.GetDataTypeName(output_dtype)}')
            
            # Criar raster de saída
            feedback.pushInfo('Criando raster de saída...')
            driver = gdal.GetDriverByName('GTiff')
            output_dataset = driver.Create(
                output_path,
                cols,
                rows,
                bands,
                output_dtype,
                options=['COMPRESS=LZW', 'TILED=YES']
            )
            
            if output_dataset is None:
                raise QgsProcessingException('Não foi possível criar o raster de saída')
            
            # Definir georreferenciamento
            output_dataset.SetGeoTransform(geotransform)
            output_dataset.SetProjection(projection)
            
            # Processar cada banda
            for band_idx in range(1, bands + 1):
                feedback.pushInfo(f'Processando banda {band_idx}/{bands}...')
                
                if feedback.isCanceled():
                    break
                
                # Ler dados da banda
                input_band = dataset.GetRasterBand(band_idx)
                input_array = input_band.ReadAsArray()
                
                # Criar array de saída
                output_array = np.full(input_array.shape, nodata_value, dtype=numpy_dtype)
                
                # Aplicar mapeamento
                for input_val, output_val in mapping_numeric.items():
                    mask = input_array == input_val
                    output_array[mask] = output_val
                
                # Tratar valores não mapeados
                if input_nodata is not None:
                    output_array[input_array == input_nodata] = nodata_value
                
                # Escrever banda de saída
                output_band = output_dataset.GetRasterBand(band_idx)
                output_band.WriteArray(output_array)
                output_band.SetNoDataValue(nodata_value)
                
                # Atualizar progresso
                feedback.setProgress(int((band_idx / bands) * 100))
            
            # Fechar datasets
            dataset = None
            output_dataset = None
            
            feedback.pushInfo('Remapeamento concluído com sucesso!')
            
            return {self.OUTPUT_RASTER: output_path}
            
        except Exception as e:
            feedback.reportError(f'Erro durante o processamento: {str(e)}')
            raise QgsProcessingException(str(e))
