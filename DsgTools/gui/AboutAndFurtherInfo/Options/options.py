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
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.spellChecker.datasets.ptBR import PalavrasFileConfig, WordDatasetPtBRFileConfig
from DsgTools.core.NetworkTools.ExternalFilesHandler import ExternalFileDownloadProcessor

from processing.modeler.ModelerUtils import ModelerUtils
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, Qt, QSettings
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QFileDialog

from qgis.utils import iface

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'options.ui'))

class Options(QDialog, FORM_CLASS):
    __dsgToolsModelPath__ = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "core", "Misc", "QGIS_Models"
    ))
    __qgisModelPath__ = ModelerUtils.modelsFolders()[0]

    # # some options signals
    # modelPathChanged = pyqtSignal()

    def __init__(self, parent = None):
        """Constructor."""
        super(Options, self).__init__(parent)
        self.setupUi(self)
        self.setInterfaceWithParametersFromConfig()
        self.setupValidationToolbarConfig()
        # project option still not implemented
        self.removeModelsProjectCheckBox.hide()

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
        self.blackListWidget.sortItems(order=Qt.AscendingOrder)
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
        freeHandFinalSimplifyTolerance = self.finalToleranceQgsDoubleSpinBox.value()
        return (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals, freeHandFinalSimplifyTolerance)

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
        freeHandFinalSimplifyTolerance = settings.value('freeHandFinalSimplifyTolerance')
        if valueList:
            valueList = valueList.split(';')
        settings.endGroup()
        return (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals, freeHandFinalSimplifyTolerance)
    
    def setInterfaceWithParametersFromConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals, freeHandFinalSimplifyTolerance) = self.loadParametersFromConfig()
        if freeHandTolerance:
            self.toleranceQgsDoubleSpinBox.setValue(float(freeHandTolerance))
        if freeHandSmoothIterations:
            self.smoothIterationsQgsSpinBox.setValue(int(freeHandSmoothIterations))
        if freeHandSmoothOffset:
            self.smoothOffsetQgsDoubleSpinBox.setValue(float(freeHandSmoothOffset))
        if algIterations:
            self.algIterationsQgsSpinBox.setValue(int(algIterations))
        if minSegmentDistance:
            self.minSegmentDistanceQgsSpinBox.setValue(float(minSegmentDistance))
        if valueList:
            self.blackListWidget.clear()
            self.blackListWidget.addItems(valueList)
            self.blackListWidget.sortItems(order = Qt.AscendingOrder)
        if undoPoints:
            self.undoQgsSpinBox.setValue(int(undoPoints))
        if decimals:
            self.decimalQgsSpinBox.setValue(int(decimals))
        if freeHandFinalSimplifyTolerance:
            self.finalToleranceQgsDoubleSpinBox.setValue(float(freeHandFinalSimplifyTolerance))
    
    def storeParametersInConfig(self):
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals, freeHandFinalSimplifyTolerance) = self.getParameters()
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
        settings.setValue('freeHandFinalSimplifyTolerance', freeHandFinalSimplifyTolerance)
        settings.endGroup()
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.storeParametersInConfig()
        self.updateValidationToolbarConfig()
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
        (freeHandTolerance, freeHandSmoothIterations, freeHandSmoothOffset, algIterations, minSegmentDistance, valueList, undoPoints, decimals, freeHandFinalSimplifyTolerance) = self.loadParametersFromConfig()
        if not (freeHandTolerance and freeHandSmoothIterations and freeHandSmoothOffset and algIterations and valueList and undoPoints and decimals is not None and freeHandFinalSimplifyTolerance is not None):
            self.storeParametersInConfig()

    def setupModelPath(self):
        """
        Clears all model paths and leaves the default options.
        """
        self.modelPathComboBox.clear()
        self.modelPathComboBox.addItems([
            self.__dsgToolsModelPath__,
            self.__qgisModelPath__
        ])

    def setupValidationToolbarConfig(self):
        """
        Sets up Validation Toolbar parameters to DSGTools default values.
        """
        # reset combo box to default as well
        self.setupModelPath()
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        if settings.value('loadModelOutput') is None:
            settings.setValue('loadModelOutput', True)
        self.loadModelOutputCheckBox.setChecked(settings.value('loadModelOutput') in (True, "true"))
        if settings.value('checkBeforeRunModel') is None:
            settings.setValue('checkBeforeRunModel', True)
        self.checkBeforeRunModelCheckBox.setChecked(settings.value('checkBeforeRunModel') in (True, "true"))
        if settings.value('removeModelsOnExit') is None:
            settings.setValue('', False)
        self.resetModelsCheckBox.setChecked(settings.value('removeModelsOnExit') in (True, "true"))
        if settings.value('removeModelsOnNewProject') is None:
            settings.setValue('removeModelsOnNewProject', False)
        self.removeModelsProjectCheckBox.setChecked(settings.value('removeModelsOnNewProject') in (True, "true"))
        if settings.value('defaultModelPath') is None:
            settings.setValue('defaultModelPath', self.modelPathComboBox.currentText())
        idx = self.modelPathComboBox.findText(settings.value('defaultModelPath'))
        if idx < 0:
            self.modelPathComboBox.addItem(settings.value('defaultModelPath'))
        self.modelPathComboBox.setCurrentText(settings.value('defaultModelPath'))
        settings.endGroup() 

    def validationToolbarConfig(self):
        """
        Reads all parameters for Validation Toolbar.
        :return: (dict) set of parameters for Validation Toolbar.
        """
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        loadModelOutput = settings.value('loadModelOutput')
        checkBeforeRunModel = settings.value('checkBeforeRunModel')
        removeModelsOnExit = settings.value('removeModelsOnExit')
        removeModelsOnNewProject = settings.value('removeModelsOnNewProject')
        defaultModelPath = settings.value('defaultModelPath')
        settings.endGroup()
        return {
            "loadModelOutput" : loadModelOutput in (True, "true"),
            "checkBeforeRunModel" : checkBeforeRunModel in (True, "true"),
            "removeModelsOnExit" : removeModelsOnExit in (True, "true"),
            "removeModelsOnNewProject" : removeModelsOnNewProject in (True, "true"),
            "defaultModelPath" : defaultModelPath
        }

    def updateValidationToolbarConfig(self):
        """
        Updates current Validation Toolbar parameter values from GUI.
        """
        settings = QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        settings.setValue('loadModelOutput', self.loadModelOutputCheckBox.isChecked())
        settings.setValue('checkBeforeRunModel', self.checkBeforeRunModelCheckBox.isChecked())
        settings.setValue('removeModelsOnExit', self.resetModelsCheckBox.isChecked())
        settings.setValue('removeModelsOnNewProject', self.removeModelsProjectCheckBox.isChecked())
        # oldModelPath = settings.value('defaultModelPath')
        # newModelPath = self.modelPathComboBox.currentText()
        settings.setValue('defaultModelPath', self.modelPathComboBox.currentText())
        settings.endGroup()
        # if oldModelPath != newModelPath:
        #     self.modelPathChanged.emit()

    def addNewModelPath(self, modelPath, setAsDefault=True):
        """
        Adds a custom model path as an option.
        :param modelPath: (str) path to look for QGIS Processing models.
        :param setAsDefault: (bool) whether current selection should be updated to new model path.
        :return: (int) index for new model path on its selection combo box.
        """
        if not os.path.exists(modelPath) or self.modelPathComboBox.findText(modelPath) >= 0:
            return -1
        self.modelPathComboBox.addItem(modelPath)
        idx = self.modelPathComboBox.findText(modelPath)
        if setAsDefault:
            self.modelPathComboBox.setCurrentIndex(idx)
        return idx

    @pyqtSlot(bool, name="on_addModelPathPushButton_clicked")
    def setCustomModelPath(self):
        """
        Adds a custom model path and sets it as default.
        """
        fd = QFileDialog()
        newModelPath = fd.getExistingDirectory(
            caption=self.tr('Select a directory for DSGTools Validation'
                            ' Toolbar to look for QGIS Processing models')
        )
        newModelPath = newModelPath[0] if isinstance(newModelPath, tuple) else newModelPath
        if not newModelPath:
            return
        self.addNewModelPath(newModelPath)
