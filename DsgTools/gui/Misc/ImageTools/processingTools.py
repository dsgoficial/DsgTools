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
from builtins import str
from builtins import range
import os
import osgeo.gdal
import osgeo.osr
import numpy

# Import the PyQt and QGIS libraries
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog
from qgis.PyQt.QtCore import pyqtSlot

from qgis.core import QgsCoordinateReferenceSystem, QgsMessageLog
from qgis.gui import QgsProjectionSelectionTreeWidget

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ui_processingTools.ui")
)


class ProcessingTools(QtWidgets.QDialog, FORM_CLASS):
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

        self.tabWidget.removeTab(1)

        self.epsg = 4326
        srs = QgsCoordinateReferenceSystem(
            self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId
        )
        self.srLineEdit.setText(srs.description())

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Starts to process the selected images
        """
        if self.fileListWidget.count() == 0:
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr("Warning!"),
                self.tr("Please select at least one image."),
            )
            return

        if self.outputFolderEdit.text() == "":
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr("Warning!"),
                self.tr("Please select at the output folder."),
            )
            return

        QMessageBox.information(
            self.iface.mainWindow(),
            self.tr("Information!"),
            self.tr(
                "The processing may take several minutes. Please wait the final message."
            ),
        )

        self.filesList = []
        for itemNumber in range(0, self.fileListWidget.count()):
            inFile = self.fileListWidget.item(itemNumber).text()
            self.filesList.append(str(inFile))

    def getParameters(self):
        """
        Gets the process parameters
        """
        (rasterType, minOutValue, maxOutValue) = self.getGDALRasterType()
        return (
            self.filesList,
            rasterType,
            minOutValue,
            maxOutValue,
            str(self.outputFolderEdit.text()),
            self.getStretchingPercentage(),
            self.epsg,
        )

    @pyqtSlot(bool)
    def on_srsButton_clicked(self):
        """
        Opens the dialog to select CRS
        """
        projSelector = QgsProjectionSelectionTreeWidget()
        message = self.tr("Select the Spatial Reference System!")
        projSelector.setMessage(theMessage=message)
        if not projSelector.exec_():
            QMessageBox.warning(self, self.tr("Warning!"), message)
            return
        else:
            self.epsg = int(projSelector.selectedAuthId().split(":")[-1])
        srs = QgsCoordinateReferenceSystem(
            self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId
        )
        self.srLineEdit.setText(srs.description())

    @pyqtSlot(bool)
    def on_addButton_clicked(self):
        """
        Adds image files to be processed
        """
        fileNames, __ = QFileDialog.getOpenFileNames(
            self, self.tr("Select Images"), "", self.tr("Image files (*.tif)")
        )
        self.fileListWidget.addItems(fileNames)

    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        """
        Remove files from processing list
        """
        selectedItems = self.fileListWidget.selectedItems()
        for item in selectedItems:
            row = self.fileListWidget.row(item)
            self.fileListWidget.takeItem(row)

    @pyqtSlot(bool)
    def on_addFolderButton_clicked(self):
        """
        Adds a folder to be processed
        """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Select Directory"))
        for dirName, subdirList, fileList in os.walk(folder):
            for fileName in fileList:
                if fileName.split(".")[-1] == "tif":
                    self.fileListWidget.addItem(os.path.join(dirName, fileName))

    @pyqtSlot(bool)
    def on_outputFolderButton_clicked(self):
        """
        Defines the output folder
        """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Select Directory"))
        self.outputFolderEdit.setText(folder)

    def getStretchingPercentage(self):
        """
        Gets the histogram stretching percentage
        """
        index = self.stretchComboBox.currentIndex()
        if index == 0:
            return 0
        elif index == 1:
            return 2

    def getGDALRasterType(self):
        """
        Gets the output raster type
        """
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
