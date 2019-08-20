#! -*- coding: utf-8 -*-
"""
/***************************************************************************
                             -------------------
        begin                : 2019-08-20
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from processing.gui.AlgorithmDialog import AlgorithmDialog
from qgis.core import QgsProcessingModelAlgorithm, QgsProcessingFeedback, QgsProcessingContext
from qgis.PyQt.QtWidgets import QWidget, QMessageBox, QFileDialog
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'dataValidationTool.ui')
)

class DataValidationTool(QWidget, FORM_CLASS):
    __defaultModelPath__ = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "..", "core", "Misc", "QGIS_Models"
    )
    modelAdded = pyqtSignal(str)
    modelRemoved = pyqtSignal(str)

    def __init__(self, iface, parent=None):
        """
        Class constructor.
        :param iface: A QGIS interface instance.
        :param parent: (QtWidgets) widget parent to new instance of DataValidationTool.
        """
        super(DataValidationTool, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.activateTool()
        self.resetModelList()
        self._feedback = QgsProcessingFeedback()
        self._context = QgsProcessingContext()

    def _widgets(self):
        """
        Gets a list of all [important] widgets.
        :return: (list-of-QtWidgets) all widgets this object parents.
        """
        return [
            self.validationPushButton,
            self.modelComboBox,
            self.addModelPushButton,
            self.removeModelPushButton,
            self.runModelPushButton,
            self.splitter
        ]

    def model(self, idx=None):
        """
        Gets current model name or the model from an index.
        :param idx: (int) order in model combo box.
        :return: (str) model name.
        """
        if idx is not None and (self.modelComboBox.count() < idx or idx < 1):
            return ""
        return self.modelComboBox.currentText()

    def modelPath(self, idx=None):
        """
        Gets a model's path from its index.
        :param idx: (int) order in model combo box.
        :return: (str) model path.
        """
        model = self.model(idx)
        return os.path.join(self.__defaultModelPath__, model) if model else ""

    def resetModelList(self):
        """
        Clear models listed and look refill it with current models.
        """
        self.modelComboBox.clear()
        print(self.__defaultModelPath__)
        self.modelComboBox.addItem(self.tr("Select a model..."))
        self.modelComboBox.addItems([
            x.strip() for x in os.popen("ls {path} | grep '.model3$'".format(
                    path=self.__defaultModelPath__
                )
            ).readlines()
        ])
        self.modelComboBox.addItems([
            x.strip() for x in os.popen("ls {path} | grep '.model$'".format(
                    path=self.__defaultModelPath__
                )
            ).readlines()
        ])

    @pyqtSlot(bool, name = 'on_validationPushButton_toggled')
    def activateTool(self, toggled=None):
        """
        Shows/hides the toolbar.
        :param active: (bool) toolbar status.
        """
        if toggled is None:
            toggled = self.validationPushButton.isChecked()
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()

    def confirmAction(self, msg):
        """
        Raises a message box for confirmation before executing an action.
        :param msg: (str) message to be exposed.
        :return: (bool) whether action was confirmed.
        """
        return QMessageBox.question(
            self, self.tr('Confirm Action'), msg,
            QMessageBox.Ok|QMessageBox.Cancel
        ) == QMessageBox.Ok

    def modelExists(self, modelName):
        """
        Checks if model from modelPath exists (by name).
        :param modelName: (str) model name to be checked if exists.
        :return: (str) whether model exists into default directory.
        """
        return os.path.exists(
            os.path.join(self.__defaultModelPath__, os.path.basename(modelName))
        )

    @pyqtSlot(bool, name = 'on_addModelPushButton_clicked')
    def registerModel(self, modelPath=None):
        """
        Registers a model to the model runner. This application register all
        new models to a default directory.
        :param modelPath: (str) path to the model to be registered.
        """
        if modelPath is None or not isinstance(modelPath, str):
            fd = QFileDialog()
            modelPath = fd.getOpenFileName(
                caption=self.tr('Select a QGIS processing model to be added'),
                filter=self.tr('QGIS Processing Model (*.model *.model3)')
            )
            modelPath = modelPath[0] if isinstance(modelPath, tuple) else modelPath
            if modelPath == "":
                return
        msg = self.tr(
            "Model seems to be already registered, would you like to overwrite"
            " it?"
        )
        modelName = os.path.basename(modelPath)
        if self.modelExists(modelName) and not self.confirmAction(msg):
            return
        dest = os.path.join(self.__defaultModelPath__, modelName)
        os.popen('cp "{source}" "{dest}"'.format(source=modelPath, dest=dest))
        if os.path.exists(dest):
            self.modelComboBox.addItem(modelName)
            self.modelAdded.emit(modelName)

    @pyqtSlot(bool, name = 'on_removeModelPushButton_clicked')
    def unregisterModel(self, modelName=None):
        """
        Unregisters a model to the model runner. Removes the model from the 
        default directory.
        :param modelName: (str) basename for the model to be removed.
        """
        if self.modelComboBox.currentIndex() < 1:
            return
        if not modelName or isinstance(modelName, bool):
            modelName = self.model()
            modelPath = self.modelPath()
        else:
            modelPath = os.path.join(self.__defaultModelPath__, modelName)
        msg = self.tr("Remove model '{modelName}'?".format(modelName=modelName))
        if self.confirmAction(msg):
            os.popen("rm {modelPath}".format(modelPath=modelPath))
            if not os.path.exists(modelPath):
                self.modelComboBox.removeItem(self.modelComboBox.findText(modelName))
                self.modelRemoved.emit(modelName)

    @pyqtSlot(bool, name = 'on_runModelPushButton_clicked')
    def runModel(self, modelName=None):
        """
        Executes chosen model, if possible.
        :param modelPath: (str) path to the model to be registered.
        """
        if self.modelComboBox.currentIndex() < 1:
            return
        if not modelName or isinstance(modelName, bool):
            modelName = self.model()
            modelPath = self.modelPath()
        else:
            modelPath = os.path.join(self.__defaultModelPath__, modelName)
        alg = QgsProcessingModelAlgorithm()
        alg.fromFile(modelPath)
        # dlg = AlgorithmDialog(alg.create(), parent=self.iface.mainWindow())
        # dlg.runAlgorithm()

    def unload(self):
        """
        Method called whenever tool is being destructed. Blocks signals and clears
        all objects that it parents.
        """
        for w in self._widgets():
            w.blockSignals(True)
            del w
        del self
