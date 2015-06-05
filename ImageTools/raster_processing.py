from osgeo import gdal, osr
import sys
import colorsys
import numpy

class RasterProcess():
    def __init__(self, rgbfile, panfile):
        # this allows GDAL to throw Python Exceptions
        gdal.UseExceptions()

        try:
            self.rgb = gdal.Open( rgbfile )
        except RuntimeError, e:
            print 'Unable to open rgb image'
            print e

            sys.exit(1)

        try:
            self.pan = gdal.Open( panfile )
        except RuntimeError, e:
            print 'Unable to open pan image'
            print e

            sys.exit(1)

    def __del__(self):
        self.rgb = None
        self.pan = None

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

    def createRasterFromRGBbands(self, red, green, blue, destfile):
        cols = self.rgb.RasterXSize
        rows = self.rgb.RasterYSize

        (xOrigin, yOrigin, pixelWidth, pixelHeight) = self.getGeoreferenceInfo(self.rgb)

        targetSR = self.getCRS(self.rgb)

        driver = gdal.GetDriverByName('GTiff')

        outRaster = driver.Create(destfile, cols, rows, 3, gdal.GDT_Byte)
        outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))

        outRaster.GetRasterBand(1).WriteArray(red)
        outRaster.GetRasterBand(2).WriteArray(green)
        outRaster.GetRasterBand(3).WriteArray(blue)

        outRaster.SetProjection(targetSR.ExportToWkt())

    def pansharpenImage(self, destfile):
        red = self.getBandAsArray(self.rgb, 1)
        green = self.getBandAsArray(self.rgb, 2)
        blue = self.getBandAsArray(self.rgb, 3)

        pan = self.getBandAsArray(self.pan, 1)

        rgb_to_hsv 	= numpy.vectorize(colorsys.rgb_to_hsv)
        hsv_to_rgb 	= numpy.vectorize(colorsys.hsv_to_rgb)

        h,s,v = rgb_to_hsv(red, green, blue)
        r,g,b = hsv_to_rgb(h, s, pan)

        self.createRasterFromRGBbands(r, g, b, destfile)

obj = RasterProcess("/Users/luiz/Downloads/WV24bandsample/superimposed.tif", "/Users/luiz/Downloads/WV24bandsample/pan_sample.tif")
# band = obj.getBandAsArray(1)
# obj.createRasterFromBandArray(band, "/Users/luiz/Downloads/landsat_sample/teste.tif")
obj.pansharpenImage("/Users/luiz/Downloads/WV24bandsample/sharpened.tif")