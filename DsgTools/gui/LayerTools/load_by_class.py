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
        email                : borba.philipe@eb.mil.br
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
from builtins import range
import os

#Qgis imports
from qgis.gui import QgsMessageBar
from qgis.core import QgsMessageLog

#PyQt imports
from qgis.PyQt import QtWidgets, QtCore, uic
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtGui import QCursor
import qgis as qgis

#DsgTools imports
from DsgTools.core.Factories.LayerFactory.layerFactory import LayerFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'load_by_class_base.ui'))

class LoadByClass(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, codeList, parent=None):
        """
        Constructor
        """
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
        self.widget.styleChanged.connect(self.populateStyleCombo)
        self.codeList = codeList
        self.layerFactory = LayerFactory()

    def restoreInitialState(self):
        '''
        Restores the dialog initial state
        '''
        self.selectedClasses = []

        tam = self.classesListWidget.__len__()
        for i in range(tam+1,1,-1):
            item = self.classesListWidget.takeItem(i-2)

        self.selectAllCheck.setCheckState(0)

    def listClassesFromDatabase(self):
        '''
        List all classes from database
        '''
        self.classes = []
        self.classesListWidget.clear()
        self.dbVersion = self.widget.getDBVersion()
        self.qmlPath = self.widget.getQmlPath()
        self.parentClassList = self.widget.abstractDb.getOrphanGeomTablesWithElements(loading = True)

        self.classes = []
        try:
            self.classes = self.widget.abstractDb.listGeomClassesFromDatabase()
        except Exception as e:
            self.bar.pushMessage(self.tr("CRITICAL!"), self.tr('A problem occurred! Check log for details.'), level=QgsMessageBar.CRITICAL)
            QgsMessageLog.logMessage(':'.join(e.args), 'DSGTools Plugin', Qgis.Critical)

        if self.onlyParentsCheckBox.isChecked() and not self.widget.isSpatialite:
            self.classesListWidget.addItems(self.parentClassList)
        else:
            self.classesListWidget.addItems(self.classes)
        self.classesListWidget.sortItems()

    def on_filterEdit_textChanged(self, text):
        '''
        Filters shown classes
        text: text used to filter classes
        '''
        classes = [edgvClass for edgvClass in self.classes if text in edgvClass]
        self.classesListWidget.clear()
        self.classesListWidget.addItems(classes)
        self.classesListWidget.sortItems()

    def cancel(self):
        '''
        Cancels the process
        '''
        self.restoreInitialState()
        self.close()
        
    def pushMessage(self, msg):
        '''
        Pushes a message into message bar
        '''
        self.bar.pushMessage("", msg, level=QgsMessageBar.CRITICAL)

    def selectAll(self):
        '''
        Select all classes to be loaded
        '''
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
        '''
        Gets the selected classes
        '''
        lista = self.classesListWidget.selectedItems()
        self.selectedClasses = []
        tam = len(lista)
        for i in range(tam):
            self.selectedClasses.append(lista[i].text())
        self.selectedClasses.sort()

    def okSelected(self):
        '''
        Loads the selected layers
        '''
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.loadLayers()
        QApplication.restoreOverrideCursor()

    def loadLayers(self):
        '''
        Actual method that load layers
        '''
        self.getSelectedItems()
        if len(self.selectedClasses)>0:
            try:
                selectedStyle = None
                if self.styleDict:
                    if self.styleComboBox.currentText() in list(self.styleDict.keys()):
                        selectedStyle = self.styleDict[self.styleComboBox.currentText()] 
                for layer in self.selectedClasses:
                    dbName = self.widget.abstractDb.getDatabaseName()
                    groupList =  qgis.utils.iface.legendInterface().groups()
                    edgvLayer = self.layerFactory.makeLayer(self.widget.abstractDb, self.codeList, layer)
                    if dbName in groupList:
                        edgvLayer.load(self.widget.crs, groupList.index(dbName), stylePath = selectedStyle)
                    else:
                        self.parentTreeNode = qgis.utils.iface.legendInterface().addGroup(self.widget.abstractDb.getDatabaseName(), -1)
                        edgvLayer.load(self.widget.crs, self.parentTreeNode, stylePath = selectedStyle)
                self.restoreInitialState()
                self.close()
            except:
                self.bar.pushMessage(self.tr("Error!"), self.tr("Could not load the selected classes!"), level=QgsMessageBar.CRITICAL)
        else:
            self.bar.pushMessage(self.tr("Warning!"), self.tr("Please, select at least one class!"), level=QgsMessageBar.WARNING)

    def populateStyleCombo(self, styleDict):
        self.styleComboBox.clear()
        self.styleDict = styleDict
        styleList = list(styleDict.keys())
        numberOfStyles = len(styleList)
        if numberOfStyles > 0:
            self.styleComboBox.addItem(self.tr('Select Style'))
            for i in range(numberOfStyles):
                self.styleComboBox.addItem(styleList[i])
        else:
            self.syleComboBox.addItem(self.tr('No available styles'))
    
    @pyqtSlot(int)
    def on_onlyParentsCheckBox_stateChanged(self):
        self.listClassesFromDatabase()