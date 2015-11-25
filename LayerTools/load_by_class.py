# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LoadByClass
                                 A QGIS plugin
 Load database classes.
                             -------------------
        begin                : 2014-06-17
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
        mod history          : 2014-12-17 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
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

#Qgis imports
from qgis.core import QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry,QgsMessageLog
from qgis.gui import QgsMessageBar

#PyQt imports
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import Qt
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QApplication, QCursor

#DsgTools imports
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'load_by_class_base.ui'))

class LoadByClass(QtGui.QDialog, FORM_CLASS):
    def __init__(self, codeList, parent=None):
        """Constructor."""
        super(LoadByClass, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.selectedClasses = []

        self.bar = QgsMessageBar()
        self.setLayout(QtGui.QGridLayout(self))
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.bar.setSizePolicy(sizePolicy)
        self.layout().addWidget(self.bar, 0,0,1,1)

        #Objects Connections
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("connectionChanged()")), self.listClassesFromDatabase)
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("problemOccurred()")), self.pushMessage)
        
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(("clicked()")), self.cancel)
        QtCore.QObject.connect(self.selectAllCheck, QtCore.SIGNAL(("stateChanged(int)")), self.selectAll)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL(("clicked()")), self.okSelected)
        
        self.widget.tabWidget.currentChanged.connect(self.restoreInitialState)
        
        self.codeList = codeList
        self.layerFactory = LayerFactory()

    def restoreInitialState(self):
        self.selectedClasses = []

        tam = self.classesListWidget.__len__()
        for i in range(tam+1,1,-1):
            item = self.classesListWidget.takeItem(i-2)

        self.selectAllCheck.setCheckState(0)

    def listClassesFromDatabase(self):
        self.classes = []
        self.classesListWidget.clear()
        self.dbVersion = self.widget.getDBVersion()
        self.qmlPath = self.widget.getQmlPath()
        self.classes = self.widget.abstractDb.listGeomClassesFromDatabase()
        self.classesListWidget.addItems(self.classes)
        self.classesListWidget.sortItems()

    def on_filterEdit_textChanged(self, text):
        classes = [edgvClass for edgvClass in self.classes if text in edgvClass]
        self.classesListWidget.clear()
        self.classesListWidget.addItems(classes)
        self.classesListWidget.sortItems()

    def cancel(self):
        self.restoreInitialState()
        self.close()
        
    def pushMessage(self, msg):
        self.bar.pushMessage("", self.tr("Coordinate Reference System not set or invalid!"), level=QgsMessageBar.WARNING)

    def selectAll(self):
        if self.selectAllCheck.isChecked():
            tam = self.classesListWidget.__len__()
            for i in range(tam+1):
                item = self.classesListWidget.item(i-1)
                self.classesListWidget.setItemSelected(item,2)

        else:
            tam = self.classesListWidget.__len__()
            for i in range(tam+1):
                item = self.classesListWidget.item(i-1)
                self.classesListWidget.setItemSelected(item,0)

    def getSelectedItems(self):
        lista = self.classesListWidget.selectedItems()
        self.selectedClasses = []
        tam = len(lista)
        for i in range(tam):
            self.selectedClasses.append(lista[i].text())
        self.selectedClasses.sort()

    def okSelected(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.loadLayers()
        QApplication.restoreOverrideCursor()

    def loadLayers(self):
        self.getSelectedItems()
        if len(self.selectedClasses)>0:
            try:
                for layer in self.selectedClasses:
                    edgvLayer = self.layerFactory.makeLayer(self.widget.abstractDb, self.codeList, layer)
                    edgvLayer.load(self.widget.crs)
                self.restoreInitialState()
                self.close()
            except:
                self.bar.pushMessage(self.tr("Error!"), self.tr("Could not load the selected classes!"), level=QgsMessageBar.CRITICAL)
        else:
            self.bar.pushMessage(self.tr("Warning!"), self.tr("Please, select at least one class!"), level=QgsMessageBar.WARNING)