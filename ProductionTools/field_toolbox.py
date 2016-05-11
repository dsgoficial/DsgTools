# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2016-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Brazilian Army - Geographic Service Bureau
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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import pyqtSlot, pyqtSignal

# QGIS imports
from qgis.core import QgsMapLayer, QgsGeometry, QgsMapLayerRegistry

#DsgTools imports
from DsgTools.ProductionTools.field_setup import FieldSetup
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_toolbox.ui'))

class FieldToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
    
    @pyqtSlot(bool)
    def on_setupButton_clicked(self):
        dlg = FieldSetup()
        dlg.exec_()
        
        reclassificationDict = dlg.makeReclassificationDict()
        self.createButtons(reclassificationDict)
        
    def createButtons(self, reclassificationDict):
        formLayout = QtGui.QFormLayout()
        
        for edgvClass in reclassificationDict.keys():
            for button in reclassificationDict[edgvClass].keys():
                pushButton = QtGui.QPushButton(button)
                formLayout.addRow(pushButton)
        
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QtGui.QFrame.Shape(0))  # no frame
        w = QtGui.QWidget()
        w.setLayout(formLayout)
        scrollArea.setWidget(w)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(scrollArea)
        
        self.tabWidget.widget(0).setLayout(layout)