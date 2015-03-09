# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mosaicTools import Ui_Dialog

class MosaicTools(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor."""
        super(MosaicTools, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        print "foi"
        
    @pyqtSlot()
    def on_procuraSRButton_clicked(self):
        print "procuraSR"
        
    @pyqtSlot()
    def on_addButton_clicked(self):
        print "addButton"
        
    @pyqtSlot()
    def on_removeButton_clicked(self):
        print "removeButton"
        
    @pyqtSlot()
    def on_addFolderButton_clicked(self):
        print "addFolderButton"
    
    @pyqtSlot()
    def on_outputFolderButton_clicked(self):
        print "outputFolderButton"
    
    #Aplica realce de contraste, reprojecao e troca o tipo de numero utilizando a GDAL. 
    def stretchImage(inFile, outFile, percent, zone, bands, epsg=4674, maxOutValue=254, minOutValue=0):
        """Method that applies a specific histogram stretching to a group of images.
            The method also performs a conversion changing the raster type.
        """

        #Open image
        imgIn=gdal.Open(inFile)
        if not imgIn:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), self.tr("Failed to open input file."))
            return
        
        #Defining the output driver
        outDriver=imgIn.GetDriver()
        createOptions=['PHOTOMETRIC=RGB', 'ALPHA=NO']
        
        #creating temp file for contrast stretch
        outFileTmp=outFile+'tmp'
        
        #Creating a temp image, with the same input parameters, to store the converted input image to 8 bits
        imgOut=outDriver.Create(outFileTmp,imgIn.RasterXSize, imgIn.RasterYSize, len(bands), gdal.GDT_Byte, options = createOptions)
        imgOut.SetProjection(imgIn.GetProjection())
        imgOut.SetGeoTransform(imgIn.GetGeoTransform())
        
        #Linear stretching
        topPercent=1-percent/2
        bottomPercent=percent/2
        outBandNumber=1
        for bandNumber in bands:
            
            b1=imgIn.GetRasterBand(bandNumber+1)
            matrix=b1.ReadAsArray()
            arr=numpy.array(matrix)
            
            minValue, maxValue = numpy.percentile(matrix, [bottomPercent*100., topPercent*100.])
            print minValue, maxValue
    
            #Transformation parameters
            #Rouding the values out of bounds
            numpy.putmask(arr, arr>maxValue,maxValue)
            numpy.putmask(arr, arr<minValue,minValue)
            
            #The maxOutValue and the minOutValue must be set according to the convertion that will be applied (e.g. 8 bits, 16 bits, 32 bits)
            a=(maxOutValue-minOutValue)/(maxValue-minValue)
            newArr=numpy.floor((arr-minValue)*a+minOutValue)
            
            outB=imgOut.GetRasterBand(outBandNumber)
            outBandNumber+=1
            outB.WriteArray(newArr)
            outB.FlushCache()
              
            print "Band", bandNumber, ",", percentValue, ",",
        
        #creating final image for reprojection
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(epsg)
        
        #this code uses virtual raster to compute the parameters of the output image
        vrt = gdal.AutoCreateWarpedVRT(imgOut, None, outRasterSRS.ExportToWkt(), gdal.GRA_NearestNeighbour,  0.0)
        imgWGS=outDriver.CreateCopy(outFile, vrt, options = createOptions)
        
        #Checking if the output file was created with success
        if os.path.exists(outFile):
            QMessageBox.information(self.iface.mainWindow(), self.tr("Success!"), self.tr("File successfully created: ")+outFile)
        
        #Deleting the objects
        del imgWGS
        del imgOut    
        del imgIn
        
        #Unlinking the temp file
        os.unlink(outFileTmp)
