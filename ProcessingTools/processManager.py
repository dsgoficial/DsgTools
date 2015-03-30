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

from DsgTools.Factories.ThreadFactory.threadFactory import ThreadFactory

class ProcessManager(QObject):
    def __init__(self, iface):
        super(ProcessManager, self).__init__()
        
        self.iface = iface
        self.processDict = dict()
        self.messageBarDict = dict()

        self.threadFactory = ThreadFactory()

    def findProgressMessageBar(self, uuid):
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
        (progressMessageBar, progressBar) = self.findProgressMessageBar(uuid)
        
        if progressMessageBar:
            progressBar.setRange(0, maximum)

    @pyqtSlot(str)
    def stepProcessed(self, uuid):
        (progressMessageBar, progressBar) = self.findProgressMessageBar(uuid)
        if progressMessageBar:
            progressBar.setValue(progressBar.value() + 1)

    @pyqtSlot(int,str,str)
    def processFinished( self, feedback, message, uuid):
        (progressMessageBar, progressBar) = self.findProgressMessageBar(uuid)

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
        self.processDict[process] = (progressMessageBar, progressBar)
        self.messageBarDict[progressMessageBar] = progressBar

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
