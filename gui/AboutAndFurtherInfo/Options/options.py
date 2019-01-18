# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from os.path import expanduser

# Qt imports
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QMessageBox, QDialog

# DSGTools imports

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'options.ui'))

class Options(QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(Options, self).__init__(parent)
        self.setupUi(self)
        self.setInterfaceWithParametersFromConfig()
    
    @pyqtSlot(bool)
    def on_addPushButton_clicked(self):
        newValue = self.addParameterLineEdit.text()
        valueList = [self.blackListWidget.itemAt(i,0).text() for i in range(self.blackListWidget.count())]
        if newValue == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill in a value before adding!'))
            return
        if newValue in valueList:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Value already in black list!'))
            return
        self.blackListWidget.addItem(newValue)
        self.blackListWidget.sortItems(order = Qt.AscendingOrder)
        self.addParameterLineEdit.setText('')
    
    def getParameters(self):
        freeHandTolerance = self.toleranceQgsDoubleSpinBox.value()
        freeHandSmoothIterations = self.smoothIterationsQgsSpinBox.value()
        freeHandSmoothOffset = self.smoothOffsetQgsDoubleSpinBox.value()
        algIterations = self.algIterationsQgsSpinBox.value()
        minSegmentDistance = self.minSegmentDistanceQgsSpinBox.value()
        valueList = [self.blackListWidget.item(i).text() for i in range(self.blackListWidget.count())]
        undoPoints = self.undoQgsSpinBox.value()
        decimals = self.decimalQgsSpinBox.value()
        return (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals)

    def loadParametersFromConfig(self):
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        freeHandTolerance = settings.value('freeHandTolerance')
        freeHandSmoothIterations = settings.value('freeHandSmoothIterations')
        freeHandSmoothOffset = settings.value('freeHandSmoothOffset')
        algIterations = settings.value('algIterations')
        minSegmentDistance = settings.value('minSegmentDistance')
        valueList = settings.value('valueList')
        undoPoints = settings.value('undoPoints')
        decimals = settings.value('decimals')
        if valueList:
            valueList = valueList.split(';')
        settings.endGroup()
        return (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals)
    
    def setInterfaceWithParametersFromConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals) = self.loadParametersFromConfig()
        if freeHandTolerance:
            self.toleranceQgsDoubleSpinBox.setValue(float(freeHandTolerance))
        if freeHandSmoothIterations:
            self.smoothIterationsQgsSpinBox.setValue(int(freeHandSmoothIterations))
        if freeHandSmoothOffset:
            self.smoothOffsetQgsDoubleSpinBox.setValue(float(freeHandSmoothOffset))
        if algIterations:
            self.algIterationsQgsSpinBox.setValue(int(algIterations))
        if minSegmentDistance:
            self.minSegmentDistanceQgsSpinBox.setValue(int(minSegmentDistance))
        if valueList:
            self.blackListWidget.clear()
            self.blackListWidget.addItems(valueList)
            self.blackListWidget.sortItems(order = Qt.AscendingOrder)
        if undoPoints:
            self.undoQgsSpinBox.setValue(int(undoPoints))
    
    def storeParametersInConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals) = self.getParameters()
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        settings.setValue('freeHandTolerance', freeHandTolerance)
        settings.setValue('freeHandSmoothIterations', freeHandSmoothIterations)
        settings.setValue('freeHandSmoothOffset', freeHandSmoothOffset)
        settings.setValue('algIterations', algIterations)
        settings.setValue('minSegmentDistance', minSegmentDistance)
        settings.setValue('valueList', ';'.join(valueList))
        settings.setValue('undoPoints', undoPoints)
        settings.setValue('decimals', decimals)
        settings.endGroup()
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.storeParametersInConfig()
        self.close()
    
    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        selectedItems = self.blackListWidget.selectedItems()
        idxList = []
        for i in range(self.blackListWidget.count()):
            if self.blackListWidget.item(i) in selectedItems:
                idxList.append(i)
        idxList.sort(reverse=True)
        for i in idxList:
            self.blackListWidget.takeItem(i)
    
    def firstTimeConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals) = self.loadParametersFromConfig()
        if not (freeHandTolerance and freeHandSmoothIterations and freeHandSmoothOffset and algIterations and valueList and undoPoints and decimals is not None):
            self.storeParametersInConfig()
