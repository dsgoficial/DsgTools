from osgeo import gdal, osr
import sys
import colorsys
import numpy


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
            print 'Band ( %i ) not found' % band_num
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
        cols = srcraster.RasterXSize
        rows = srcraster.RasterYSize

        (xOrigin, yOrigin, pixelWidth, pixelHeight) = self.getGeoreferenceInfo(self.rgb)

        targetSR = self.getCRS(srcraster)

        driver = gdal.GetDriverByName('GTiff')

        outRaster = driver.Create(destfile, cols, rows, 3, gdal.GDT_Byte)
        outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))

        outRaster.GetRasterBand(1).WriteArray(red)
        outRaster.GetRasterBand(2).WriteArray(green)
        outRaster.GetRasterBand(3).WriteArray(blue)

        outRaster.SetProjection(targetSR.ExportToWkt())

    def pansharpenImage(self, rgbfile, panfile, destfile):
        rgb = self.openRaster(rgbfile)
        red = self.getBandAsArray(rgb, 1)
        green = self.getBandAsArray(rgb, 2)
        blue = self.getBandAsArray(rgb, 3)

        panraster = self.openRaster(panfile)
        pan = self.getBandAsArray(panraster, 1)

        rgb_to_hsv = numpy.vectorize(colorsys.rgb_to_hsv)
        hsv_to_rgb = numpy.vectorize(colorsys.hsv_to_rgb)

        h, s, v = rgb_to_hsv(red, green, blue)
        r, g, b = hsv_to_rgb(h, s, pan)

        self.createRasterFromRGBbands(rgb, r, g, b, destfile)

        rgb = None
        panraster = None


obj = RasterProcess()
obj.pansharpenImage("/Users/luiz/Downloads/WV24bandsample/superimposed.tif",
                    "/Users/luiz/Downloads/WV24bandsample/pan_sample.tif",
                    "/Users/luiz/Downloads/WV24bandsample/sharpened.tif")
