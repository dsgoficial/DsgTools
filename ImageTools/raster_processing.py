from osgeo import gdal, osr
import sys
class RasterProcess():
    def __init__(self, rasterFile):
        # this allows GDAL to throw Python Exceptions
        gdal.UseExceptions()

        try:
            self.src_ds = gdal.Open( rasterFile )
        except RuntimeError, e:
            print 'Unable to open INPUT.tif'
            print e
            sys.exit(1)

    def getBandAsArray(self, bandnumber):
        try:
            band = self.src_ds.GetRasterBand(bandnumber)
        except RuntimeError, e:
            # for example, try GetRasterBand(10)
            print 'Band ( %i ) not found' % band_num
            print e
            sys.exit(1)

        return band.ReadAsArray()

    def getGeoreferenceInfo(self):
        # Get raster georeference info
        transform = self.src_ds.GetGeoTransform()
        xOrigin = transform[0]
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = transform[5]

        return (xOrigin, yOrigin, pixelWidth, pixelHeight)

    def getCRS(self):
        targetSR = osr.SpatialReference()
        targetSR.ImportFromWkt(self.src_ds.GetProjectionRef())

        return targetSR

    def createRasterFromBandArray(self, band, destfile):
        cols = band.shape[1]
        rows = band.shape[0]

        (xOrigin, yOrigin, pixelWidth, pixelHeight) = self.getGeoreferenceInfo()

        targetSR = self.getCRS()

        driver = gdal.GetDriverByName('GTiff')

        outRaster = driver.Create(destfile, cols, rows, 1, gdal.GDT_Byte)
        outRaster.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))

        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(band)

        outRaster.SetProjection(targetSR.ExportToWkt())

        outband.FlushCache()

obj = RasterProcess("/Users/luiz/Downloads/landsat_sample/sample.tif")
band = obj.getBandAsArray(1)
obj.createRasterFromBandArray(band, "/Users/luiz/Downloads/landsat_sample/teste.tif")