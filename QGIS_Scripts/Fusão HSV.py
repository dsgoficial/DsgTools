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

##DSG=group
##Arquivo_RGB=raster
##Arquivo_Pan=raster
##Arquivo_fusionado=output raster

from osgeo import gdal, osr
import sys
import colorsys
import numpy
import struct


class RasterProcess():
    def __init__(self):
        # this allows GDAL to throw Python Exceptions
        gdal.UseExceptions()

    def openRaster(self, file):
        try:
            raster = gdal.Open(file)
        except RuntimeError, e:
            print 'Unable to open image'
            print e

            sys.exit(1)

        return raster

    def getBandAsArray(self, raster, bandnumber):
        try:
            band = raster.GetRasterBand(bandnumber)
        except RuntimeError, e:
            # for example, try GetRasterBand(10)
            print 'Band ( %i ) not found' % bandnumber
            print e
            sys.exit(1)

        return band.ReadAsArray()

    def getGeoreferenceInfo(self, raster):
        # Get raster georeference info
        transform = raster.GetGeoTransform()
        xOrigin = transform[0]
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = transform[5]

        return (xOrigin, yOrigin, pixelWidth, pixelHeight)

    def getCRS(self, raster):
        targetSR = osr.SpatialReference()
        targetSR.ImportFromWkt(raster.GetProjectionRef())

        return targetSR

    def createRasterFromRGBbands(self, srcraster, red, green, blue, destfile):
        outRaster = self.createRaster(srcraster, destfile)
        
        outRaster.GetRasterBand(1).WriteArray(red)
        outRaster.GetRasterBand(2).WriteArray(green)
        outRaster.GetRasterBand(3).WriteArray(blue)

    def createRaster(self, srcraster, destfile):
        cols = srcraster.RasterXSize
        rows = srcraster.RasterYSize

        (xOrigin, yOrigin, pixelWidth, pixelHeight) = self.getGeoreferenceInfo(srcraster)

        targetSR = self.getCRS(srcraster)

        driver = gdal.GetDriverByName('GTiff')

        outRaster = driver.Create(destfile, cols, rows, 3, gdal.GDT_Float32)
        outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))
        outRaster.SetProjection(targetSR.ExportToWkt())
        
        return outRaster

    def pansharpenImage(self, rgbfile, panfile, destfile):
        rgb = self.openRaster(rgbfile)
        red = rgb.GetRasterBand(1)
        green = rgb.GetRasterBand(2)
        blue = rgb.GetRasterBand(3)

        panraster = self.openRaster(panfile)
        pan = panraster.GetRasterBand(1)
        
        rgb_to_hsv = numpy.vectorize(colorsys.rgb_to_hsv)
        hsv_to_rgb = numpy.vectorize(colorsys.hsv_to_rgb)

        outRaster = self.createRaster(rgb, destfile)
        outR = outRaster.GetRasterBand(1)
        outG = outRaster.GetRasterBand(2)
        outB = outRaster.GetRasterBand(3)

        if int(float(i)/sizeY*100)!=progress:
            progress=int(float(i)/sizeY*100)
            print "Linha: ", row, "de", sizeY, "(", progress , "%). Tempo restante estimado:", timePerCycle*(sizeY-row)  

        
        sizeX = pan.XSize
        sizeY = pan.YSize
        
        p = 0
        progress.setPercentage(p)
        for row in range(sizeY):
            redblock = self.readBlock(red, sizeX, 1, row, gdal.GDT_Byte)
            greenblock = self.readBlock(green, sizeX, 1, row, gdal.GDT_Byte)
            blueblock = self.readBlock(blue, sizeX, 1, row, gdal.GDT_Byte)
            
            panblock = self.readBlock(pan, sizeX, 1, row, gdal.GDT_Float32)
            
            h, s, v = rgb_to_hsv(redblock, greenblock, blueblock)
            r, g, b = hsv_to_rgb(h, s, panblock)
            
            self.writeBlock(outR, r, sizeX, 1, row, gdal.GDT_Float32)
            self.writeBlock(outG, g, sizeX, 1, row, gdal.GDT_Float32)
            self.writeBlock(outB, b, sizeX, 1, row, gdal.GDT_Float32)

            if int(float(row)/sizeY*100) != p:
                p = int(float(row)/sizeY*100)
                progress.setPercentage(p)

        rgb = None
        panraster = None
        outRaster = None
        
    def normalize(self, arr):
        ''' Function to normalize an input array to 0-1 '''
        arr_min = arr.min()
        arr_max = arr.max()
        return [(arr - arr_min) / (arr_max - arr_min)]*255
    
    def readBlock(self, band, sizeX, sizeY = 1, offsetY = 0, pixelType = gdal.GDT_Byte):
        numpytype = self.getNumpyType(pixelType)

        bandscanline =band.ReadRaster( 0, offsetY, sizeX, sizeY, sizeX, sizeY, pixelType )
        pixelArray=numpy.fromstring(bandscanline, dtype=numpytype)
        
        return pixelArray
    
    def getNumpyType(self, pixelType = gdal.GDT_Byte):
        numpytype = None
        if pixelType == gdal.GDT_Byte:
            numpytype = numpy.ubyte
        elif pixelType == gdal.GDT_Float32:
            numpytype = numpy.float32
            
        return numpytype
    
    def writeBlock(self, band, block, sizeX, sizeY = 1, offsetY = 0, pixelType = gdal.GDT_Byte):
        numpytype = self.getNumpyType(pixelType)

        band.WriteRaster(0, offsetY, sizeX, sizeY, block.astype(numpytype).tostring())

obj = RasterProcess()
obj.pansharpenImage(Arquivo_RGB,
                    Arquivo_Pan,
                    Arquivo_fusionado)
