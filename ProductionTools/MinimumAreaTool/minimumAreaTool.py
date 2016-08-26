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
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QSettings, pyqtSignal, pyqtSlot, SIGNAL, QObject
from PyQt4.Qt import QWidget, QObject

#qgis imports
import qgis.utils
from qgis.gui import QgsMessageBar
#DsgTools Imports
from DsgTools.ProductionTools.MinimumAreaTool.shapeTool import ShapeTool

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'minimumAreaTool.ui'))

class MinimumAreaTool(QWidget,FORM_CLASS):
    def __init__(self, iface, parent = None):
        """
        Constructor
        """
        super(MinimumAreaTool, self).__init__(parent)
        self.setupUi(self)
        self.splitter.hide()
        self.iface = iface
        self.scale = None
        self.shape = None
        self.size = None
        self.createDict()
    
    def initGui(self):
        '''
        Adds the tool bar in QGIS
        '''
        self.iface.addToolBarWidget(self.splitter)
        
    def createDict(self):
        '''
        Creates the dictionary used to create the geometry templates
        '''
        self.sizes = {}
        self.sizes[u"25mm²"] = {self.tr('value'): 25, self.tr('type'): self.tr('area')}
        self.sizes[u"4mm²"] = {self.tr('value'): 4, self.tr('type'): self.tr('area')}
        self.sizes[u"1x1mm²"] = {self.tr('value'): 1, self.tr('type'): self.tr('area')}
        self.sizes[u"0.8x0.8mm²"] = {self.tr('value'): 0.64, self.tr('type'): self.tr('area')}
        self.sizes[u"0.8mm"] = {self.tr('value'): 0.8,self.tr('type'): self.tr('distance')}
        
    def shapeComboSetter(self):
        '''
        Sets the correct index for the shapes combo box according to the text select in the sizes combo box
        '''
        if self.sizesComboBox.currentText() == '0.8mm':
            self.shapesComboBox.setCurrentIndex(2)
            self.shapesComboBox.setEnabled(False)
        else:
            self.shapesComboBox.setEnabled(True)
    
    @pyqtSlot(int)
    def on_sizesComboBox_currentIndexChanged(self):
        '''
        Slot used to check if the user selected 0.8mm (this is used for linear features).
        In this case we should force the use of circle and set the shape combo box enabled(False)
        '''
        if self.sizesComboBox.currentIndex() <> 0:
            self.shapeComboSetter()
    
    @pyqtSlot(int)
    def on_shapesComboBox_currentIndexChanged(self):
        '''
        Slot used to check if the user selected 0.8mm (this is used for linear features).
        In this case we should force the use of circle and set the shape combo box enabled(False)
        '''
        if self.shapesComboBox.currentIndex() <> 0:
            self.shapeComboSetter()
    
    @pyqtSlot(bool)
    def on_drawShape_clicked(self):
        '''
        Draws the select template shape on the map canvas
        '''
        scale = self.scalesComboBox.currentText()
        size = self.sizesComboBox.currentText()
        shape = self.shapesComboBox.currentText()
        validated = self.validateCombos(self.scalesComboBox.currentIndex(), self.sizesComboBox.currentIndex(), self.shapesComboBox.currentIndex())
        if validated:
            crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
            if crs.mapUnits() == 2:
                self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('This tool does not work with angular unit reference system!'), level=QgsMessageBar.WARNING, duration=3)
            else:
                self.run(scale, size, shape)
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr(u"Error!"), self.tr(u"<font color=red>Shape value not defined :</font><br><font color=blue>Define all values to activate tool!</font>"), QMessageBox.Close)              
    
    def run(self, scale, size, shape):
        '''
        Runs the ShapeTool and set it as the current map tool
        '''
        #checking the selected type
        if (self.sizes[size][self.tr('type')] == self.tr('area')):
            param = (float(scale)**2)*float(self.sizes[size][self.tr('value')])
        else:
            param = float(scale)*float(self.sizes[size][self.tr('value')])
        tool = ShapeTool(self.iface.mapCanvas(), shape, param, self.sizes[size][self.tr('type')] )
        tool.toolFinished.connect(self.refreshCombo)
        self.iface.mapCanvas().setMapTool(tool)

    def refreshCombo(self):
        '''
        Re-enables the shapes combo
        '''
        self.shapesComboBox.setEnabled(True)
    
    def validateCombos(self,scale,size,shape):
        '''
        Checks if all combos correctly selected
        '''
        if scale <> 0 and size <> 0 and shape <> 0:
            return True
        else:
            return False

    @pyqtSlot(bool)
    def on_showPushButton_toggled(self, toggled):
        '''
        Slot to show/hide the tool bar
        '''
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()