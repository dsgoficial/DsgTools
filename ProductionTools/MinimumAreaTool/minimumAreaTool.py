# -*- coding: utf-8 -*-
"""
/***************************************************************************
MinimumAreaTool
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
                                            Felipe Diniz - Cartographic Engineer @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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
import resources 
from PyQt4.QtCore import QSettings, pyqtSignal, pyqtSlot, SIGNAL, QObject
import qgis.utils
from DsgTools.ProductionTools.MinimumAreaTool.shapeTool import ShapeTool
from PyQt4.QtGui import QSplitter, QPushButton, QComboBox, QIcon, QMessageBox
from PyQt4.Qt import QWidget, QObject

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'minimumAreaTool.ui'))

class MinimumAreaTool(QWidget,FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(MinimumAreaTool, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.valuees={}
        self.scale = None
        self.shape = None
        self.size = None
        self.createDict()
    
    def initGui(self):
        self.iface.addToolBarWidget(self.splitter)
        
    def createDict(self):
        self.sizes = {}
        self.sizes[u"25mm²"] = {self.tr('value'): 25, self.tr('type'): self.tr('area')}
        self.sizes[u"4mm²"] = {self.tr('value'): 4, self.tr('type'): self.tr('area')}
        self.sizes[u"1x1mm²"] = {self.tr('value'): 1, self.tr('type'): self.tr('area')}
        self.sizes[u"0.8x0.8mm²"] = {self.tr('value'): 0.64, self.tr('type'): self.tr('area')}
        self.sizes[u"0.8mm"] = {self.tr('value'): 0.8,self.tr('type'): self.tr('distance')}
    
    @pyqtSlot(int)
    def on_scalesComboBox_currentIndexChanged(self):
        if self.scalesComboBox.currentIndex() <> 0:
            self.scale = self.scalesComboBox.currentText()
    
    @pyqtSlot(int)
    def on_sizesComboBox_currentIndexChanged(self):
        if self.sizesComboBox.currentIndex() <> 0:
            self.size = self.sizesComboBox.currentText()
            if self.sizesComboBox.currentText() == '0.8mm':
                self.shapesComboBox.setCurrentIndex(2)
                self.shapesComboBox.setEnabled(False)
            else:
                self.shapesComboBox.setEnabled(True)
    
    @pyqtSlot(int)
    def on_shapesComboBox_currentIndexChanged(self):
        if self.shapesComboBox.currentIndex() <> 0:
            self.shape = self.shapesComboBox.currentText()
            if self.sizesComboBox.currentText() == '0.8mm':
                self.shapesComboBox.setCurrentIndex(2)
                self.shapesComboBox.setEnabled(False)
            else:
                self.shapesComboBox.setEnabled(True)
    
    @pyqtSlot(bool)
    def on_drawShape_clicked(self):
        if self.scale and self.size and self.shape:
            self.run()
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr(u"Error!"), self.tr(u"<font color=red>Shape value not defined :</font><br><font color=blue>Define all values to activate tool!</font>"), QMessageBox.Close)    
    
    def unload(self):
        try:
            self.iface.mapCanvas().unsetMapTool(self.tool)

        except:
            pass           
    
    def run(self):
        if (self.sizes[self.size][self.tr('type')] == self.tr('area')):
            param = (float(self.scale)**2)*float(self.sizes[self.size][self.tr('value')])
        else:
            param = float(self.scale)*float(self.sizes[self.size][self.tr('value')])
        self.tool = ShapeTool(self.iface.mapCanvas(), self.shape, param, self.sizes[self.size][self.tr('type')] )
        self.tool.toolFinished.connect(self.refreshCombo)
        self.tool.setCursor(self.tool)        
        self.iface.mapCanvas().setMapTool(self.tool)            

    def refreshCombo(self):
        self.shapesComboBox.setEnabled(True)

