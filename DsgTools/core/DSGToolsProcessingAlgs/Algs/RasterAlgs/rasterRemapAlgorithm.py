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
import os
import shutil
import traceback
from osgeo import gdal, osr
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterFile,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterBoolean,
    QgsProcessingException,
    QgsRasterLayer,
    QgsMessageLog,
    Qgis
)

class RasterRemapAlgorithm(QgsProcessingAlgorithm):
    INPUT_RASTER = 'INPUT_RASTER'
    MAPPING_FILE = 'MAPPING_FILE'
    OUTPUT_RASTER = 'OUTPUT_RASTER'
    FORCE_CHUNKED = 'FORCE_CHUNKED'

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
        OTIMIZADO COM DIVISÃO ADAPTATIVA PARA GRANDES RASTERS.
        
        Parâmetros:
        - Input Raster: Raster de entrada
        - Mapping File: Arquivo JSON com mapeamento de valores
        - Output Raster: Raster de saída remapeado
        - Force Chunked Processing: Forçar processamento em chunks (padrão: Não)
        
        ESTRATÉGIA DE PROCESSAMENTO:
        
        O algoritmo tenta processar o raster inteiro de uma vez para máxima
        performance com NumPy. Se houver erro de memória, divide automaticamente:
        
        1ª tentativa: Processar tudo (1x1 = 1 bloco)
        2ª tentativa: Dividir em 2x2 (4 blocos)
        3ª tentativa: Dividir em 4x4 (16 blocos)
        4ª tentativa: Dividir em 8x8 (64 blocos)
        ... e assim por diante até conseguir
        
        Isso maximiza o uso eficiente do NumPy e minimiza loops Python.
        
        FORMATO DO ARQUIVO JSON:
        
        {
          "description": "Descrição do mapeamento",
          "nodata_value": -9999,
          "mapping": {
            "0": -9999,
            "3": 601,
            "15": 901
          }
        }
        
        CAMPOS OBRIGATÓRIOS:
        - mapping: Objeto com pares "valor_origem": valor_destino
        - nodata_value: Valor para pixels sem dados
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
        
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FORCE_CHUNKED,
                'Force Chunked Processing',
                defaultValue=False,
                optional=True
            )
        )

    def load_mapping(self, mapping_file, feedback):
        """Carrega e valida o arquivo de mapeamento JSON"""
        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping_data = json.load(f)
            
            if 'mapping' not in mapping_data:
                raise QgsProcessingException(
                    'Arquivo JSON deve conter o campo "mapping".'
                )
            
            mapping = mapping_data['mapping']
            nodata_value = mapping_data.get('nodata_value', -9999)
            
            if not mapping:
                raise QgsProcessingException('O campo "mapping" não pode estar vazio.')
            
            # Converter para tipos numéricos
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
                    f'Valores inválidos ignorados: {", ".join(invalid_mappings)}'
                )
            
            if not mapping_numeric:
                raise QgsProcessingException('Nenhum mapeamento válido encontrado.')
            
            feedback.pushInfo(f'Mapeamento carregado: {len(mapping_numeric)} classes')
            feedback.pushInfo(f'Valor NoData: {nodata_value}')
            
            return mapping_numeric, nodata_value
            
        except json.JSONDecodeError as e:
            raise QgsProcessingException(f'Erro ao decodificar JSON: {str(e)}')
        except FileNotFoundError:
            raise QgsProcessingException(f'Arquivo não encontrado: {mapping_file}')
        except Exception as e:
            raise QgsProcessingException(f'Erro ao carregar JSON: {str(e)}')

    def determine_output_dtype(self, mapping_numeric, nodata_value):
        """Determina o tipo de dados ideal para o raster de saída"""
        mapped_values = list(mapping_numeric.values())
        min_val = min(mapped_values + [nodata_value])
        max_val = max(mapped_values + [nodata_value])
        
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
        
        return output_dtype, numpy_dtype

    def remap_array(self, input_array, mapping_numeric, nodata_value, input_nodata, numpy_dtype):
        """Aplica o remapeamento em um array NumPy"""
        output_array = np.full(input_array.shape, nodata_value, dtype=numpy_dtype)
        
        # Aplicar mapeamento - operação vetorizada do NumPy
        for input_val, output_val in mapping_numeric.items():
            mask = input_array == input_val
            output_array[mask] = output_val
        
        # Tratar valores nodata da entrada
        if input_nodata is not None:
            output_array[input_array == input_nodata] = nodata_value
        
        return output_array

    def process_band_whole(self, input_band, output_band, mapping_numeric, 
                          nodata_value, input_nodata, numpy_dtype, feedback):
        """Tenta processar a banda inteira de uma vez"""
        try:
            feedback.pushInfo('Tentando processar banda inteira...')
            
            # Ler array completo
            input_array = input_band.ReadAsArray()
            
            if input_array is None:
                raise MemoryError('Falha ao ler array')
            
            # Aplicar remapeamento
            output_array = self.remap_array(
                input_array, mapping_numeric, nodata_value, 
                input_nodata, numpy_dtype
            )
            
            # Escrever resultado
            output_band.WriteArray(output_array)
            output_band.SetNoDataValue(nodata_value)
            output_band.FlushCache()
            
            feedback.pushInfo('✓ Banda processada com sucesso (modo completo)')
            return True
            
        except (MemoryError, Exception) as e:
            feedback.pushInfo(f'✗ Não foi possível processar banda inteira: {str(e)}')
            return False

    def process_band_chunked(self, input_band, output_band, cols, rows,
                            mapping_numeric, nodata_value, input_nodata, 
                            numpy_dtype, feedback):
        """Processa a banda em chunks com divisão adaptativa"""
        
        # Começar com divisão 2x2
        divisions = 2
        max_divisions = 64  # Limite máximo para evitar chunks muito pequenos
        
        while divisions <= max_divisions:
            try:
                feedback.pushInfo(f'Tentando processar em {divisions}x{divisions} chunks...')
                
                # Calcular tamanho dos chunks
                chunk_rows = rows // divisions
                chunk_cols = cols // divisions
                
                # Calcular tamanho estimado em GB
                estimated_size_gb = (chunk_rows * chunk_cols * np.dtype(numpy_dtype).itemsize) / (1024**3)
                feedback.pushInfo(f'Tamanho estimado por chunk: {estimated_size_gb:.2f} GB')
                
                total_chunks = divisions * divisions
                current_chunk = 0
                
                # Processar cada chunk
                for i in range(divisions):
                    if feedback.isCanceled():
                        return False
                    
                    # Calcular limites em Y
                    y_start = i * chunk_rows
                    if i == divisions - 1:
                        y_end = rows
                    else:
                        y_end = (i + 1) * chunk_rows
                    y_size = y_end - y_start
                    
                    for j in range(divisions):
                        if feedback.isCanceled():
                            return False
                        
                        # Calcular limites em X
                        x_start = j * chunk_cols
                        if j == divisions - 1:
                            x_end = cols
                        else:
                            x_end = (j + 1) * chunk_cols
                        x_size = x_end - x_start
                        
                        # Ler chunk
                        input_chunk = input_band.ReadAsArray(x_start, y_start, x_size, y_size)
                        
                        if input_chunk is None:
                            raise MemoryError(f'Falha ao ler chunk ({i},{j})')
                        
                        # Aplicar remapeamento
                        output_chunk = self.remap_array(
                            input_chunk, mapping_numeric, nodata_value,
                            input_nodata, numpy_dtype
                        )
                        
                        # Escrever chunk
                        output_band.WriteArray(output_chunk, x_start, y_start)
                        
                        # Atualizar progresso
                        current_chunk += 1
                        progress = int((current_chunk / total_chunks) * 100)
                        feedback.setProgress(progress)
                        
                        if current_chunk % max(1, total_chunks // 10) == 0:
                            feedback.pushInfo(
                                f'Progresso: {current_chunk}/{total_chunks} chunks '
                                f'({progress}%)'
                            )
                
                output_band.SetNoDataValue(nodata_value)
                output_band.FlushCache()
                
                feedback.pushInfo(
                    f'✓ Banda processada com sucesso em {divisions}x{divisions} chunks '
                    f'(total: {total_chunks} chunks)'
                )
                return True
                
            except (MemoryError, Exception) as e:
                feedback.pushWarning(
                    f'✗ Falha com {divisions}x{divisions} chunks: {str(e)}'
                )
                # Dobrar o número de divisões
                divisions *= 2
                continue
        
        raise QgsProcessingException(
            f'Não foi possível processar mesmo com {max_divisions}x{max_divisions} chunks. '
            'Raster muito grande ou memória insuficiente.'
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Configurar GDAL para reportar erros
        gdal.UseExceptions()
        
        try:
            # Obter parâmetros
            input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
            mapping_file = self.parameterAsString(parameters, self.MAPPING_FILE, context)
            output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
            force_chunked = self.parameterAsBool(parameters, self.FORCE_CHUNKED, context)
            
            # Validar caminho de saída
            if not output_path:
                raise QgsProcessingException('Caminho de saída não especificado')
            
            # Avisar se está usando caminho de rede
            if output_path.startswith('\\\\') or output_path.startswith('//'):
                feedback.pushWarning(
                    'ATENÇÃO: Caminho de rede detectado no arquivo de saída.\n'
                    'Processamento pode ser mais lento. Considere usar disco local.'
                )
            
            if not input_raster or not input_raster.isValid():
                raise QgsProcessingException('Raster de entrada inválido')
            
            # Carregar mapeamento
            feedback.pushInfo('=' * 60)
            feedback.pushInfo('CARREGANDO MAPEAMENTO')
            feedback.pushInfo('=' * 60)
            mapping_numeric, nodata_value = self.load_mapping(mapping_file, feedback)
            
            # Abrir raster
            feedback.pushInfo('=' * 60)
            feedback.pushInfo('ABRINDO RASTER')
            feedback.pushInfo('=' * 60)
            input_path = input_raster.source()
            feedback.pushInfo(f'Caminho: {input_path}')
            
            try:
                dataset = gdal.Open(input_path, gdal.GA_ReadOnly)
                
                if dataset is None:
                    gdal_error = gdal.GetLastErrorMsg()
                    raise QgsProcessingException(
                        f'Não foi possível abrir o raster de entrada.\n'
                        f'Erro GDAL: {gdal_error}\n'
                        f'Caminho: {input_path}'
                    )
                
                feedback.pushInfo('✓ Raster aberto com sucesso')
                
            except Exception as e:
                raise QgsProcessingException(
                    f'Erro ao abrir raster: {str(e)}\n'
                    f'Caminho: {input_path}'
                )
            
            # Obter informações do raster
            cols = dataset.RasterXSize
            rows = dataset.RasterYSize
            bands = dataset.RasterCount
            geotransform = dataset.GetGeoTransform()
            projection = dataset.GetProjection()
            
            feedback.pushInfo(f'Dimensões: {cols:,} x {rows:,} pixels')
            feedback.pushInfo(f'Bandas: {bands}')
            
            # Calcular tamanho estimado
            input_band = dataset.GetRasterBand(1)
            input_nodata = input_band.GetNoDataValue()
            input_dtype = gdal.GetDataTypeName(input_band.DataType)
            
            size_gb = (cols * rows * input_band.DataType) / (1024**3)
            feedback.pushInfo(f'Tamanho estimado: {size_gb:.2f} GB')
            feedback.pushInfo(f'Tipo de dados entrada: {input_dtype}')
            
            # Determinar tipo de saída
            output_dtype, numpy_dtype = self.determine_output_dtype(
                mapping_numeric, nodata_value
            )
            feedback.pushInfo(f'Tipo de dados saída: {gdal.GetDataTypeName(output_dtype)}')
            
            # Criar raster de saída
            feedback.pushInfo('=' * 60)
            feedback.pushInfo('CRIANDO RASTER DE SAÍDA')
            feedback.pushInfo('=' * 60)
            feedback.pushInfo(f'Caminho de saída: {output_path}')
            
            # Validar diretório de saída
            output_dir = os.path.dirname(output_path)
            if not output_dir:
                output_dir = '.'
            
            feedback.pushInfo(f'Diretório de saída: {output_dir}')
            
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    feedback.pushInfo(f'✓ Diretório criado: {output_dir}')
                except Exception as e:
                    raise QgsProcessingException(
                        f'Não foi possível criar diretório de saída:\n'
                        f'{output_dir}\n'
                        f'Erro: {str(e)}'
                    )
            else:
                feedback.pushInfo(f'✓ Diretório existe: {output_dir}')
            
            # Testar permissão de escrita
            test_file = os.path.join(output_dir, '.test_write_permission')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                feedback.pushInfo('✓ Permissão de escrita verificada')
            except Exception as e:
                raise QgsProcessingException(
                    f'Sem permissão de escrita no diretório:\n'
                    f'{output_dir}\n'
                    f'Erro: {str(e)}'
                )
            
            # Verificar espaço em disco disponível (Windows)
            try:
                import shutil
                total, used, free = shutil.disk_usage(output_dir)
                available_gb = free / (1024**3)
                required_gb = size_gb * 1.5  # Adicionar margem de 50%
                
                feedback.pushInfo(f'Espaço disponível: {available_gb:.1f} GB')
                feedback.pushInfo(f'Espaço necessário (estimado): {required_gb:.1f} GB')
                
                if available_gb < required_gb:
                    raise QgsProcessingException(
                        f'ESPAÇO EM DISCO INSUFICIENTE!\n'
                        f'Disponível: {available_gb:.1f} GB\n'
                        f'Necessário: {required_gb:.1f} GB\n'
                        f'Libere espaço no disco ou escolha outro local.'
                    )
                else:
                    feedback.pushInfo('✓ Espaço em disco suficiente')
                    
            except QgsProcessingException:
                raise
            except Exception as e:
                feedback.pushWarning(f'Não foi possível verificar espaço em disco: {str(e)}')
            
            # Verificar se arquivo já existe
            if os.path.exists(output_path):
                feedback.pushWarning(f'Arquivo já existe e será sobrescrito: {output_path}')
                try:
                    os.remove(output_path)
                    feedback.pushInfo('✓ Arquivo anterior removido')
                except Exception as e:
                    raise QgsProcessingException(
                        f'Não foi possível remover arquivo existente:\n'
                        f'{output_path}\n'
                        f'Erro: {str(e)}\n'
                        f'O arquivo pode estar em uso por outro programa.'
                    )
            
            try:
                feedback.pushInfo('Obtendo driver GTiff...')
                driver = gdal.GetDriverByName('GTiff')
                if driver is None:
                    raise QgsProcessingException('Driver GTiff não disponível no GDAL')
                
                feedback.pushInfo('✓ Driver GTiff obtido')
                
                # Preparar opções de criação
                create_options = ['COMPRESS=LZW', 'TILED=YES', 'BIGTIFF=YES']
                feedback.pushInfo(f'Opções de criação: {", ".join(create_options)}')
                
                # Log dos parâmetros
                feedback.pushInfo(f'Parâmetros de criação:')
                feedback.pushInfo(f'  - Colunas: {cols:,}')
                feedback.pushInfo(f'  - Linhas: {rows:,}')
                feedback.pushInfo(f'  - Bandas: {bands}')
                feedback.pushInfo(f'  - Tipo: {gdal.GetDataTypeName(output_dtype)}')
                
                feedback.pushInfo('Criando dataset GDAL...')
                
                output_dataset = driver.Create(
                    output_path,
                    cols,
                    rows,
                    bands,
                    output_dtype,
                    options=create_options
                )
                
                feedback.pushInfo('Chamada Create() concluída')
                
                if output_dataset is None:
                    # Capturar erro do GDAL
                    gdal_error = gdal.GetLastErrorMsg()
                    gdal_error_num = gdal.GetLastErrorNo()
                    gdal_error_type = gdal.GetLastErrorType()
                    
                    error_details = (
                        f'Não foi possível criar o raster de saída.\n'
                        f'Caminho: {output_path}\n'
                        f'GDAL Error Number: {gdal_error_num}\n'
                        f'GDAL Error Type: {gdal_error_type}\n'
                        f'GDAL Error Message: {gdal_error}\n\n'
                        f'Possíveis causas:\n'
                        f'- Caminho inválido ou muito longo\n'
                        f'- Caracteres especiais no nome do arquivo\n'
                        f'- Unidade de rede inacessível\n'
                        f'- Problema com driver GTiff\n'
                        f'- Arquivo/processo bloqueado por antivírus\n'
                    )
                    raise QgsProcessingException(error_details)
                
                feedback.pushInfo('✓ Arquivo de saída criado')
                
                output_dataset.SetGeoTransform(geotransform)
                output_dataset.SetProjection(projection)
                feedback.pushInfo('✓ Georreferenciamento configurado')
                
                # Validar que conseguimos acessar as bandas
                for b in range(1, bands + 1):
                    band = output_dataset.GetRasterBand(b)
                    if band is None:
                        raise QgsProcessingException(
                            f'Não foi possível criar banda {b} no raster de saída'
                        )
                feedback.pushInfo(f'✓ {bands} banda(s) criada(s) com sucesso')
                
                # Tentar forçar flush inicial para detectar erros de I/O
                try:
                    output_dataset.FlushCache()
                    feedback.pushInfo('✓ Validação de escrita em disco OK')
                except Exception as flush_error:
                    raise QgsProcessingException(
                        f'Erro ao escrever no disco: {str(flush_error)}\n'
                        f'Possíveis causas:\n'
                        f'- Espaço em disco insuficiente\n'
                        f'- Permissões de escrita\n'
                        f'- Caminho de rede com problemas'
                    )
                
            except Exception as e:
                # Tentar limpar arquivo parcial
                try:
                    if output_dataset is not None:
                        output_dataset = None
                    if os.path.exists(output_path):
                        os.remove(output_path)
                        feedback.pushInfo('Arquivo parcial removido')
                except:
                    pass
                
                # Re-raise com mais contexto
                error_type = type(e).__name__
                error_msg = str(e)
                gdal_error = gdal.GetLastErrorMsg()
                
                full_error = f'Erro ao criar raster de saída:\n'
                full_error += f'Tipo: {error_type}\n'
                full_error += f'Mensagem: {error_msg}\n'
                if gdal_error:
                    full_error += f'GDAL: {gdal_error}\n'
                full_error += f'Caminho: {output_path}\n'
                
                feedback.reportError(full_error)
                
                raise QgsProcessingException(full_error)
            
            # Processar cada banda
            feedback.pushInfo('=' * 60)
            feedback.pushInfo('PROCESSANDO BANDAS')
            feedback.pushInfo('=' * 60)
            
            for band_idx in range(1, bands + 1):
                feedback.pushInfo(f'\nBanda {band_idx}/{bands}')
                feedback.pushInfo('-' * 60)
                
                if feedback.isCanceled():
                    break
                
                input_band = dataset.GetRasterBand(band_idx)
                output_band = output_dataset.GetRasterBand(band_idx)
                
                # Decidir estratégia de processamento
                if force_chunked:
                    feedback.pushInfo('Modo chunked forçado pelo usuário')
                    success = self.process_band_chunked(
                        input_band, output_band, cols, rows,
                        mapping_numeric, nodata_value, input_nodata,
                        numpy_dtype, feedback
                    )
                else:
                    # Tentar modo completo primeiro
                    success = self.process_band_whole(
                        input_band, output_band, mapping_numeric,
                        nodata_value, input_nodata, numpy_dtype, feedback
                    )
                    
                    # Se falhar, usar modo chunked
                    if not success:
                        feedback.pushInfo('Alternando para modo chunked...')
                        success = self.process_band_chunked(
                            input_band, output_band, cols, rows,
                            mapping_numeric, nodata_value, input_nodata,
                            numpy_dtype, feedback
                        )
                
                if not success:
                    raise QgsProcessingException(f'Falha ao processar banda {band_idx}')
            
            # Fechar datasets e garantir flush final
            feedback.pushInfo('=' * 60)
            feedback.pushInfo('FINALIZANDO')
            feedback.pushInfo('=' * 60)
            
            try:
                # Forçar flush de todas as bandas
                for band_idx in range(1, bands + 1):
                    band = output_dataset.GetRasterBand(band_idx)
                    if band:
                        band.FlushCache()
                
                output_dataset.FlushCache()
                feedback.pushInfo('✓ Dados gravados no disco')
                
                # Fechar datasets
                dataset = None
                output_dataset = None
                feedback.pushInfo('✓ Arquivos fechados')
                
                # Verificar se arquivo foi criado
                if not os.path.exists(output_path):
                    raise QgsProcessingException(
                        'Arquivo de saída não foi criado. Verifique permissões e espaço em disco.'
                    )
                
                file_size_gb = os.path.getsize(output_path) / (1024**3)
                feedback.pushInfo(f'✓ Arquivo criado: {file_size_gb:.2f} GB')
                
            except Exception as e:
                raise QgsProcessingException(f'Erro ao finalizar arquivo: {str(e)}')
            
            feedback.pushInfo('=' * 60)
            feedback.pushInfo('CONCLUÍDO COM SUCESSO!')
            feedback.pushInfo(f'Arquivo salvo: {output_path}')
            feedback.pushInfo('=' * 60)
            
            return {self.OUTPUT_RASTER: output_path}
            
        except QgsProcessingException:
            # Re-raise QgsProcessingException sem modificar
            raise
        except MemoryError as e:
            error_msg = (
                f'ERRO DE MEMÓRIA: {str(e)}\n\n'
                f'O raster é muito grande para processar.\n'
                f'Soluções:\n'
                f'1. Marque a opção "Force Chunked Processing"\n'
                f'2. Feche outros programas para liberar memória\n'
                f'3. Processe em uma máquina com mais RAM'
            )
            feedback.reportError(error_msg)
            raise QgsProcessingException(error_msg)
        except Exception as e:
            error_type = type(e).__name__
            error_msg = f'ERRO INESPERADO [{error_type}]: {str(e)}'
            feedback.reportError(error_msg)
            feedback.reportError('=' * 60)
            
            # Tentar obter mais informações do GDAL
            try:
                gdal_error = gdal.GetLastErrorMsg()
                gdal_error_num = gdal.GetLastErrorNo()
                if gdal_error:
                    feedback.reportError(f'GDAL Error #{gdal_error_num}: {gdal_error}')
            except:
                pass
            
            # Adicionar traceback para debug
            tb = traceback.format_exc()
            feedback.reportError('Traceback completo:')
            feedback.reportError(tb)
            feedback.reportError('=' * 60)
            
            raise QgsProcessingException(f'{error_type}: {str(e)}')