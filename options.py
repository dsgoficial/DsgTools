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
import os
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings, pyqtSignal
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

from DsgTools.UserTools.profile_editor import ProfileEditor
from DsgTools.ServerTools.createView import CreateView
from DsgTools.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.ServerTools.selectStyles import SelectStyles

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'options.ui'))

class Options(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
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
        valueList = [self.blackListWidget.itemAt(i,0).text() for i in range(self.blackListWidget.count())]
        return (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, valueList)

    def loadParametersFromConfig(self):
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        freeHandTolerance = settings.value('freeHandTolerance')
        freeHandSmoothIterations = settings.value('freeHandSmoothIterations')
        freeHandSmoothOffset = settings.value('freeHandSmoothOffset')
        algIterations = settings.value('algIterations')
        valueList = settings.value('valueList')
        if valueList:
            valueList = valueList.split(';')
        settings.endGroup()
        return (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, valueList)
    
    def setInterfaceWithParametersFromConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, valueList) = self.loadParametersFromConfig()
        
        if freeHandTolerance != '' and freeHandTolerance:
            self.toleranceQgsDoubleSpinBox.setValue(float(freeHandTolerance))
        if freeHandSmoothIterations != '' and freeHandSmoothIterations:
            self.smoothIterationsQgsSpinBox.setValue(int(freeHandSmoothIterations))
        if freeHandSmoothOffset != '' and freeHandSmoothOffset:
            self.smoothOffsetQgsDoubleSpinBox.setValue(float(freeHandSmoothOffset))
        if algIterations != '' and algIterations:
            self.algIterationsQgsSpinBox.setValue(int(algIterations))
        if valueList != '' and valueList:
            self.blackListWidget.clear()
            self.blackListWidget.addItems(valueList)
            self.blackListWidget.sortItems(order = Qt.AscendingOrder)
    
    def storeParametersInConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, valueList) = self.getParameters()
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        settings.setValue('freeHandTolerance', freeHandTolerance)
        settings.setValue('freeHandSmoothIterations', freeHandSmoothIterations)
        settings.setValue('freeHandSmoothOffset', freeHandSmoothOffset)
        settings.setValue('algIterations', algIterations)
        settings.setValue('valueList', ';'.join(valueList))
        settings.endGroup()
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.storeParametersInConfig()
        self.close()
    
    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        selectedItems = self.blackListWidget.selectedItems()
        for item in selectedItems:
            self.blackListWidget.removeItemWidget(item)
    
    def firstTimeConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, valueList) = self.loadParametersFromConfig()
        if not (freeHandTolerance and freeHandSmoothIterations and freeHandSmoothOffset and algIterations and valueList):
            self.storeParametersInConfig()
        
        