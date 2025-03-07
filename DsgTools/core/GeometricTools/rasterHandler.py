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
