# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-05-15
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
from builtins import range
import os
import time
import csv
import shutil
from osgeo import gdal, ogr

from qgis.PyQt.Qt import QObject, QVariant
from qgis.PyQt.QtCore import pyqtSlot

# Import the PyQt and QGIS libraries
from qgis.core import (
    QgsMessageLog,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsGeometry,
    QgsField,
    QgsPointXY,
    QgsProcessingMultiStepFeedback,
    QgsFeature,
    QgsProject,
    QgsFields,
)

from .genericThread import GenericThread


class InventoryMessages(QObject):
    def __init__(self, thread):
        """
        Inventory messages constructor
        :param thread:
        """
        super(InventoryMessages, self).__init__()

        self.thread = thread

    def getInventoryErrorMessage(self):
        """
        Returns generic error message
        """
        return self.tr("An error occurred while searching for files.")

    def getCopyErrorMessage(self):
        """
        Returns copy error message
        """
        return self.tr("An error occurred while copying the files.")

    def getSuccessInventoryMessage(self):
        """
        Returns success message
        """
        return self.tr("Inventory successfully created!")

    def getSuccessInventoryAndCopyMessage(self):
        """
        Returns successful copy message
        """
        return self.tr("Inventory and copy performed successfully!")

    def getUserCanceledFeedbackMessage(self):
        """
        Returns user canceled message
        """
        return self.tr("User canceled inventory processing!")

    @pyqtSlot()
    def progressCanceled(self):
        self.thread.stopped[0] = True


class InventoryThread(GenericThread):
    def __init__(self):
        """
        Constructor.
        """
        super(InventoryThread, self).__init__()

        self.messenger = InventoryMessages(self)
        self.files = list()
        gdal.DontUseExceptions()
        ogr.DontUseExceptions()
        self.layer_attributes = [
            QgsField("filename", QVariant.String),
            QgsField("date", QVariant.String),
            QgsField("size", QVariant.String),
            QgsField("extension", QVariant.String),
        ]
        self.qgsattr = QgsFields()
        for i in self.layer_attributes:
            self.qgsattr.append(i)

    def setParameters(
        self,
        parentFolder,
        outputFile,
        makeCopy,
        destinationFolder,
        formatsList,
        isWhitelist,
        isOnlyGeo,
        stopped,
    ):
        self.parentFolder = parentFolder
        self.outputFile = outputFile
        self.makeCopy = makeCopy
        self.destinationFolder = destinationFolder
        self.formatsList = formatsList
        self.stopped = stopped
        self.isWhitelist = isWhitelist
        self.isOnlyGeo = isOnlyGeo

    def run(self):
        """
        Runs the thread
        """
        # Actual process
        (ret, msg) = self.makeInventory(
            self.parentFolder, self.outputFile, self.destinationFolder
        )

        if ret == 1:
            self.signals.loadFile.emit(self.outputFile, self.isOnlyGeo)

        self.signals.processingFinished.emit(ret, msg, self.getId())

    def get_format_set(self, format_list):
        if "shp" in format_list:
            return set(format_list + ["prj"])
        else:
            return set(format_list)

    def make_inventory_from_processing(
        self,
        parent_folder,
        format_list,
        destination_folder=None,
        make_copy=False,
        onlyGeo=True,
        feedback=None,
    ):
        featList = []
        fileList = []
        format_set = self.get_format_set(format_list)
        tuple_list = [i for i in os.walk(parent_folder)]
        nSteps = len(tuple_list) if make_copy else len(tuple_list) - 1
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback) if feedback else None
        )
        for current_step, [root, dirs, files] in enumerate(tuple_list):
            if feedback is not None:
                if feedback.isCanceled():
                    return []
                multiStepFeedback.setCurrentStep(current_step)
            n_files = len(files)
            files_progress = 100 / n_files if n_files else 0
            for current, current_file in enumerate(files):
                if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                    break
                extension = current_file.split(".")[-1]
                if extension not in format_set:
                    continue
                full_path = self.get_full_path(current_file, root)
                if gdal.Open(full_path) or ogr.Open(full_path):
                    bbox_geom, attributes = self.computeBoxAndAttributes(
                        None, full_path, extension, insertIntoMemory=False
                    )
                    new_feat = self.get_new_feat(bbox_geom, attributes)
                    featList.append(new_feat)
                    fileList.append(full_path)
                if multiStepFeedback is not None:
                    multiStepFeedback.setProgress(files_progress * current)
        if make_copy:
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(nSteps)
            copy_len = len(fileList)
            for current, file_ in fileList:
                if multiStepFeedback is not None and multiStepFeedback.isCanceled:
                    break
                try:
                    self.copy_single_file(file_, destination_folder)
                    if multiStepFeedback is not None:
                        multiStepFeedback.pushInfo(
                            self.tr("File {file} copied to {destination}").format(
                                file=file_, destination=destination_folder
                            )
                        )
                except Exception as e:
                    if multiStepFeedback is not None:
                        multiStepFeedback.pushInfo(
                            self.tr("Error copying file {file}: {exception}\n").format(
                                file=file_, exception="\n".join(e.args)
                            )
                        )
        return featList

    def get_full_path(self, file_name, root):
        line = os.path.join(root, file_name)
        line = line.encode(encoding="UTF-8")
        return line

    def get_new_feat(self, geom, attributes):
        new_feat = QgsFeature(self.qgsattr)
        new_feat.setAttributes(attributes)
        new_feat.setGeometry(geom)
        return new_feat

    def makeInventory(self, parentFolder, outputFile, destinationFolder):
        """
        Makes the inventory
        """
        # creating a csv file
        try:
            csvfile = open(outputFile, "wb")
        except IOError as e:
            QgsMessageLog.logMessage(
                self.messenger.getInventoryErrorMessage() + "\n" + e.strerror,
                "DSGTools Plugin",
                QgsMessageLog.INFO,
            )
            return (0, self.messenger.getInventoryErrorMessage() + "\n" + e.strerror)

        try:
            outwriter = csv.writer(csvfile)
            # defining the first row
            outwriter.writerow(["fileName", "date", "size (KB)", "extension"])
            # creating the memory layer used in only geo mode
            layer = self.createMemoryLayer()
            # iterating over the parent folder recursively
            for root, dirs, files in os.walk(parentFolder):
                # Progress bar steps calculated
                self.signals.rangeCalculated.emit(len(files), self.getId())
                for file in files:
                    # check if the user stopped the operation
                    if not self.stopped[0]:
                        extension = file.split(".")[-1]
                        # check if the file should be skipped
                        if not self.inventoryFile(extension):
                            continue
                        # making the full path
                        line = os.path.join(root, file)
                        line = line.encode(encoding="UTF-8")
                        # changing the separator, it will be changed later
                        line = line.replace(os.sep, "/")
                        # forcing the inventory of .prj files
                        if extension == "prj":
                            self.writeLine(outwriter, line, extension)
                        else:
                            # check if GDAL/OGR recognizes the file
                            gdalSrc = gdal.Open(line)
                            ogrSrc = ogr.Open(line)
                            if gdalSrc or ogrSrc:
                                # if only geo mode
                                if self.isOnlyGeo:
                                    self.computeBoxAndAttributes(layer, line, extension)
                                else:
                                    self.writeLine(outwriter, line, extension)
                                self.files.append(line)
                            gdalSrc = None
                            ogrSrc = None

                        self.signals.stepProcessed.emit(self.getId())
                    else:
                        QgsMessageLog.logMessage(
                            self.messenger.getUserCanceledFeedbackMessage(),
                            "DSGTools Plugin",
                            QgsMessageLog.INFO,
                        )
                        return (-1, self.messenger.getUserCanceledFeedbackMessage())
        except csv.Error as e:
            csvfile.close()
            QgsMessageLog.logMessage(
                self.messenger.getInventoryErrorMessage() + "\n" + e,
                "DSGTools Plugin",
                QgsMessageLog.INFO,
            )
            return (0, self.messenger.getInventoryErrorMessage() + "\n" + e)
        except OSError as e:
            csvfile.close()
            QgsMessageLog.logMessage(
                self.messenger.getInventoryErrorMessage() + "\n" + e.strerror,
                "DSGTools Plugin",
                QgsMessageLog.INFO,
            )
            return (0, self.messenger.getInventoryErrorMessage() + "\n" + e.strerror)
        except Exception as e:
            csvfile.close()
            QgsMessageLog.logMessage(
                self.messenger.getInventoryErrorMessage() + "\n" + ":".join(e.args),
                "DSGTools Plugin",
                QgsMessageLog.INFO,
            )
            return (0, self.messenger.getInventoryErrorMessage())
        csvfile.close()

        if self.isOnlyGeo:
            error = QgsVectorFileWriter.writeAsVectorFormat(
                layer, self.outputFile, "utf-8", None, "ESRI Shapefile"
            )

        if self.makeCopy:
            # return self.copyFiles(destinationFolder)
            return self.copy(destinationFolder)
        else:
            QgsMessageLog.logMessage(
                self.messenger.getSuccessInventoryMessage(),
                "DSGTools Plugin",
                QgsMessageLog.INFO,
            )
            return (1, self.messenger.getSuccessInventoryMessage())

    def computeBoxAndAttributes(self, layer, line, extension, insertIntoMemory=True):
        """
        Computes bounding box and inventory attributes
        """
        # get the bounding box and wkt projection
        (ogrPoly, prjWkt) = self.getExtent(line)
        if ogrPoly == None or prjWkt == None:
            return
        # making a QGIS projection
        crsSrc = QgsCoordinateReferenceSystem()
        crsSrc.createFromWkt(prjWkt)
        # reprojecting the bounding box
        qgsPolygon = self.reprojectBoundingBox(crsSrc, ogrPoly)
        # making the attributes
        attributes = self.makeAttributes(line, extension)
        # inserting into memory layer
        if not insertIntoMemory:
            return qgsPolygon, attributes
        self.insertIntoMemoryLayer(layer, qgsPolygon, attributes)

    def copyFiles(self, destinationFolder):
        """
        Copy inventoried files to the destination folder
        """
        for fileName in self.files:
            if not self.stopped[0]:
                # adjusting the separators according to the OS
                fileName = fileName.replace("/", os.sep)
                file = fileName.split(os.sep)[-1]
                newFileName = os.path.join(destinationFolder, file)
                newFileName = newFileName.replace("/", os.sep)

                # making tha actual copy
                try:
                    shutil.copy2(fileName, newFileName)
                except IOError as e:
                    QgsMessageLog.logMessage(
                        self.messenger.getCopyErrorMessage() + "\n" + e.strerror,
                        "DSGTools Plugin",
                        QgsMessageLog.INFO,
                    )
                    return (0, self.messenger.getCopyErrorMessage() + "\n" + e.strerror)
            else:
                QgsMessageLog.logMessage(
                    self.messenger.getUserCanceledFeedbackMessage(),
                    "DSGTools Plugin",
                    QgsMessageLog.INFO,
                )
                return (-1, self.messenger.getUserCanceledFeedbackMessage())

        QgsMessageLog.logMessage(
            self.messenger.getSuccessInventoryAndCopyMessage(),
            "DSGTools Plugin",
            QgsMessageLog.INFO,
        )
        return (1, self.messenger.getSuccessInventoryAndCopyMessage())

    def copy(self, destinationFolder):
        """
        Copy inventoried files considering the dataset
        destinationFolder: copy destination folder
        """
        for fileName in self.files:
            # adjusting the separators according to the OS
            fileName = fileName.replace("/", os.sep)
            file = fileName.split(os.sep)[-1]
            newFileName = os.path.join(destinationFolder, file)
            newFileName = newFileName.replace("/", os.sep)

            try:
                gdalSrc = gdal.Open(fileName)
                ogrSrc = ogr.Open(fileName)
                if ogrSrc:
                    self.copyOGRDataSource(ogrSrc, newFileName)
                elif gdalSrc:
                    self.copyGDALDataSource(gdalSrc, newFileName)
            except Exception as e:
                QgsMessageLog.logMessage(
                    self.messenger.getCopyErrorMessage() + "\n" + ":".join(e.args),
                    "DSGTools Plugin",
                    QgsMessageLog.INFO,
                )
                return (
                    0,
                    self.messenger.getCopyErrorMessage() + "\n" + ":".join(e.args),
                )

        QgsMessageLog.logMessage(
            self.messenger.getSuccessInventoryAndCopyMessage(),
            "DSGTools Plugin",
            QgsMessageLog.INFO,
        )
        return (1, self.messenger.getSuccessInventoryAndCopyMessage())

    def copy_single_file(self, file_name, destination_folder):
        file_name = file_name.replace("/", os.sep)
        file_ = file_name.split(os.sep)[-1]
        newFileName = os.path.join(destination_folder, file_)
        newFileName = newFileName.replace("/", os.sep)
        gdalSrc = gdal.Open(fileName)
        ogrSrc = ogr.Open(fileName)
        if ogrSrc:
            self.copyOGRDataSource(ogrSrc, newFileName)
        elif gdalSrc:
            self.copyGDALDataSource(gdalSrc, newFileName)

    def copyGDALDataSource(self, gdalSrc, newFileName):
        """
        Copies a GDAL datasource
        gdalSrc: original gdal source
        newFileName: new file name
        """
        driver = gdalSrc.GetDriver()
        dst_ds = driver.CreateCopy(newFileName, gdalSrc)
        ogrSrc = None
        dst_ds = None

    def copyOGRDataSource(self, ogrSrc, newFileName):
        """
        Copies a OGR datasource
        ogrSrc: original ogr source
        newFileName: new file name
        """
        driver = ogrSrc.GetDriver()
        dst_ds = driver.CopyDataSource(ogrSrc, newFileName)
        ogrSrc = None
        dst_ds = None

    def isInFormatsList(self, ext):
        """
        Check if the extension is in the formats list
        ext: file extension
        """
        if ext in self.formatsList:
            return True
        return False

    def inventoryFile(self, ext):
        """
        Check is the extension should be analyzed
        ext: file extension
        """
        if self.isWhitelist:
            return self.isInFormatsList(ext)
        else:
            return not self.isInFormatsList(ext)

    def writeLine(self, outwriter, line, extension):
        """
        Write CSV line
        outwriter: csv file
        line: csv line
        extension: file extension
        """
        row = self.makeAttributes(line, extension)
        outwriter.writerow(row)

    def makeAttributes(self, line, extension):
        """
        Make the attributes array
        line: csv line
        extension: file extension
        """
        creationDate = time.ctime(os.path.getctime(line))
        size = os.path.getsize(line) / 1000.0

        return [line.decode(encoding="UTF-8"), creationDate, size, extension]

    def getRasterExtent(self, gt, cols, rows):
        """
        Return list of corner coordinates from a geotransform
            @param gt: geotransform
            @param cols: number of columns in the dataset
            @param rows: number of rows in the dataset
            @return:   coordinates of each corner
        """
        ext = []
        xarr = [0, cols]
        yarr = [0, rows]

        for px in xarr:
            for py in yarr:
                x = gt[0] + (px * gt[1]) + (py * gt[2])
                y = gt[3] + (px * gt[4]) + (py * gt[5])
                ext.append([x, y])
            yarr.reverse()
        return ext

    def getExtent(self, filename):
        """
        Makes a ogr polygon to represent the extent (i.e. bounding box)
        filename: file name
        """
        gdalSrc = gdal.Open(filename)
        ogrSrc = ogr.Open(filename)
        if ogrSrc:
            poly = ogr.Geometry(ogr.wkbPolygon)
            spatialRef = None
            for id in range(ogrSrc.GetLayerCount()):
                layer = ogrSrc.GetLayer(id)
                extent = layer.GetExtent()
                spatialRef = layer.GetSpatialRef()

                # Create a Polygon from the extent tuple
                ring = ogr.Geometry(ogr.wkbLinearRing)
                ring.AddPoint(extent[0], extent[2])
                ring.AddPoint(extent[0], extent[3])
                ring.AddPoint(extent[1], extent[3])
                ring.AddPoint(extent[1], extent[2])
                ring.AddPoint(extent[0], extent[2])
                box = ogr.Geometry(ogr.wkbPolygon)
                box.AddGeometry(ring)

                poly = poly.Union(box)

            ogrSrc = None
            if not spatialRef:
                return (None, None)
            return (poly, spatialRef.ExportToWkt())
        elif gdalSrc:
            gdalSrc.GetProjectionRef()
            gt = gdalSrc.GetGeoTransform()
            cols = gdalSrc.RasterXSize
            rows = gdalSrc.RasterYSize
            ext = self.getRasterExtent(gt, cols, rows)

            ring = ogr.Geometry(ogr.wkbLinearRing)
            for pt in ext:
                ring.AddPoint(pt[0], pt[1])
            ring.AddPoint(ext[0][0], ext[0][1])

            box = ogr.Geometry(ogr.wkbPolygon)
            box.AddGeometry(ring)

            prjWkt = gdalSrc.GetProjectionRef()
            gdalSrc = None
            return (box, prjWkt)
        else:
            return (None, None)

    def createMemoryLayer(self):
        """
        Creates a memory layer
        """
        layer = QgsVectorLayer("Polygon?crs=4326", "Inventory", "memory")
        if not layer.isValid():
            return None
        provider = layer.dataProvider()
        provider.addAttributes(self.layer_attributes)
        layer.updateFields()
        return layer

    def reprojectBoundingBox(self, crsSrc, ogrPoly):
        """
        Reprojects the bounding box
        crsSrc:source crs
        ogrPoly: ogr polygon
        """
        crsDest = QgsCoordinateReferenceSystem(4326)
        coordinateTransformer = QgsCoordinateTransform(
            crsSrc, crsDest, QgsProject.instance()
        )

        newPolyline = []
        ring = ogrPoly.GetGeometryRef(0)
        for i in range(ring.GetPointCount()):
            pt = ring.GetPoint(i)
            point = QgsPointXY(pt[0], pt[1])
            newPolyline.append(point)
        qgsPolygon = QgsGeometry.fromPolygonXY([newPolyline])
        qgsPolygon.transform(coordinateTransformer)
        return qgsPolygon

    def insertIntoMemoryLayer(self, layer, poly, attributes):
        """
        Inserts the poly into memory layer
        layer: QgsVectorLayer
        poly: QgsGeometry
        attributes: Attributes list
        """
        provider = layer.dataProvider()

        # Creating the feature
        feature = QgsFeature()
        feature.setGeometry(poly)
        feature.setAttributes(attributes)

        # Adding the feature into the file
        provider.addFeatures([feature])
