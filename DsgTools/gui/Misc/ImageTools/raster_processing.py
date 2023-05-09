# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-06-05
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from __future__ import print_function

##DSG=group
##RGB_Layer=raster
##Pan_Layer=raster
##Pansharpened=output raster

from builtins import range
from builtins import object
from osgeo import gdal, osr
import sys
import colorsys
import numpy
import struct


class RasterProcess(object):
    def __init__(self):
        # this allows GDAL to throw Python Exceptions
        gdal.UseExceptions()

    def openRaster(self, file):
        """
        Opens a gdal raster file
        """
        try:
            raster = gdal.Open(file)
        except RuntimeError as e:
            # fix_print_with_import
            print("Unable to open image")
            # fix_print_with_import
            print(e)

            sys.exit(1)

        return raster

    def getBandAsArray(self, raster, bandnumber):
        """
        Gets a raster band as array
        raster: gdal raster file
        bandnumber: band number
        """
        try:
            band = raster.GetRasterBand(bandnumber)
        except RuntimeError as e:
            # for example, try GetRasterBand(10)
            # fix_print_with_import
            print("Band ( %i ) not found" % bandnumber)
            # fix_print_with_import
            print(e)
            sys.exit(1)

        return band.ReadAsArray()

    def getGeoreferenceInfo(self, raster):
        """
        Gets georeference information
        raster: raster file
        """
        # Get raster georeference info
        transform = raster.GetGeoTransform()
        xOrigin = transform[0]
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = transform[5]

        return (xOrigin, yOrigin, pixelWidth, pixelHeight)

    def getCRS(self, raster):
        """
        Gets raster file CRS
        """
        targetSR = osr.SpatialReference()
        targetSR.ImportFromWkt(raster.GetProjectionRef())

        return targetSR

    def createRasterFromRGBbands(self, srcraster, red, green, blue, destfile):
        """
        Creates a raster file from RGB bands
        srcraster: source raster file
        red: red band
        green: green band
        blue: blue band
        destfile: destination file
        """
        outRaster = self.createRaster(srcraster, destfile)

        outRaster.GetRasterBand(1).WriteArray(red)
        outRaster.GetRasterBand(2).WriteArray(green)
        outRaster.GetRasterBand(3).WriteArray(blue)

    def createRaster(self, srcraster, destfile, pixelType):
        """
        Creates a raster file
        srcraster: source raster
        destfile: destination file
        pixelType: raster pixel type (e.g byte)
        """
        cols = srcraster.RasterXSize
        rows = srcraster.RasterYSize

        (xOrigin, yOrigin, pixelWidth, pixelHeight) = self.getGeoreferenceInfo(
            srcraster
        )

        targetSR = self.getCRS(srcraster)

        driver = gdal.GetDriverByName("GTiff")

        outRaster = driver.Create(destfile, cols, rows, 3, pixelType)
        outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))
        outRaster.SetProjection(targetSR.ExportToWkt())

        return outRaster

    def pansharpenImage(self, rgbfile, panfile, destfile):
        """
        Performs a HSV fusion
        rgbfile: original RGB raster file
        panfile: original PAN raster file
        destfile: destination file
        """
        rgb = self.openRaster(rgbfile)
        red = rgb.GetRasterBand(1)
        green = rgb.GetRasterBand(2)
        blue = rgb.GetRasterBand(3)

        panraster = self.openRaster(panfile)
        pan = panraster.GetRasterBand(1)

        rgb_to_hsv = numpy.vectorize(colorsys.rgb_to_hsv)
        hsv_to_rgb = numpy.vectorize(colorsys.hsv_to_rgb)

        if red.DataType > pan.DataType:
            pixelType = red.DataType
        else:
            pixelType = pan.DataType

        outRaster = self.createRaster(rgb, destfile, pixelType)
        outR = outRaster.GetRasterBand(1)
        outG = outRaster.GetRasterBand(2)
        outB = outRaster.GetRasterBand(3)

        sizeX = pan.XSize
        sizeY = pan.YSize
        for row in range(sizeY):
            redblock = self.readBlock(red, sizeX, 1, row, red.DataType)
            greenblock = self.readBlock(green, sizeX, 1, row, green.DataType)
            blueblock = self.readBlock(blue, sizeX, 1, row, blue.DataType)

            panblock = self.readBlock(pan, sizeX, 1, row, pan.DataType)

            h, s, v = rgb_to_hsv(redblock, greenblock, blueblock)
            r, g, b = hsv_to_rgb(h, s, panblock)

            self.writeBlock(outR, r, sizeX, 1, row, pixelType)
            self.writeBlock(outG, g, sizeX, 1, row, pixelType)
            self.writeBlock(outB, b, sizeX, 1, row, pixelType)

        rgb = None
        panraster = None
        outRaster = None

    def normalize(self, arr):
        """
        Function to normalize an input array to 0-1
        """
        arr_min = arr.min()
        arr_max = arr.max()
        return [(arr - arr_min) / (arr_max - arr_min)] * 255

    def readBlock(self, band, sizeX, sizeY=1, offsetY=0, pixelType=gdal.GDT_Byte):
        """
        Reads image block
        band: band used
        sizeX: x block size
        sizeY: y block size
        offsetY: Y offset
        pixelType: pixel type
        """
        numpytype = self.getNumpyType(pixelType)

        bandscanline = band.ReadRaster(
            0, offsetY, sizeX, sizeY, sizeX, sizeY, pixelType
        )
        pixelArray = numpy.fromstring(bandscanline, dtype=numpytype)

        return pixelArray

    def getNumpyType(self, pixelType=gdal.GDT_Byte):
        """
        Translates the gdal raster type to numpy type
        pixelType: gdal raster type
        """
        if pixelType == gdal.GDT_Byte:
            return numpy.uint8
        elif pixelType == gdal.GDT_UInt16:
            return numpy.uint16
        elif pixelType == gdal.GDT_Int16:
            return numpy.int16
        elif pixelType == gdal.GDT_UInt32:
            return numpy.uint32
        elif pixelType == gdal.GDT_Int32:
            return numpy.int32
        elif pixelType == gdal.GDT_Float32:
            return numpy.float32
        elif pixelType == gdal.GDT_Float64:
            return numpy.float64

    def writeBlock(
        self, band, block, sizeX, sizeY=1, offsetY=0, pixelType=gdal.GDT_Byte
    ):
        """
        Writes image block
        band: band used
        sizeX: x block size
        sizeY: y block size
        offsetY: Y offset
        pixelType: pixel type
        """
        numpytype = self.getNumpyType(pixelType)

        band.WriteRaster(0, offsetY, sizeX, sizeY, block.astype(numpytype).tostring())


obj = RasterProcess()
obj.pansharpenImage(
    "/home/lclaudio/Documents/classificacao_rgb.tif",
    "/home/lclaudio/Documents/corte_amp.tif",
    "/home/lclaudio/Documents/teste.tif",
)
