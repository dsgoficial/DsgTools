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
from builtins import str
from qgis.PyQt.Qt import QObject
from qgis.PyQt.QtCore import QUrl, pyqtSlot
from qgis.PyQt.QtWidgets import QProgressBar
from qgis._core import QgsAction

import sip

from DsgTools.core.Factories.ThreadFactory.threadFactory import ThreadFactory

class ProcessManager(QObject):
    def __init__(self, iface):
        """
        Constructor
        """
        super(ProcessManager, self).__init__()

        self.iface = iface
        self.processDict = dict()

        self.threadFactory = ThreadFactory()

    def findProgressBar(self, uuid):
        """
        Gets a process progress bar by its uuid
        """
        for key in list(self.processDict.keys()):
            id = key.getId()
            if id == uuid:
                return self.processDict[key]
        return None

    def findProcess(self, uuid):
        """
        Finds a process by its uuid
        """
        for key in list(self.processDict.keys()):
            id = key.getId()
            if id == uuid:
                return key
        return None

    @pyqtSlot(int, str)
    def setProgressRange(self, maximum, uuid):
        """
        Sets the progress range for the process
        maximum: progress range
        uuid: process uuid
        """
        progressBar = self.findProgressBar(uuid)
        if not sip.isdeleted(progressBar):
            progressBar.setRange(0, maximum)

    @pyqtSlot(str)
    def stepProcessed(self, uuid):
        """
        Updates the process progress bar
        uuid: process uuid
        """
        progressBar = self.findProgressBar(uuid)
        if not sip.isdeleted(progressBar):
            progressBar.setValue(progressBar.value() + 1)

    @pyqtSlot(int,str,str)
    def processFinished( self, feedback, message, uuid):
        """
        Finalizes the process
        feedback: feedback code
        message: feedback message
        uuid: process uuid
        """
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
        """
        Prepares the process to be executed.
        Creates a message bar.
        Connects the destroyed progress bar signal to the process cancel method
        """
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

    def createPostgisDatabaseProcess(self, dbName, abstractDb, version, epsg):
        """
        Create the postgis databsae process
        """
        #creating process
        process = self.threadFactory.makeProcess('pgdb')
        stopped = [False]
        process.setParameters(abstractDb,dbName,version,epsg,stopped)
        #connecting signal/slots
        process.signals.rangeCalculated.connect(self.setProgressRange)
        process.signals.stepProcessed.connect(self.stepProcessed)
        process.signals.processingFinished.connect(self.processFinished)
        #preparing the progressBar that will be created
        self.prepareProcess(process, self.tr("Creating database structure..."))

    def createDpiProcess(self, filesList, rasterType, minOutValue, maxOutValue, outDir, percent, epsg):
        """
        Creates the digital image process
        """
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

    def createInventoryProcess(self, parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, isOnlyGeo):
        """
        Creates the inventory process
        """
        #creating process
        process = self.threadFactory.makeProcess('inventory')
        stopped = [False]
        process.setParameters(parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, isOnlyGeo, stopped)

        #connecting signal/slots
        process.signals.rangeCalculated.connect(self.setProgressRange)
        process.signals.stepProcessed.connect(self.stepProcessed)
        process.signals.processingFinished.connect(self.processFinished)
        process.signals.loadFile.connect(self.loadInventoryFile)

        #preparing the progressBar that will be created
        self.prepareProcess(process, self.tr("Making inventory, please wait..."))

    @pyqtSlot(str, bool)
    def loadInventoryFile(self, outputFile, isOnlyGeo):
        """
        Loads the inventory upon completion
        """
        if not isOnlyGeo:
            # Adding the layer and making it active
            url = QUrl.fromLocalFile(outputFile)
            url.addQueryItem('delimiter', ',')
            layer_uri = str(url.toEncoded())
            layer = self.iface.addVectorLayer(layer_uri, 'Inventory', 'delimitedtext')
        else:
            layer = self.iface.addVectorLayer(outputFile, 'Inventory', 'ogr')

        if layer:
            self.iface.setActiveLayer(layer)            
            # Creating and Attribute Action to load the inventoried file
            actions = layer.actions()
            field = '[% "fileName" %]'
            actions.addAction(QgsAction.GenericPython, 'Load Vector Layer', 'qgis.utils.iface.addVectorLayer(r\'%s\', \'File\', \'ogr\')' % field)
            actions.addAction(QgsAction.GenericPython, 'Load Raster Layer', 'qgis.utils.iface.addRasterLayer(r\'%s\', \'File\')' % field)            
