# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-05-20
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from typing import Dict, List, Tuple, Union
from uuid import uuid4

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner

from .affine import Affine
import numpy as np
from osgeo import gdal, ogr
from osgeo.gdal import Dataset
from qgis.core import (
    QgsFeature,
    QgsFields,
    QgsGeometry,
    QgsPoint,
    QgsProcessingUtils,
    QgsProject,
    QgsRasterLayer,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsProcessingContext,
    QgsPointXY,
    QgsRectangle,
    QgsCoordinateReferenceSystem,
    QgsProcessingException,
)

def readAsNumpy(
    inputRaster: Union[str, QgsRasterLayer], dtype=None, nodataValue=None
) -> Tuple[Dataset, np.array]:
    inputRaster = (
        inputRaster.dataProvider().dataSourceUri()
        if isinstance(inputRaster, QgsRasterLayer)
        else inputRaster
    )
    ds = gdal.Open(inputRaster)
    npArray = (
        np.array(ds.GetRasterBand(1).ReadAsArray().transpose())
        if dtype is None
        else np.array(ds.GetRasterBand(1).ReadAsArray().transpose(), dtype=dtype)
    )
    if nodataValue is not None:
        npArray[npArray == nodataValue] = np.nan
    return ds, npArray


def getCoordinateTransform(ds: Dataset) -> Affine:
    return Affine.from_gdal(*ds.GetGeoTransform())


def getMaxCoordinatesFromNpArray(npArray: np.array) -> np.array:
    return np.argwhere(npArray == npArray[~np.isnan(npArray)].max())


def getMinCoordinatesFromNpArray(npArray: np.array) -> np.array:
    return np.argwhere(npArray == npArray[~np.isnan(npArray)].min())


def createFeatureWithPixelValueFromPixelCoordinates(
    pixelCoordinates: Tuple[float, float],
    fieldName: str,
    fields: QgsFields,
    npRaster: np.array,
    transform: Affine,
    defaultAtributeMap: Dict = None,
) -> QgsFeature:
    newFeat = QgsFeature(fields)
    terrainCoordinates = transform * pixelCoordinates
    newFeat.setGeometry(QgsGeometry(QgsPoint(*terrainCoordinates)))
    try:
        value = npRaster[pixelCoordinates]
    except:
        return None
    if np.isnan(value):
        return None
    newFeat[fieldName] = int(value)
    if defaultAtributeMap is None:
        return newFeat
    for attr, value in defaultAtributeMap.items():
        newFeat[attr] = value
    return newFeat


def createFeatureListWithPixelValuesFromPixelCoordinatesArray(
    pixelCoordinates: np.array,
    fieldName: str,
    fields: QgsFields,
    npRaster: np.array,
    transform: Affine,
    defaultAtributeMap: Dict = None,
) -> List[QgsFeature]:
    return list(
        filter(
            lambda x: x is not None,
            (
                createFeatureWithPixelValueFromPixelCoordinates(
                    tuple(coords),
                    fieldName,
                    fields,
                    npRaster,
                    transform,
                    defaultAtributeMap=defaultAtributeMap,
                )
                for coords in pixelCoordinates
            ),
        )
    )


def createFeatureListWithPointList(
    pointList: List[QgsPoint],
    fieldName: str,
    fields: QgsFields,
    npRaster: np.array,
    transform: Affine,
    defaultAtributeMap: Dict = None,
) -> List[QgsFeature]:
    return [
        createFeatureWithPixelValueFromTerrainCoordinates(
            tuple(
                point.geometry().asMultiPoint()[0]
                if point.geometry().isMultipart()
                else point.geometry().asPoint()
            ),
            fieldName,
            fields,
            npRaster,
            transform,
            defaultAtributeMap,
        )
        for point in pointList
    ]


def createFeatureWithPixelValueFromTerrainCoordinates(
    terrainCoordinates: Tuple[float, float],
    fieldName: str,
    fields: QgsFields,
    npRaster: np.array,
    transform: Affine,
    defaultAtributeMap: Dict = None,
) -> QgsFeature:
    newFeat = QgsFeature(fields)
    pixelCoordinates = ~transform * terrainCoordinates
    pixelCoordinates = tuple(map(int, pixelCoordinates))
    try:
        value = npRaster[pixelCoordinates]
    except:
        return None
    if np.isnan(value):
        return None
    newFeat.setGeometry(QgsGeometry(QgsPoint(*terrainCoordinates)))
    newFeat[fieldName] = int(value)
    if defaultAtributeMap is None:
        return newFeat
    for attr, value in defaultAtributeMap.items():
        newFeat[attr] = value
    return newFeat


def buildNumpyNodataMask(rasterLyr: QgsRasterLayer, vectorLyr: QgsVectorLayer):
    _out = QgsProcessingUtils.generateTempFilename(f"clip_{str(uuid4().hex)}.tif")
    _temp_in = QgsProcessingUtils.generateTempFilename(f"feats_{str(uuid4().hex)}.shp")

    NoData_value = -9999
    x_res = rasterLyr.rasterUnitsPerPixelX()
    y_res = rasterLyr.rasterUnitsPerPixelY()
    x_min, y_min, x_max, y_max = rasterLyr.extent().toRectF().getCoords()

    # 4. Create Target - TIFF
    cols = int((x_max - x_min) / x_res)
    rows = int((y_max - y_min) / y_res)

    _raster = gdal.GetDriverByName("GTiff").Create(_out, cols, rows, 1, gdal.GDT_Byte)
    _raster.SetGeoTransform((x_min, x_res, 0, y_max, 0, -y_res))
    _band = _raster.GetRasterBand(1)
    _band.SetNoDataValue(NoData_value)

    if vectorLyr is None or vectorLyr.featureCount() == 0:
        _raster = None
        ds = gdal.Open(_out)
        npRaster = np.array(ds.GetRasterBand(1).ReadAsArray())
        ds = None
        return npRaster

    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "ESRI Shapefile"
    save_options.fileEncoding = "UTF-8"
    transform_context = QgsProject.instance().transformContext()
    error = QgsVectorFileWriter.writeAsVectorFormatV3(
        vectorLyr, _temp_in, transform_context, save_options
    )

    # 3. Open Shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    source_ds = driver.Open(_temp_in, 0)
    source_layer = source_ds.GetLayer()

    gdal.RasterizeLayer(_raster, [1], source_layer, burn_values=[255.0])
    _raster = None
    ds = gdal.Open(_out)
    npRaster = np.array(ds.GetRasterBand(1).ReadAsArray(), dtype=float)
    ds = None
    npRaster[npRaster == 255.0] = np.nan
    return npRaster


def createMaxPointFeatFromRasterLayer(
    inputRaster: QgsRasterLayer,
    fields: QgsFields,
    fieldName: str,
    defaultAtributeMap: Dict = None,
    maxValue: float = None,
    minValue: float = None,
) -> QgsFeature:
    ds, npRaster = readAsNumpy(inputRaster)
    transform = getCoordinateTransform(ds)
    nanIndexes = np.isnan(npRaster)
    npRaster = (np.rint(npRaster)).astype(float)
    npRaster[nanIndexes] = np.nan
    if maxValue is not None:
        npRaster[npRaster >= maxValue] = np.nan
    if minValue is not None:
        npRaster[npRaster <= minValue] = np.nan
    pixelCoordinates = getMaxCoordinatesFromNpArray(npRaster)
    pixelCoordinates = (
        tuple(pixelCoordinates.reshape(1, -1)[0])
        if pixelCoordinates.shape[0] == 1
        else tuple(pixelCoordinates[0])
    )
    return createFeatureWithPixelValueFromPixelCoordinates(
        pixelCoordinates=pixelCoordinates,
        fieldName=fieldName,
        fields=fields,
        npRaster=npRaster,
        transform=transform,
        defaultAtributeMap=defaultAtributeMap,
    )


def createMaxPointFeatListFromRasterLayer(
    inputRaster: QgsRasterLayer,
    fields: QgsFields,
    fieldName: str,
    defaultAtributeMap: Dict = None,
) -> List[QgsFeature]:
    ds, npRaster = readAsNumpy(inputRaster)
    transform = getCoordinateTransform(ds)
    nanIndexes = np.isnan(npRaster)
    npRaster = (np.rint(npRaster)).astype(float)
    npRaster[nanIndexes] = np.nan
    pixelCoordinates = getMaxCoordinatesFromNpArray(npRaster)
    return createFeatureListWithPixelValuesFromPixelCoordinatesArray(
        pixelCoordinates=pixelCoordinates,
        fieldName=fieldName,
        fields=fields,
        npRaster=npRaster,
        transform=transform,
        defaultAtributeMap=defaultAtributeMap,
    )


def writeOutputRaster(outputRaster, npRaster, ds=None, outputType=None):
    driver = gdal.GetDriverByName("GTiff")
    ds = (
        ds
        if ds is not None
        else driver.Create(
            outputRaster,
            int(npRaster.shape[1]),
            int(npRaster.shape[0]),
            1,
            gdal.GDT_Int16,
        )
    )
    try:
        # 1. Check if file is in use
        if os.path.exists(outputRaster):
            try:
                with open(outputRaster, "r+b"):
                    pass
            except IOError:
                raise RuntimeError(f"Output file {outputRaster} is locked or in use")

        # 2. Check directory permissions
        output_dir = os.path.dirname(outputRaster)
        if not os.access(output_dir, os.W_OK):
            raise RuntimeError(f"No write permission in directory {output_dir}")

        # 3. Verify input data
        if npRaster is None or ds is None:
            raise ValueError("Input raster or dataset is None")

        # 5. Verify array isn't empty and has valid dimensions
        if npRaster.size == 0 or len(npRaster.shape) != 2:
            raise ValueError(f"Invalid array shape: {npRaster.shape}")

        outputType = gdal.GDT_Int32 if outputType is None else outputType
        options = ["COMPRESS=LZW", "TILED=YES"]

        # 6. Verify driver
        if driver is None:
            raise RuntimeError("Failed to get GTiff driver")

        # 7. Create output dataset with error catching
        mem_driver = gdal.GetDriverByName("MEM")
        temp_ds = mem_driver.Create(
            "", int(npRaster.shape[1]), int(npRaster.shape[0]), 1, gdal.GDT_Int16
        )

        temp_ds.SetProjection(ds.GetProjection())
        temp_ds.SetGeoTransform(ds.GetGeoTransform())
        temp_ds.GetRasterBand(1).SetNoDataValue(-9999)
        temp_ds.GetRasterBand(1).WriteArray(npRaster.astype(np.int16))

        translate_options = gdal.TranslateOptions(
            format="GTiff", creationOptions=["COMPRESS=LZW", "TILED=YES"]
        )

        gdal.Translate(outputRaster, temp_ds, options=translate_options)

    except Exception as e:
        import traceback

        error_msg = f"Failed to write raster:\n{str(e)}\n{traceback.format_exc()}"
        raise RuntimeError(error_msg)
    finally:
        # Clean up
        if "temp_ds" in locals() and temp_ds is not None:
            temp_ds = None


def getNumpyViewFromPolygon(
    npRaster: np.array,
    transform: Affine,
    geom: QgsGeometry,
    pixelBuffer: int = 2,
    returnWindow=False,
) -> np.array:
    bbox = geom.boundingBox()
    terrain_xmin, terrain_ymin, terrain_xmax, terrain_ymax = bbox.toRectF().getCoords()
    a, b = map(int, ~transform * (terrain_xmin, terrain_ymin))
    c, d = map(int, ~transform * (terrain_xmax, terrain_ymax))
    xmin, xmax = min(a, c), max(a, c)
    ymin, ymax = min(b, d), max(b, d)

    x_start = max(xmin - pixelBuffer, 0)
    x_end = min(xmax + pixelBuffer + 1, npRaster.shape[0])
    y_start = max(ymin - pixelBuffer, 0)
    y_end = min(ymax + pixelBuffer + 1, npRaster.shape[1])

    npView = npRaster[x_start:x_end, y_start:y_end]
    return npView if not returnWindow else npView, {
        "x_start": x_start,
        "x_end": x_end,
        "y_start": y_start,
        "y_end": y_end,
    }


def getNumpyViewAndMaskFromPolygon(
    npRaster: np.array,
    transform: Affine,
    geom: QgsGeometry,
    pixelBuffer: int = 2,
    returnWindow=False,
) -> Union[Tuple[np.array, np.array], Tuple[np.array, np.array, Dict[str, float]]]:
    """
    Get a view of the numpy array for a polygon and create a mask of pixels that intersect with the polygon.
    Strictly contains modifications within polygon boundaries.

    Parameters:
        npRaster: The input numpy array
        transform: Affine transform from pixel to world coordinates
        geom: The polygon geometry
        pixelBuffer: Buffer in pixels around the polygon bbox

    Returns:
        Tuple of (array view, mask array) where mask is NaN inside polygon and original raster value outside
    """
    bbox = geom.boundingBox()
    terrain_xmin, terrain_ymin, terrain_xmax, terrain_ymax = bbox.toRectF().getCoords()

    # Convert terrain coordinates to pixel coordinates
    a, b = map(int, ~transform * (terrain_xmin, terrain_ymin))
    c, d = map(int, ~transform * (terrain_xmax, terrain_ymax))
    xmin, xmax = min(a, c), max(a, c)
    ymin, ymax = min(b, d), max(b, d)

    # Calculate view boundaries with buffer
    view_xmin = max(xmin - pixelBuffer, 0)
    view_xmax = min(xmax + pixelBuffer + 1, npRaster.shape[0])
    view_ymin = max(ymin - pixelBuffer, 0)
    view_ymax = min(ymax + pixelBuffer + 1, npRaster.shape[1])

    # Get the view of the raster
    npView = npRaster[view_xmin:view_xmax, view_ymin:view_ymax]

    # Create mask array initialized with the original raster values
    mask = np.zeros(npView.shape)

    # Iterate through pixels in the view
    for i in range(view_xmax - view_xmin):
        for j in range(view_ymax - view_ymin):
            # Get pixel coordinates
            pixel_x = view_xmin + i
            pixel_y = view_ymin + j

            # Get pixel corners in world coordinates
            corners = [
                transform * (pixel_x, pixel_y),  # Upper left
                transform * (pixel_x + 1, pixel_y),  # Upper right
                transform * (pixel_x + 1, pixel_y + 1),  # Lower right
                transform * (pixel_x, pixel_y + 1),  # Lower left
            ]

            # Get center point
            center_x, center_y = transform * (pixel_x + 0.5, pixel_y + 0.5)
            center_point = QgsGeometry.fromPointXY(QgsPointXY(center_x, center_y))

            # Create pixel polygon from corners
            pixel_poly = QgsGeometry.fromPolygonXY(
                [[QgsPointXY(*corner) for corner in corners]]
            )

            # Check if pixel is completely inside polygon
            if geom.contains(center_point) and geom.intersects(pixel_poly):
                mask[i, j] = np.nan
    if not returnWindow:
        return npView, mask
    else:
        return (
            npView,
            mask,
            {
                "x_start": view_xmin,
                "x_end": view_xmax,
                "y_start": view_ymin,
                "y_end": view_ymax,
            },
        )


def buildNumpyNodataMaskForPolygon(
    x_res, y_res, npRaster, geom: QgsGeometry, crs, valueToBurnAsMask=np.nan
):
    _out = QgsProcessingUtils.generateTempFilename(f"clip_{str(uuid4().hex)}.tif")
    _temp_in = QgsProcessingUtils.generateTempFilename(f"feats_{str(uuid4().hex)}.shp")

    NoData_value = -9999
    bbox = geom.boundingBox()
    x_min, y_min, x_max, y_max = bbox.toRectF().getCoords()

    # 4. Create Target - TIFF
    cols, rows = npRaster.shape
    # cols = int((x_max - x_min) / x_res)
    # rows = int((y_max - y_min) / y_res)

    _raster = gdal.GetDriverByName("GTiff").Create(_out, cols, rows, 1, gdal.GDT_Byte)
    # _raster.SetGeoTransform(transform.to_gdal())
    _raster.SetGeoTransform((x_min, x_res, 0, y_max, 0, -y_res))
    _band = _raster.GetRasterBand(1)
    _band.SetNoDataValue(NoData_value)

    vectorLyr = LayerHandler().createMemoryLayerFromGeometry(geom, crs)

    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "ESRI Shapefile"
    save_options.fileEncoding = "UTF-8"
    transform_context = QgsProject.instance().transformContext()
    error = QgsVectorFileWriter.writeAsVectorFormatV3(
        vectorLyr, _temp_in, transform_context, save_options
    )

    # 3. Open Shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    source_ds = driver.Open(_temp_in, 0)
    source_layer = source_ds.GetLayer()

    gdal.RasterizeLayer(_raster, [1], source_layer, burn_values=[255.0])
    _raster = None
    ds = gdal.Open(_out)
    outputNpRaster = np.array(ds.GetRasterBand(1).ReadAsArray(), dtype=float)
    ds = None
    outputNpRaster[outputNpRaster == 255.0] = valueToBurnAsMask
    return outputNpRaster


def polygonizeFromNumpyArray(npRaster, ds):
    _out = QgsProcessingUtils.generateTempFilename(f"polygonize_{str(uuid4().hex)}.tif")
    writeOutputRaster(_out, npRaster, ds)
    outputLyr = AlgRunner().runGdalPolygonize(
        inputRaster=_out,
        context=QgsProcessingContext(),
    )
    return outputLyr

def rasterizePolygonsToFile(
    vectorLayer: QgsVectorLayer,
    classField: str,
    outputPath: str,
    bbox: QgsRectangle = None,
    pixelSize: float = None,
    crs: QgsCoordinateReferenceSystem = None,
    nodataValue: int = -9999,
    dtype: str = "int16",
    width: int = None,
    height: int = None,
    transform_affine = None,
) -> None:
    """
    Rasteriza uma camada de polígonos para um arquivo GeoTIFF.
    
    Esta função usa rasterio para criar uma máscara de segmentação onde cada
    pixel tem o valor do campo de classe do polígono que o contém.
    
    Args:
        vectorLayer: Camada vetorial com os polígonos
        classField: Nome do campo que contém os valores de classe (inteiros)
        outputPath: Caminho completo para o arquivo de saída (.tif)
        bbox: Bounding box da área a ser rasterizada (QgsRectangle) - opcional se width/height/transform forem fornecidos
        pixelSize: Tamanho do pixel em unidades do CRS - opcional se width/height/transform forem fornecidos
        crs: Sistema de coordenadas de referência
        nodataValue: Valor para pixels sem dados (padrão: -9999)
        dtype: Tipo de dados do raster ('int16', 'int32', 'uint8', 'uint16', etc.)
        width: Largura específica do raster (opcional, tem prioridade sobre cálculo via bbox)
        height: Altura específica do raster (opcional, tem prioridade sobre cálculo via bbox)
        transform_affine: Transformação afim específica (opcional, tem prioridade sobre cálculo via bbox)
    
    Raises:
        ImportError: Se rasterio não estiver instalado
        QgsProcessingException: Se houver erro no processamento
    """
    try:
        import rasterio
        from rasterio.features import rasterize
        from rasterio.transform import from_bounds
    except ImportError:
        raise ImportError(
            "A biblioteca 'rasterio' não está instalada. "
            "Instale com: pip install rasterio"
        )
    
    import json
    
    try:
        # Verificar se o campo existe
        field_names = [field.name() for field in vectorLayer.fields()]
        if classField not in field_names:
            raise QgsProcessingException(
                f'Campo "{classField}" não encontrado na camada'
            )
        
        # Verificar se há features
        if vectorLayer.featureCount() == 0:
            raise QgsProcessingException("Camada não contém features")
        
        # Calcular dimensões do raster
        if width is not None and height is not None and transform_affine is not None:
            # Usar dimensões e transform fornecidos (modo de compatibilidade)
            transform = transform_affine
        else:
            # Calcular a partir do bbox e pixelSize
            if bbox is None or pixelSize is None:
                raise QgsProcessingException(
                    "bbox e pixelSize são obrigatórios quando width/height/transform não são fornecidos"
                )
            
            xmin, ymin, xmax, ymax = bbox.toRectF().getCoords()
            width = int(np.ceil((xmax - xmin) / pixelSize))
            height = int(np.ceil((ymax - ymin) / pixelSize))
            
            if width <= 0 or height <= 0:
                raise QgsProcessingException(
                    f"Dimensões inválidas do raster: {width}x{height}"
                )
            
            # Criar transformação afim
            transform = from_bounds(xmin, ymin, xmax, ymax, width, height)
        
        # Preparar shapes para rasterização (geometrias + valores)
        shapes = []
        for feature in vectorLayer.getFeatures():
            geom = feature.geometry()
            if geom is None or geom.isEmpty():
                continue
            
            # Obter valor da classe
            class_value = feature[classField]
            if class_value is None:
                continue
            
            try:
                class_value = int(class_value)
            except (ValueError, TypeError):
                continue
            
            # Converter geometria QGIS para formato GeoJSON usando asJson()
            try:
                geom_json = geom.asJson()
                geom_dict = json.loads(geom_json)
            except Exception as e:
                # Se asJson() falhar, tentar com shapely
                try:
                    from shapely.wkt import loads as wkt_loads
                    from shapely.geometry import mapping
                    
                    wkt = geom.asWkt()
                    shapely_geom = wkt_loads(wkt)
                    geom_dict = mapping(shapely_geom)
                except ImportError:
                    raise QgsProcessingException(
                        f"Erro ao converter geometria. "
                        f"Instale shapely: pip install shapely"
                    )
                except Exception as e2:
                    raise QgsProcessingException(
                        f"Erro ao converter geometria: {str(e2)}"
                    )
            
            shapes.append((geom_dict, class_value))
        
        if not shapes:
            raise QgsProcessingException(
                "Nenhuma geometria válida encontrada para rasterizar"
            )
        
        # Mapear dtype string para numpy dtype
        dtype_map = {
            'int16': np.int16,
            'int32': np.int32,
            'uint8': np.uint8,
            'uint16': np.uint16,
            'float32': np.float32,
            'float64': np.float64,
        }
        np_dtype = dtype_map.get(dtype, np.int16)
        
        # Rasterizar
        raster_array = rasterize(
            shapes=shapes,
            out_shape=(height, width),
            transform=transform,
            fill=nodataValue,
            dtype=np_dtype,
            all_touched=True,  # Incluir pixels que tocam os polígonos
        )
        
        # Salvar como GeoTIFF
        with rasterio.open(
            outputPath,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=np_dtype,
            crs=crs.toWkt() if crs else None,
            transform=transform,
            nodata=nodataValue,
            compress='lzw',
            tiled=True,
        ) as dst:
            dst.write(raster_array, 1)
    
    except ImportError:
        raise
    except QgsProcessingException:
        raise
    except Exception as e:
        import traceback
        raise QgsProcessingException(
            f"Erro ao rasterizar polígonos: {str(e)}\n{traceback.format_exc()}"
        )

def calculateSegmentationMetrics(
    ground_truth_path: str,
    prediction_path: str,
    nodata_value: int = -9999,
    class_names: dict = None,
) -> dict:
    """
    Calcula métricas e retorna contadores brutos (TP, FP, FN).
    Wrapper que lê arquivos e chama calculateSegmentationMetricsFromArrays.
    """
    try:
        import rasterio
    except ImportError:
        raise ImportError("A biblioteca 'rasterio' não está instalada.")
    
    import numpy as np
    
    with rasterio.open(ground_truth_path) as gt_src:
        ground_truth = gt_src.read(1)
    
    with rasterio.open(prediction_path) as pred_src:
        prediction = pred_src.read(1)
    
    return calculateSegmentationMetricsFromArrays(
        ground_truth, prediction, nodata_value, class_names
    )

def rasterizePolygonsToArray(
    vectorLayer: QgsVectorLayer,
    classField: str,
    bbox: QgsRectangle,
    pixelSize: float,
    nodataValue: int = 0,
    dtype: str = "uint8",
) -> np.ndarray:
    """
    Rasteriza uma camada de polígonos para um array numpy.
    
    Similar a rasterizePolygonsToFile, mas retorna um array numpy em vez
    de salvar em arquivo.
    
    Args:
        vectorLayer: Camada vetorial com os polígonos
        classField: Nome do campo que contém os valores de classe (inteiros)
        bbox: Bounding box da área a ser rasterizada (QgsRectangle)
        pixelSize: Tamanho do pixel em unidades do CRS
        nodataValue: Valor para pixels sem dados (padrão: 0)
        dtype: Tipo de dados do raster ('uint8', 'uint16', 'int16', 'int32', etc.)
    
    Returns:
        Array numpy com os valores rasterizados
    
    Raises:
        ImportError: Se rasterio não estiver instalado
        QgsProcessingException: Se houver erro no processamento
    """
    try:
        import rasterio
        from rasterio.features import rasterize
        from rasterio.transform import from_bounds
    except ImportError:
        raise ImportError(
            "A biblioteca 'rasterio' não está instalada. "
            "Instale com: pip install rasterio"
        )
    
    import json
    
    try:
        # Verificar se o campo existe
        field_names = [field.name() for field in vectorLayer.fields()]
        if classField not in field_names:
            raise QgsProcessingException(
                f'Campo "{classField}" não encontrado na camada'
            )
        
        # Verificar se há features
        if vectorLayer.featureCount() == 0:
            raise QgsProcessingException("Camada não contém features")
        
        # Calcular dimensões do raster
        xmin, ymin, xmax, ymax = bbox.toRectF().getCoords()
        width = int(np.ceil((xmax - xmin) / pixelSize))
        height = int(np.ceil((ymax - ymin) / pixelSize))
        
        if width <= 0 or height <= 0:
            raise QgsProcessingException(
                f"Dimensões inválidas do raster: {width}x{height}"
            )
        
        # Criar transformação afim
        transform = from_bounds(xmin, ymin, xmax, ymax, width, height)
        
        # Preparar shapes para rasterização (geometrias + valores)
        shapes = []
        for feature in vectorLayer.getFeatures():
            geom = feature.geometry()
            if geom is None or geom.isEmpty():
                continue
            
            # Obter valor da classe
            class_value = feature[classField]
            if class_value is None:
                continue
            
            try:
                class_value = int(class_value)
            except (ValueError, TypeError):
                continue
            
            # Converter geometria QGIS para formato GeoJSON usando asJson()
            try:
                geom_json = geom.asJson()
                geom_dict = json.loads(geom_json)
            except Exception as e:
                # Se asJson() falhar, tentar com shapely
                try:
                    from shapely.wkt import loads as wkt_loads
                    from shapely.geometry import mapping
                    
                    wkt = geom.asWkt()
                    shapely_geom = wkt_loads(wkt)
                    geom_dict = mapping(shapely_geom)
                except ImportError:
                    raise QgsProcessingException(
                        f"Erro ao converter geometria. "
                        f"Instale shapely: pip install shapely"
                    )
                except Exception as e2:
                    raise QgsProcessingException(
                        f"Erro ao converter geometria: {str(e2)}"
                    )
            
            shapes.append((geom_dict, class_value))
        
        if not shapes:
            raise QgsProcessingException(
                "Nenhuma geometria válida encontrada para rasterizar"
            )
        
        # Mapear dtype string para numpy dtype
        dtype_map = {
            'int16': np.int16,
            'int32': np.int32,
            'uint8': np.uint8,
            'uint16': np.uint16,
            'float32': np.float32,
            'float64': np.float64,
        }
        np_dtype = dtype_map.get(dtype, np.int16)
        
        # Rasterizar
        raster_array = rasterize(
            shapes=shapes,
            out_shape=(height, width),
            transform=transform,
            fill=nodataValue,
            dtype=np_dtype,
            all_touched=True,
        )
        
        return raster_array
    
    except ImportError:
        raise
    except QgsProcessingException:
        raise
    except Exception as e:
        import traceback
        raise QgsProcessingException(
            f"Erro ao rasterizar polígonos: {str(e)}\n{traceback.format_exc()}"
        )

def clipRasterByVectorMask(
    input_raster_path: str,
    mask_layer: QgsVectorLayer,
    output_path: str,
    nodata_value: int = -9999,
) -> str:
    """
    Clipa um raster usando uma máscara vetorial.
    
    Args:
        input_raster_path: Caminho do raster de entrada
        mask_layer: Camada vetorial com a máscara (deve ter uma feature)
        output_path: Caminho do raster de saída
        nodata_value: Valor para pixels fora da máscara
    
    Returns:
        Caminho do raster de saída
    
    Raises:
        ImportError: Se rasterio não estiver instalado
        QgsProcessingException: Se houver erro no processamento
    """
    try:
        import rasterio
        from rasterio.mask import mask
        from rasterio.warp import calculate_default_transform, reproject, Resampling
    except ImportError:
        raise ImportError(
            "A biblioteca 'rasterio' não está instalada. "
            "Instale com: pip install rasterio"
        )
    
    import json
    from shapely.wkt import loads as wkt_loads
    
    try:
        # Obter a geometria da máscara
        features = list(mask_layer.getFeatures())
        if not features:
            raise QgsProcessingException("Camada de máscara não contém features")
        
        # Usar a primeira feature como máscara
        mask_geom = features[0].geometry()
        
        # Converter para shapely geometry
        wkt = mask_geom.asWkt()
        shapely_geom = wkt_loads(wkt)
        
        # Abrir o raster de entrada
        with rasterio.open(input_raster_path) as src:
            # Clipar o raster
            out_image, out_transform = mask(
                src,
                [shapely_geom],
                crop=True,
                nodata=nodata_value,
                all_touched=False,
            )
            
            # Atualizar metadados
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
                "nodata": nodata_value,
                "compress": "lzw",
                "tiled": True,
            })
            
            # Salvar o raster clipado
            with rasterio.open(output_path, "w", **out_meta) as dest:
                dest.write(out_image)
        
        return output_path
    
    except ImportError:
        raise
    except QgsProcessingException:
        raise
    except Exception as e:
        import traceback
        raise QgsProcessingException(
            f"Erro ao clipar raster: {str(e)}\n{traceback.format_exc()}"
        )

def calculateSegmentationMetricsFromArrays(
    ground_truth_array: np.ndarray,
    prediction_array: np.ndarray,
    nodata_value: int = -9999,
    class_names: dict = None,
) -> dict:
    """
    Calcula métricas diretamente dos arrays numpy (SEM I/O).
    Versão otimizada para processar tiles em memória.
    """
    if class_names is None:
        class_names = {}
    
    if ground_truth_array.shape != prediction_array.shape:
        raise ValueError(f"Dimensões diferentes: {ground_truth_array.shape} vs {prediction_array.shape}")
    
    valid_mask = (ground_truth_array != nodata_value) & (prediction_array != nodata_value)
    
    result = {}
    counts = {}
    
    if not valid_mask.any():
        result = {
            "accuracy": 0.0,
            "mean_iou": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "total_pixels": 0,
            "correct_pixels": 0,
            "raw_counts": {}
        }
        return result
    
    gt_valid = ground_truth_array[valid_mask]
    pred_valid = prediction_array[valid_mask]
    
    classes = np.unique(np.concatenate([gt_valid, pred_valid]))
    
    total_pixels = len(gt_valid)
    correct_pixels = np.sum(gt_valid == pred_valid)
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0
    
    result["accuracy"] = float(accuracy)
    result["total_pixels"] = int(total_pixels)
    result["correct_pixels"] = int(correct_pixels)
    
    ious, precisions, recalls, f1_scores = [], [], [], []
    
    for cls in classes:
        c = int(cls)
        tp = np.sum((gt_valid == c) & (pred_valid == c))
        fp = np.sum((gt_valid != c) & (pred_valid == c))
        fn = np.sum((gt_valid == c) & (pred_valid != c))
        
        counts[c] = {'tp': int(tp), 'fp': int(fp), 'fn': int(fn)}
        
        union = tp + fp + fn
        iou = tp / union if union > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        ious.append(iou)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
        
        class_name = class_names.get(c, f"Classe_{c}")
        prefix = f"class_{c}_{class_name}"
        result[f"{prefix}_iou"] = float(iou)
        result[f"{prefix}_precision"] = float(precision)
        result[f"{prefix}_recall"] = float(recall)
        result[f"{prefix}_f1_score"] = float(f1)

    result["mean_iou"] = float(np.mean(ious)) if ious else 0.0
    result["precision"] = float(np.mean(precisions)) if precisions else 0.0
    result["recall"] = float(np.mean(recalls)) if recalls else 0.0
    result["f1_score"] = float(np.mean(f1_scores)) if f1_scores else 0.0
    result["raw_counts"] = counts
    
    return result
