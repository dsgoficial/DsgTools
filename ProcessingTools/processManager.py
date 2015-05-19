# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-03-29
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis._core import QgsAction

import sip

from DsgTools.Factories.ThreadFactory.threadFactory import ThreadFactory

class ProcessManager(QObject):
    def __init__(self, iface):
        super(ProcessManager, self).__init__()

        self.iface = iface
        self.processDict = dict()

        self.threadFactory = ThreadFactory()

    def findProgressBar(self, uuid):
        for key in self.processDict.keys():
            id = key.getId()
            if id == uuid:
                return self.processDict[key]
        return None

    def findProcess(self, uuid):
        for key in self.processDict.keys():
            id = key.getId()
            if id == uuid:
                return key
        return None

    @pyqtSlot(int, str)
    def setProgressRange(self, maximum, uuid):
        progressBar = self.findProgressBar(uuid)
        if not sip.isdeleted(progressBar):
            progressBar.setRange(0, maximum)

    @pyqtSlot(str)
    def stepProcessed(self, uuid):
        progressBar = self.findProgressBar(uuid)
        if not sip.isdeleted(progressBar):
            progressBar.setValue(progressBar.value() + 1)

    @pyqtSlot(int,str,str)
    def processFinished( self, feedback, message, uuid):
        progressBar = self.findProgressBar(uuid)

        process = self.findProcess(uuid)
        if process != None:
            process.stopped[0] = True
            self.processDict.pop(process, None)
            process = None

        if feedback == 1:
            progressBar.setValue(progressBar.maximum())
        QMessageBox.information(self.iface.mainWindow(), 'DSG Tools', message)

    def prepareProcess(self, process, message):
        # Setting the progress bar
        progressMessageBar = self.iface.messageBar().createMessage(message)
        progressBar = QProgressBar()
        progressBar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progressBar)
        self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)

        #connecting the destroyed signal
        progressMessageBar.destroyed.connect(process.messenger.progressCanceled)

        #storing the process and its related progressBar
        self.processDict[process] = progressBar

        #initiating processing
        QThreadPool.globalInstance().start(process)

    def createPostgisDatabaseProcess(self, db, version,epsg):
        #creating process
        process = self.threadFactory.makeProcess('pgdb')
        stopped = [False]
        process.setParameters(db,version,epsg,stopped)

        #connecting signal/slots
        process.signals.rangeCalculated.connect(self.setProgressRange)
        process.signals.stepProcessed.connect(self.stepProcessed)
        process.signals.processingFinished.connect(self.processFinished)

        #preparing the progressBar that will be created
        self.prepareProcess(process, self.tr("Creating database structure..."))

    def createDpiProcess(self, filesList, rasterType, minOutValue, maxOutValue, outDir, percent, epsg):
        #creating process
        process = self.threadFactory.makeProcess('dpi')
        stopped = [False]
        process.setParameters(filesList, rasterType, minOutValue, maxOutValue, outDir, percent, epsg, stopped)

        #connecting signal/slots
        process.signals.rangeCalculated.connect(self.setProgressRange)
        process.signals.stepProcessed.connect(self.stepProcessed)
        process.signals.processingFinished.connect(self.processFinished)

        #preparing the progressBar that will be created
        self.prepareProcess(process, self.tr("Processing images..."))

    def createInventoryProcess(self, parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist):
        #creating process
        process = self.threadFactory.makeProcess('inventory')
        stopped = [False]
        process.setParameters(parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, stopped)

        #connecting signal/slots
        process.signals.rangeCalculated.connect(self.setProgressRange)
        process.signals.stepProcessed.connect(self.stepProcessed)
        process.signals.processingFinished.connect(self.processFinished)
        process.signals.loadFile.connect(self.loadInventoryFile)

        #preparing the progressBar that will be created
        self.prepareProcess(process, self.tr("Making inventory, please wait..."))

    @pyqtSlot(str)
    def loadInventoryFile(self, outputFile):
        # Adding the layer and making it active
        layer = self.iface.addVectorLayer('file://'+outputFile+'?delimiter=%s' % ',', 'Inventory', 'delimitedtext')
        self.iface.setActiveLayer(layer)            
        # Creating and Attribute Action to load the inventoried file
        actions = layer.actions()
        field = '[% "fileName" %]'
        actions.addAction(QgsAction.GenericPython, 'Load Vector Layer', 'qgis.utils.iface.addVectorLayer(\'%s\', \'File\', \'ogr\')' % field)
        actions.addAction(QgsAction.GenericPython, 'Load Raster Layer', 'qgis.utils.iface.addRasterLayer(\'%s\', \'File\')' % field)            
