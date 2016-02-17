# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-23
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# QGIS imports
from qgis.core import QgsMapLayer, QgsField, QgsDataSourceURI
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

import qgis as qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validation_toolbox.ui'))

#DsgTools imports
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory

class ValidationToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, codeList):
        """Constructor."""
        super(ValidationToolbox, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.layerFactory = LayerFactory()
        self.iface = iface
        self.codeList = codeList
        self.widget.tabWidget.setTabEnabled(1,True)
        self.widget.tabWidget.setTabEnabled(0,False)
        self.widget.tabWidget.setCurrentIndex(1)
        self.widget.connectionChanged.connect(self.listProcesses)
        self.processList = ['identifyInvalidGeom']
    
    @pyqtSlot()
    def listProcesses(self):
        print 'lalala'
        pass
    
    def runProcess(self):
        pass
    
    @pyqtSlot(bool)
    def on_openFlagsButton_clicked(self):
        self.loadFlags()
    
    def loadFlags(self):
        try:
            self.widget.abstractDb.checkAndCreateValidationStructure()
        except Exception as e:
            raise e
        dbName = self.widget.abstractDb.getDatabaseName()
        groupList =  self.iface.legendInterface().groups()
        edgvLayer = self.layerFactory.makeLayer(self.widget.abstractDb, self.codeList, 'public.aux_flags_validacao_p')
        if dbName in groupList:
            edgvLayer.load(self.widget.crs,groupList.index(dbName))
        else:
            self.parentTreeNode = qgis.utils.iface.legendInterface().addGroup(self.widget.abstractDb.getDatabaseName(), -1)
            edgvLayer.load(self.widget.crs,self.parentTreeNode)
    
    def identifyInvalidGeom(self):
        if self.widget.abstractDb.checkInvalidGeom() > 0:
            self.loadFlags()
            