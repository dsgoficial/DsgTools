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

from typing import Dict, List, Tuple, Union
from uuid import uuid4

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
)


def readAsNumpy(inputRaster: Union[str, QgsRasterLayer]) -> Tuple[Dataset, np.array]:
    inputRasterPath = (
        inputRaster.dataProvider().dataSourceUri()
        if isinstance(inputRaster, QgsRasterLayer)
        else inputRaster
    )
    ds = gdal.Open(inputRasterPath)
    return ds, np.array(ds.GetRasterBand(1).ReadAsArray().transpose())


def getCoordinateTransform(ds: Dataset) -> Affine:
    return Affine.from_gdal(*ds.GetGeoTransform())


def getMaxCoordinatesFromNpArray(npArray: np.array) -> np.array:
    return np.argwhere(npArray == npArray[~np.isnan(npArray)].max())


def getMinCoordinatesFromNpArray(npArray: np.array) -> np.array:
    not_nan_mask = ~np.isnan(npArray)
    try:
        min_value = np.min(npArray[np.where((npArray > -500.) & not_nan_mask)])
    except:
        return np.array([])
    return np.transpose(np.where((npArray == min_value) & not_nan_mask))
    # return np.argwhere(npArray == npArray[~np.isnan(npArray)].min())


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
            lambda x: x is not None, (
                createFeatureWithPixelValueFromPixelCoordinates(
                    tuple(coords), fieldName, fields, npRaster, transform, defaultAtributeMap=defaultAtributeMap
                ) for coords in pixelCoordinates
            )
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
    inputRaster: QgsRasterLayer, fields: QgsFields, fieldName: str, defaultAtributeMap: Dict = None,
) -> QgsFeature:
    ds, npRaster = readAsNumpy(inputRaster)
    transform = getCoordinateTransform(ds)
    nanIndexes = np.isnan(npRaster)
    npRaster = (np.rint(npRaster)).astype(float)
    npRaster[nanIndexes] = np.nan
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
    inputRaster: QgsRasterLayer, fields: QgsFields, fieldName: str, defaultAtributeMap: Dict = None,
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
