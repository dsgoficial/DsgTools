# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LoadAuxStruct
                                 A QGIS plugin
 Load line centroid aux structure.
                             -------------------
        begin                : 2016-04-28
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
        mod history          : 
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
import os, json

#Qgis imports
from qgis.gui import QgsMessageBar
from qgis.core import QgsMessageLog

#PyQt imports
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QApplication, QCursor
import qgis as qgis

#DsgTools imports
from DsgTools.Factories.LayerLoaderFactory.edgvLayerLoader import EDGVLayerLoader

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'loadAuxStruct.ui'))

class LoadAuxStruct(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        self.layerFactory = LayerLoaderFactory()
        self.selectedClasses = []
        self.widget.tabWidget.setTabEnabled(0,True)
        self.widget.tabWidget.setTabEnabled(1,False)
        self.widget.tabWidget.setCurrentIndex(0)
        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("problemOccurred()")), self.pushMessage)
        self.widget.dbChanged.connect(self.widgetConv.setDatabase)

        
        self.codeList = codeList
        self.layerFactory = LayerFactory()

    @pyqtSlot(bool)
    def on_pushButtonCancel_clicked(self):
        '''
        Closes the dialog
        '''
        self.close()
        
    def pushMessage(self, msg):
        '''
        Pushes a message into message bar
        '''
        self.bar.pushMessage("", msg, level=QgsMessageBar.CRITICAL)

    @pyqtSlot(bool)
    def on_pushButtonOk_clicked(self):
        '''
        Checks the linee-centroid structure and loads the correspondent layers 
        '''
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        auxCreated = self.widget.abstractDb.checkCentroidAuxStruct()
        if not auxCreated:
            QApplication.restoreOverrideCursor()
            self.bar.pushMessage(self.tr("Error!"), self.tr("Could not load auxiliary classes! Check log for details!"), level=QgsMessageBar.CRITICAL)
                
        else:
            self.loadLayers()
        QApplication.restoreOverrideCursor()
        self.close()

    def loadLayers(self):
        '''
        Loads the layers defined in the line-centroid structure
        '''
        try:
            auxClassesDict = json.loads(self.widget.abstractDb.getEarthCoverageClasses()[0])
            auxClasses = []
            for key in auxClassesDict.keys():
                for cl in auxClassesDict[key]:
                    if cl not in auxClasses:
                        auxClasses.append(cl)
            auxCentroids = self.widget.abstractDb.getEarthCoverageCentroids()
            auxClasses = auxClasses + auxCentroids
            auxClasses.sort(reverse=True)
            auxClasses = ['aux_moldura_a']+auxClasses
            factory = self.layerFactory.makeLoader(self.iface, auxClasses)
            
        except Exception as e:
                QgsMessageLog.logMessage(str(e.args[0]), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                self.bar.pushMessage(self.tr("Error!"), self.tr("Could not load auxiliary classes! Check log for details!"), level=QgsMessageBar.CRITICAL)
                