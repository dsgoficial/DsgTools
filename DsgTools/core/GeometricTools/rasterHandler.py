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
from itertools import product
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
)


def readAsNumpy(inputRaster: Union[str, QgsRasterLayer], dtype=None, nodataValue=None) -> Tuple[Dataset, np.array]:
    inputRaster = (
        inputRaster.dataProvider().dataSourceUri()
        if isinstance(inputRaster, QgsRasterLayer)
        else inputRaster
    )
    ds = gdal.Open(inputRaster)
    npArray = np.array(ds.GetRasterBand(1).ReadAsArray().transpose()) if dtype is None else np.array(ds.GetRasterBand(1).ReadAsArray().transpose(), dtype=dtype)
    if nodataValue is not None:
        npArray[npArray==nodataValue] = np.nan
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

def writeOutputRaster(outputRaster, npRaster, ds, outputType=None):
    outputType = gdal.GDT_Int32 if outputType is None else outputType
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(
        outputRaster, npRaster.shape[1], npRaster.shape[0], 1, outputType
    )
    out_ds.SetProjection(ds.GetProjection())
    out_ds.SetGeoTransform(ds.GetGeoTransform())
    out_ds.GetRasterBand(1).SetNoDataValue(-9999)
    band = out_ds.GetRasterBand(1)
    band.WriteArray(npRaster)
    band.FlushCache()
    band.ComputeStatistics(False)
    out_ds = None

def getNumpyViewFromPolygon(npRaster: np.array, transform: Affine, geom: QgsGeometry, pixelBuffer: int = 2) -> np.array:
    bbox = geom.boundingBox()
    terrain_xmin, terrain_ymin, terrain_xmax, terrain_ymax = bbox.toRectF().getCoords()
    a, b = map(int, ~transform * (terrain_xmin, terrain_ymin))
    c, d = map(int, ~transform * (terrain_xmax, terrain_ymax))
    xmin, xmax = min(a, c), max(a, c)
    ymin, ymax = min(b, d), max(b, d)
    npView = npRaster[max(xmin-pixelBuffer, 0):xmax+pixelBuffer+1, max(ymin-pixelBuffer, 0):ymax+pixelBuffer+1]
    return npView

def getNumpyViewAndMaskFromPolygon(npRaster: np.array, transform: Affine, geom: QgsGeometry, pixelBuffer: int = 2) -> Tuple[np.array, np.array]:
    bbox = geom.boundingBox()
    terrain_xmin, terrain_ymin, terrain_xmax, terrain_ymax = bbox.toRectF().getCoords()
    a, b = map(int, ~transform * (terrain_xmin, terrain_ymin))
    c, d = map(int, ~transform * (terrain_xmax, terrain_ymax))
    xmin, xmax = min(a, c), max(a, c)
    ymin, ymax = min(b, d), max(b, d)
    npView = npRaster[max(xmin-pixelBuffer, 0):xmax+pixelBuffer+1, max(ymin-pixelBuffer, 0):ymax+pixelBuffer+1]
    mask = np.zeros((1, npView.shape[0] * npView.shape[1]))
    productPairList = list(product(range(max(xmin-pixelBuffer, 0), xmax+pixelBuffer+1), range(max(ymin-pixelBuffer, 0), ymax+pixelBuffer+1)))
    maxIdx = npView.shape[0] * npView.shape[1]
    for idx, transformedPair in enumerate(productPairList):
        transfCoord = transform * transformedPair
        candGeom = QgsGeometry(QgsPoint(*transfCoord))
        if not candGeom.intersects(geom):
            continue
        if idx >= maxIdx:
            break
        mask[:, idx] = np.nan
    mask = mask.reshape(npView.shape)
    return npView, mask


def buildNumpyNodataMaskForPolygon(x_res, y_res, npRaster, geom: QgsGeometry, crs, valueToBurnAsMask=np.nan):
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

    vectorLyr = LayerHandler().createMemoryLayerFromGeometry(
        geom, crs
    )

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
