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
        mod history          : 2015-03-10 by Maurício de Paulo - Cartographic Engineer @ Brazilian Army
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
import osgeo.gdal
import osgeo.osr
import numpy

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import QgsCoordinateReferenceSystem, QgsMessageLog
from qgis.gui import QgsGenericProjectionSelector

from ui_processingTools import Ui_Dialog

class ProcessingTools(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor."""
        super(ProcessingTools, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface

        self.epsg = 4326
        srs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
        self.srLineEdit.setText(srs.description())

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        if self.fileListWidget.count() == 0:
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please select at least one image."))
            return

        if self.outputFolderEdit.text() == '':
            QMessageBox.warning(self.iface.mainWindow(), self.tr("Warning!"), self.tr("Please select at the output folder."))
            return

        QMessageBox.information(self.iface.mainWindow(), self.tr("Information!"), self.tr("The processing may take several minutes. Please wait the final message."))

        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            outDir = self.outputFolderEdit.text()
            for itemNumber in range(0,self.fileListWidget.count()):
                inFile = self.fileListWidget.item(itemNumber).text()
                self.stretchImage(str(inFile), str(outDir), self.getStretchingPercentage(), self.epsg)

            QApplication.restoreOverrideCursor()
        except:
            QApplication.restoreOverrideCursor()

        QMessageBox.information(self.iface.mainWindow(), self.tr("Success!"), self.tr("Images Successfully processed."))

    @pyqtSlot(bool)
    def on_srsButton_clicked(self):
        projSelector = QgsGenericProjectionSelector()
        message = 'Select the Spatial Reference System!'
        projSelector.setMessage(theMessage=message)
        if not projSelector.exec_():
            QMessageBox.warning(self, self.tr("Warning!"), self.tr(message))
            return
        else:
            self.epsg = int(projSelector.selectedAuthId().split(':')[-1])
        srs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
        self.srLineEdit.setText(srs.description())

    @pyqtSlot(bool)
    def on_addButton_clicked(self):
        fileNames = QFileDialog.getOpenFileNames(self, self.tr("Select Images"), "", self.tr("Image files (*.tif)"))
        self.fileListWidget.addItems(fileNames)

    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        selectedItems = self.fileListWidget.selectedItems()
        for item in selectedItems:
            row = self.fileListWidget.row(item)
            self.fileListWidget.takeItem(row)

    @pyqtSlot(bool)
    def on_addFolderButton_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        for dirName, subdirList, fileList in os.walk(folder):
            for fileName in fileList:
                if fileName.split(".")[-1] == 'tif':
                    self.fileListWidget.addItem(os.path.join(dirName,fileName))

    @pyqtSlot(bool)
    def on_outputFolderButton_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.outputFolderEdit.setText(folder)

    def getStretchingPercentage(self):
        index = self.stretchComboBox.currentIndex()
        if index == 0:
            return 0
        elif index == 1:
            return 2

    def getGDALRasterType(self):
        index = self.numberComboBox.currentIndex()
        if index == 0:
            min = numpy.iinfo(numpy.uint8).min
            max = numpy.iinfo(numpy.uint8).max
            return (osgeo.gdal.GDT_Byte, min, max)
        elif index == 1:
            min = numpy.iinfo(numpy.uint16).min
            max = numpy.iinfo(numpy.uint16).max
            return (osgeo.gdal.GDT_UInt16, min, max)
        elif index == 2:
            min = numpy.iinfo(numpy.int16).min
            max = numpy.iinfo(numpy.int16).max
            return (osgeo.gdal.GDT_Int16, min, max)
        elif index == 3:
            min = numpy.iinfo(numpy.uint32).min
            max = numpy.iinfo(numpy.uint32).max
            return (osgeo.gdal.GDT_UInt32, min, max)
        elif index == 4:
            min = numpy.iinfo(numpy.int32).min
            max = numpy.iinfo(numpy.int32).max
            return (osgeo.gdal.GDT_Int32, min, max)
        elif index == 5:
            min = numpy.finfo(numpy.float32).min
            max = numpy.finfo(numpy.float32).max
            return (osgeo.gdal.GDT_Float32, min, max)
        elif index == 6:
            min = numpy.finfo(numpy.float64).min
            max = numpy.finfo(numpy.float64).max
            return (osgeo.gdal.GDT_Float64, min, max)

    #Aplica realce de contraste, reprojecao e troca o tipo de numero utilizando a GDAL.
    def stretchImage(self, inFile, outDir, percent, epsg, bands = []):
        """Method that applies a specific histogram stretching to a group of images.
            The method also performs a conversion changing the raster type.
        """

        #Getting the output raster type
        (rasterType, minOutValue, maxOutValue) = self.getGDALRasterType()

        #Open image
        imgIn = osgeo.gdal.Open(inFile)
        if not imgIn:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Critical!"), self.tr("Failed to open input file."))
            return

        #Setting the output file name
        fileName = inFile.split("/")[-1]
        split = fileName.split(".")
        baseName = split[0]
        extension = '.' + split[-1]

        #Defining the output driver
        outDriver = imgIn.GetDriver()
        createOptions = ['PHOTOMETRIC=RGB', 'ALPHA=NO']

        #creating temp file for contrast stretch
        outFileTmp = os.path.join(outDir, baseName+'_tmp'+extension)
        #creating output file for contrast stretch
        outFile = os.path.join(outDir, baseName+'_stretch'+extension)

        #if bands is empty, make a new file with the same band size
        if bands == []:
            bands = range(0, imgIn.RasterCount)

        #Creating a temp image, with the same input parameters, to store the converted input image to 8 bits
        imgOut = outDriver.Create(outFileTmp,imgIn.RasterXSize, imgIn.RasterYSize, len(bands), rasterType, options = createOptions)
        imgOut.SetProjection(imgIn.GetProjection())
        imgOut.SetGeoTransform(imgIn.GetGeoTransform())

        #Linear stretching
        topPercent = 100.-percent/2.
        bottomPercent = percent/2.
        outBandNumber = 1
        for bandNumber in bands:

            b1 = imgIn.GetRasterBand(bandNumber+1)
            matrix = b1.ReadAsArray()
            arr = numpy.array(matrix)

            minValue, maxValue = numpy.percentile(matrix, [bottomPercent, topPercent])
            print minValue, maxValue

            #Transformation parameters
            #Rouding the values out of bounds
            numpy.putmask(arr, arr>maxValue,maxValue)
            numpy.putmask(arr, arr<minValue,minValue)

            #The maxOutValue and the minOutValue must be set according to the convertion that will be applied (e.g. 8 bits, 16 bits, 32 bits)
            a = (maxOutValue-minOutValue)/(maxValue-minValue)
            newArr = numpy.floor((arr-minValue)*a+minOutValue)

            outB = imgOut.GetRasterBand(outBandNumber)
            outBandNumber += 1
            outB.WriteArray(newArr)
            outB.FlushCache()

            QgsMessageLog.logMessage(self.tr("Band "+ str(bandNumber)+ ": "+str(minValue)+" , "+str(maxValue)),"DSG Tools Plugin", QgsMessageLog.INFO)

        #creating final image for reprojection
        outRasterSRS = osgeo.osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(epsg)

        #this code uses virtual raster to compute the parameters of the output image
        vrt = osgeo.gdal.AutoCreateWarpedVRT(imgOut, None, outRasterSRS.ExportToWkt(), osgeo.gdal.GRA_NearestNeighbour,  0.0)
        imgWGS = outDriver.CreateCopy(outFile, vrt, options = createOptions)

        #Checking if the output file was created with success
        if os.path.exists(outFile):
            QgsMessageLog.logMessage(self.tr("File successfully created: ") + outFile, "DSG Tools Plugin", QgsMessageLog.INFO)

        #Deleting the objects
        del imgWGS
        del imgOut
        del imgIn

        #Unlinking the temp file
        os.unlink(outFileTmp)
