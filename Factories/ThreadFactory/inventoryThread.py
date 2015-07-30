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
import os
import time
import csv
import shutil
from osgeo import gdal, ogr

# Import the PyQt and QGIS libraries
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsMessageLog
from qgis._core import QgsAction, QgsPoint

from DsgTools.Factories.ThreadFactory.genericThread import GenericThread
from exceptions import OSError

class InventoryMessages(QObject):
    def __init__(self, thread):
        super(InventoryMessages, self).__init__()

        self.thread = thread
        
    def getInventoryErrorMessage(self):
        return self.tr('An error occurred while searching for files.')
    
    def getCopyErrorMessage(self):
        return self.tr('An error occurred while copying the files.')
    
    def getSuccessInventoryMessage(self):
        return self.tr('Inventory successfully created!')
    
    def getSuccessInventoryAndCopyMessage(self):
        return self.tr('Inventory and copy performed successfully!')

    def getUserCanceledFeedbackMessage(self):
        return self.tr('User canceled inventory processing!')
    
    @pyqtSlot()
    def progressCanceled(self):
        self.thread.stopped[0] = True    

class InventoryThread(GenericThread):
    def __init__(self):
        """Constructor.
        """
        super(InventoryThread, self).__init__()

        self.messenger = InventoryMessages(self)
        self.files = list()
        
    def setParameters(self, parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, isOnlyGeo, stopped):
        self.parentFolder = parentFolder
        self.outputFile = outputFile
        self.makeCopy = makeCopy
        self.destinationFolder = destinationFolder
        self.formatsList = formatsList
        self.stopped = stopped
        self.isWhitelist = isWhitelist
        self.isOnlyGeo = isOnlyGeo
    
    def run(self):
        # Actual process
        (ret, msg) = self.makeInventory(self.parentFolder, self.outputFile, self.destinationFolder)
        
        if ret == 1:
            self.signals.loadFile.emit(self.outputFile)
        
        # Doing that to stop progress bar
        self.signals.rangeCalculated.emit(10, self.getId())
        self.signals.processingFinished.emit(ret, msg, self.getId())
    
    def makeInventory(self, parentFolder, outputFile, destinationFolder):
        '''Makes the inventory
        '''
        # Progress bar steps calculated
        self.signals.rangeCalculated.emit(0, self.getId())

        # creating a csv file
        try:
            csvfile = open(outputFile, 'wb')
        except IOError, e:
            QgsMessageLog.logMessage(self.messenger.getInventoryErrorMessage()+'\n'+e.strerror, "DSG Tools Plugin", QgsMessageLog.INFO)
            return (0, self.messenger.getInventoryErrorMessage()+'\n'+e.strerror)

        try:
            outwriter = csv.writer(csvfile)
            # defining the first row
            outwriter.writerow(['fileName', 'date', 'size (KB)', 'extension'])
            # creating the memory layer used in only geo mode
            layer = self.createMemoryLayer()
            # iterating over the parent folder recursively
            for root, dirs, files in os.walk(parentFolder):
                for file in files:
                    # check if the user stopped the operation
                    if not self.stopped[0]:
                        extension = file.split('.')[-1]
                        # check if the file should be skipped
                        if not self.inventoryFile(extension):
                            continue
                        # making the full path
                        line = os.path.join(root,file)
                        line = line.encode(encoding='UTF-8')
                        # changing the separator, it will be changed later
                        line = line.replace(os.sep, '/')
                        # forcing the inventory of .prj files
                        if extension == 'prj':
                            self.writeLine(outwriter, line, extension)
                        else:
                            # check if GDAL/OGR recognizes the file
                            gdalSrc = gdal.Open(line)
                            ogrSrc = ogr.Open(line)
                            if gdalSrc or ogrSrc:
                                #if only geo mode
                                if self.isOnlyGeo:
                                    # get the bounding box and wkt projection
                                    (ogrPoly, prjWkt) = self.getExtent(line)
                                    # making a QGIS projection
                                    crsSrc = QgsCoordinateReferenceSystem()
                                    crsSrc.createFromWkt(prjWkt)
                                    # reprojecting the bounding box
                                    qgsPolygon = self.reprojectBoundingBox(crsSrc, ogrPoly)
                                    # making the attributes
                                    attributes = self.makeAttributes(line, extension)
                                    # inserting into memory layer
                                    self.insertIntoMemoryLayer(layer, qgsPolygon, attributes)
                                else:
                                    self.writeLine(outwriter, line, extension)
                            gdalSrc = None
                            ogrSrc = None
                    else:
                        QgsMessageLog.logMessage(self.messenger.getUserCanceledFeedbackMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
                        return (-1, self.messenger.getUserCanceledFeedbackMessage())
        except csv.Error, e:
            csvfile.close()
            QgsMessageLog.logMessage(self.messenger.getInventoryErrorMessage()+'\n'+str(e), "DSG Tools Plugin", QgsMessageLog.INFO)
            return (0, self.messenger.getInventoryErrorMessage()+'\n'+str(e))
        except OSError, e:
            csvfile.close()
            QgsMessageLog.logMessage(self.messenger.getInventoryErrorMessage()+'\n'+e.strerror, "DSG Tools Plugin", QgsMessageLog.INFO)
            return (0, self.messenger.getInventoryErrorMessage()+'\n'+e.strerror)
        except:
            csvfile.close()
            QgsMessageLog.logMessage(self.messenger.getInventoryErrorMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
            return (0, self.messenger.getInventoryErrorMessage())
        csvfile.close()
        
        if self.isOnlyGeo:
            error = QgsVectorFileWriter.writeAsVectorFormat(layer, self.outputFile, "utf-8", None, "ESRI Shapefile")
        
        if self.makeCopy:
            # return self.copyFiles(destinationFolder)
            return self.copy(destinationFolder)
        else:
            QgsMessageLog.logMessage(self.messenger.getSuccessInventoryMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
            return (1, self.messenger.getSuccessInventoryMessage())
        
    def copyFiles(self, destinationFolder):
        '''Copy inventoried files to the destination folder
        '''
        for fileName in self.files:
            if not self.stopped[0]:
                # adjusting the separators according to the OS
                fileName = fileName.replace('/', os.sep)
                file = fileName.split(os.sep)[-1]
                newFileName = os.path.join(destinationFolder, file)
                newFileName = newFileName.replace('/', os.sep)

                # making tha actual copy
                try:
                    shutil.copy2(fileName, newFileName)
                except IOError, e:
                    QgsMessageLog.logMessage(self.messenger.getCopyErrorMessage()+'\n'+e.strerror, "DSG Tools Plugin", QgsMessageLog.INFO)
                    return (0, self.messenger.getCopyErrorMessage()+'\n'+e.strerror)
            else:
                QgsMessageLog.logMessage(self.messenger.getUserCanceledFeedbackMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
                return (-1, self.messenger.getUserCanceledFeedbackMessage())

        QgsMessageLog.logMessage(self.messenger.getSuccessInventoryAndCopyMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
        return (1, self.messenger.getSuccessInventoryAndCopyMessage())

    def copy(self, destinationFolder):
        for fileName in self.files:
            # adjusting the separators according to the OS
            fileName = fileName.replace('/', os.sep)
            file = fileName.split(os.sep)[-1]
            newFileName = os.path.join(destinationFolder, file)
            newFileName = newFileName.replace('/', os.sep)

            gdalSrc = gdal.Open(filename)
            ogrSrc = ogr.Open(filename)
            if ogrSrc:
                driver = ogrSrc.GetDriver()
                dst_ds = driver.CreateCopy(newFileName, ogrSrc, 0)
                print 'foi'

                ogrSrc = None
                dst_ds = None
            elif gdalSrc:
                driver = gdalSrc.GetDriver()
                dst_ds = driver.CreateCopy(newFileName, gdalSrc, 0)

                ogrSrc = None
                dst_ds = None
            else:
                QgsMessageLog.logMessage(self.messenger.getCopyErrorMessage()+'\n'+e.strerror, "DSG Tools Plugin", QgsMessageLog.INFO)
                return (0, self.messenger.getCopyErrorMessage()+'\n'+e.strerror)

        QgsMessageLog.logMessage(self.messenger.getSuccessInventoryAndCopyMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
        return (1, self.messenger.getSuccessInventoryAndCopyMessage())

    def isInFormatsList(self, ext):
        '''Check if the extension is in the formats list
        '''
        if ext in self.formatsList:
                return True         
        return False
    
    def inventoryFile(self, ext):
        '''Check is the extension should be analyzed
        '''
        if self.isWhitelist:
            return self.isInFormatsList(ext)
        else:
            return not self.isInFormatsList(ext)
        
    def writeLine(self, outwriter, line, extension):
        '''Write CSV line
        '''
        row = self.makeAttributes(line, extension)
        outwriter.writerow(row)
        self.files.append(line)
        
    def makeAttributes(self, line, extension):
        '''Make the attributes array
        '''
        creationDate = time.ctime(os.path.getctime(line))
        size = os.path.getsize(line)/1000.
        
        return [line, creationDate, size, extension]
        
    def getRasterExtent(self, gt, cols, rows):
        ''' Return list of corner coordinates from a geotransform
            @param gt: geotransform
            @param cols: number of columns in the dataset
            @param rows: number of rows in the dataset
            @return:   coordinates of each corner
        '''
        ext=[]
        xarr=[0,cols]
        yarr=[0,rows]
    
        for px in xarr:
            for py in yarr:
                x=gt[0]+(px*gt[1])+(py*gt[2])
                y=gt[3]+(px*gt[4])+(py*gt[5])
                ext.append([x,y])
            yarr.reverse()
        return ext        

    def getExtent(self, filename):
        '''Makes a ogr polygon to represent the extent (i.e. bounding box)
        '''
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
                ring.AddPoint(extent[0],extent[2])
                ring.AddPoint(extent[0], extent[3])
                ring.AddPoint(extent[1], extent[3])
                ring.AddPoint(extent[1], extent[2])
                ring.AddPoint(extent[0],extent[2])
                box = ogr.Geometry(ogr.wkbPolygon)
                box.AddGeometry(ring)
                
                poly = poly.Union(box)
            
            ogrSrc = None
            return (poly, spatialRef.ExportToWkt())
        elif gdalSrc:
            gdalSrc.GetProjectionRef()
            gt = gdalSrc.GetGeoTransform()
            cols = gdalSrc.RasterXSize
            rows = gdalSrc.RasterYSize
            ext = self.getRasterExtent(gt, cols, rows)

            ring = ogr.Geometry(ogr.wkbLinearRing)
            for pt in ext:
                ring.AddPoint(pt[0],pt[1])
            ring.AddPoint(ext[0][0], ext[0][1])

            box = ogr.Geometry(ogr.wkbPolygon)
            box.AddGeometry(ring)
            
            prjWkt = gdalSrc.GetProjectionRef()
            gdalSrc = None
            return (box, prjWkt)
        else:
            return None
        
    def createMemoryLayer(self):
        layer = QgsVectorLayer('Polygon?crs=4326', 'Inventory', 'memory')
        if not layer.isValid():
            return None
        provider = layer.dataProvider()
        provider.addAttributes([QgsField('fileName', QVariant.String), QgsField('date', QVariant.String),
                                QgsField('size (KB)', QVariant.String), QgsField('extension)', QVariant.String)])
        layer.updateFields()
        return layer
    
    def reprojectBoundingBox(self, crsSrc, ogrPoly):
        crsDest = QgsCoordinateReferenceSystem(4326)
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest)
        
        newPolyline = []
        ring = ogrPoly.GetGeometryRef(0)
        for i in range(ring.GetPointCount()):
            pt = ring.GetPoint(i)
            point = QgsPoint(pt[0], pt[1])
            newPolyline.append(coordinateTransformer.transform(point))
        qgsPolygon = QgsGeometry.fromPolygon([newPolyline])
        return qgsPolygon
    
    def insertIntoMemoryLayer(self, layer, poly, attributes):
        """Inserts the poly into memory layer
        """
        provider = layer.dataProvider()

        #Creating the feature
        feature = QgsFeature()
        feature.setGeometry(poly)
        feature.setAttributes(attributes)

        # Adding the feature into the file
        provider.addFeatures([feature])
