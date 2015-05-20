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
import csv
import shutil
from osgeo import gdal, ogr

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsMessageLog
from qgis._core import QgsAction

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
        
    def setParameters(self, parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, stopped):
        self.parentFolder = parentFolder
        self.outputFile = outputFile
        self.makeCopy = makeCopy
        self.destinationFolder = destinationFolder
        self.formatsList = formatsList
        self.stopped = stopped
        self.isWhitelist = isWhitelist
    
    def run(self):
        # Actual process
        (ret, msg) = self.makeInventory(self.parentFolder, self.outputFile, self.destinationFolder)
        
        if ret == 1:
            self.signals.loadFile.emit(self.outputFile)
        
        # Doing that to stop progress bar
        self.signals.rangeCalculated.emit(10, self.getId())
        self.signals.processingFinished.emit(ret, msg, self.getId())
    
    def makeInventory(self, parentFolder, outputFile, destinationFolder):
        # Progress bar steps calculated
        self.signals.rangeCalculated.emit(0, self.getId())

        try:
            csvfile = open(outputFile, 'wb')
        except IOError, e:
            QgsMessageLog.logMessage(self.messenger.getInventoryErrorMessage()+'\n'+e.strerror, "DSG Tools Plugin", QgsMessageLog.INFO)
            return (0, self.messenger.getInventoryErrorMessage()+'\n'+e.strerror)

        try:
            outwriter = csv.writer(csvfile)
            outwriter.writerow(['fileName'])
            for root, dirs, files in os.walk(parentFolder):
                for file in files:
                    if not self.stopped[0]:
                        extension = file.split('.')[-1]
                        if not self.inventoryFile(extension):
                            continue
                        line = os.path.join(root,file)
                        line = line.decode(encoding='UTF-8')
                        if extension == 'prj':
                            outwriter.writerow([line])
                            self.files.append(line)
                        else:
                            gdalSrc = gdal.Open(line)
                            ogrSrc = ogr.Open(line)
                            if gdalSrc or ogrSrc:
                                outwriter.writerow([line])
                                self.files.append(line)
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
        
        if self.makeCopy:
            return self.copyFiles(destinationFolder)
        else:
            QgsMessageLog.logMessage(self.messenger.getSuccessInventoryMessage(), "DSG Tools Plugin", QgsMessageLog.INFO)
            return (1, self.messenger.getSuccessInventoryMessage())
        
    def copyFiles(self, destinationFolder):
        for fileName in self.files:
            if not self.stopped[0]:
                file = fileName.split(os.sep)[-1]
                newFileName = os.path.join(destinationFolder, file)

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
        
    def isInFormatsList(self, ext):
        if ext in self.formatsList:
                return True         
        return False
    
    def inventoryFile(self, ext):
        if self.isWhitelist:
            return self.isInFormatsList(ext)
        else:
            return not self.isInFormatsList(ext)
    