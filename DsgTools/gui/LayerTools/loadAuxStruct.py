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
        email                : borba.philipe@eb.mil.br
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
from qgis.PyQt import QtWidgets, QtCore, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtGui import QCursor
import qgis as qgis

#DsgTools imports
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import LayerLoaderFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'loadAuxStruct.ui'))

class LoadAuxStruct(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
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

    @pyqtSlot(bool)
    def on_pushButtonCancel_clicked(self):
        """
        Closes the dialog
        """
        self.close()
        
    def pushMessage(self, msg):
        """
        Pushes a message into message bar
        """
        self.bar.pushMessage("", msg, level=QgsMessageBar.CRITICAL)

    @pyqtSlot(bool)
    def on_pushButtonOk_clicked(self):
        """
        Checks the linee-centroid structure and loads the correspondent layers 
        """
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if self.widgetConv.settingDict == dict():
            QApplication.restoreOverrideCursor()
            self.bar.pushMessage(self.tr("Error!"), self.tr("Could not load auxiliary classes! Check log for details!"), level=QgsMessageBar.CRITICAL)
        else:
            self.loadLayers()
        QApplication.restoreOverrideCursor()
        self.close()

    def loadLayers(self):
        """
        Loads the layers defined in the line-centroid structure
        """
        try:
            if self.widget.abstractDb.getDatabaseVersion() == 'Non_EDGV':
                isEdgv = False
            else:
                isEdgv = True
            auxClassesDict = self.widgetConv.settingDict['earthCoverageDict']
            auxClasses = []
            for key in list(auxClassesDict.keys()):
                for cl in auxClassesDict[key]:
                    if cl not in auxClasses:
                        if '.' in cl:
                            classToLoad = cl.split('.')[-1]
                        else:
                            classToLoad = cl
                        auxClasses.append(classToLoad)
            auxCentroids = self.widgetConv.abstractDb.getEarthCoverageCentroids()
            auxClasses = auxClasses + auxCentroids
            auxClasses.sort(reverse=True)
            auxClasses = [self.widgetConv.settingDict['frameLayer'].split('.')[-1]]+auxClasses
            factory = self.layerFactory.makeLoader(self.iface, self.widget.abstractDb, loadCentroids=True)
            factory.load(auxClasses, uniqueLoad = True, isEdgv = isEdgv)
        except Exception as e:
                QgsMessageLog.logMessage(':'.join(e.args), "DSGTools Plugin", Qgis.Critical)
                self.bar.pushMessage(self.tr("Error!"), self.tr("Could not load auxiliary classes! Check log for details!"), level=QgsMessageBar.CRITICAL)
                