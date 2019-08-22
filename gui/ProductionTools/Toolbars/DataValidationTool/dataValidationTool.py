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

import processing
from processing.modeler.ModelerUtils import ModelerUtils
from qgis.core import (QgsProject,
                       QgsMapLayer,
                       QgsProcessingModelAlgorithm,
                       QgsProcessingContext,
                       QgsProcessingFeedback,
                       QgsLayerTreeLayer)
from qgis.PyQt.QtWidgets import QWidget, QMessageBox, QFileDialog
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'dataValidationTool.ui')
)

class DataValidationTool(QWidget, FORM_CLASS):
    """
    Toolbar for fast usage of processing methods. It is assumed that the models
    have all of its child algorithm's variable's well defined and the only 
    variables expected on input are the output layers, whenever needed and as 
    many as it may be. 
    """
    __dsgToolsModelPath__ = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "..", "core", "Misc", "QGIS_Models"
    )
    __qgisModelPath__ = ModelerUtils.modelsFolders()[0]
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
        return os.path.join(self.defaultModelPath(), model) if model else ""

    def defaultModelPath(self):
        """
        Gets the directory used to read and save the models shown on toolbar.
        :return: (str) default models path.
        """
        # change for DSGTools options input
        return self.__dsgToolsModelPath__ if True else self.__qgisModelPath__

    def resetModelList(self):
        """
        Clear models listed and look refill it with current models.
        """
        self.modelComboBox.clear()
        self.modelComboBox.addItem(self.tr("Select a model..."))
        self.modelComboBox.addItems([
            x.strip() for x in os.popen("ls {path} | grep '.model3$'".format(
                    path=self.defaultModelPath()
                )
            ).readlines()
        ])
        self.modelComboBox.addItems([
            x.strip() for x in os.popen("ls {path} | grep '.model$'".format(
                    path=self.defaultModelPath()
                )
            ).readlines()
        ])

    @pyqtSlot(bool, name='on_validationPushButton_toggled')
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

    def confirmAction(self, msg, showCancel=True):
        """
        Raises a message box for confirmation before executing an action.
        :param msg: (str) message to be exposed.
        :return: (bool) whether action was confirmed.
        """
        if showCancel:
            return QMessageBox.question(
                self, self.tr('Confirm Action'), msg,
                QMessageBox.Ok|QMessageBox.Cancel
            ) == QMessageBox.Ok
        else:
            return QMessageBox.question(
                self, self.tr('Confirm Action'), msg,
                QMessageBox.Ok
            ) == QMessageBox.Ok

    def modelExists(self, modelName):
        """
        Checks if model from modelPath exists (by name).
        :param modelName: (str) model name to be checked if exists.
        :return: (str) whether model exists into default directory.
        """
        return os.path.exists(
            os.path.join(self.defaultModelPath(), os.path.basename(modelName))
        )

    @pyqtSlot(int, name='on_modelComboBox_currentIndexChanged')
    def modelIsValid(self, idx):
        """
        Checks if a model is valid and sets GUI buttons enabled if so.
        :param idx: (int) index for the model to be checked.
        """
        enabled = idx > 0
        self.removeModelPushButton.setEnabled(enabled)
        self.runModelPushButton.setEnabled(enabled)
        return enabled

    def addLayerToGroup(self, layer, groupname, subgroupname=None):
        """
        Adds a layer to a group into layer panel.
        :param layer: (QgsMapLayer) layer to be added to canvas.
        :param groupname: (str) name for group to nest the layer.
        :param subgroupname: (str) name for the subgroup to be added.
        """
        root = QgsProject.instance().layerTreeRoot()
        for g in root.children():
            if g.name() == groupname:
                group = g
                break
        else:
            group = root.addGroup(groupname)
        if subgroupname is not None:
            for sg in group.children():
                if sg.name() == subgroupname:
                    subgroup = sg
                    break
            else:
                subgroup = group.addGroup(subgroupname)
        QgsProject.instance().addMapLayer(layer, False)
        subgroup.insertChildNode(1, QgsLayerTreeLayer(layer))

    @pyqtSlot(bool, name='on_addModelPushButton_clicked')
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
        dest = os.path.join(self.defaultModelPath(), modelName)
        os.popen("cp '{source}' '{dest}'".format(source=modelPath, dest=dest))
        if os.path.exists(dest):
            self.modelComboBox.addItem(modelName)
            self.modelAdded.emit(modelName)

    @pyqtSlot(bool, name='on_removeModelPushButton_clicked')
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
            modelPath = os.path.join(self.defaultModelPath(), modelName)
        msg = self.tr("Remove model '{modelName}'?".format(modelName=modelName))
        if self.confirmAction(msg):
            os.popen("rm {modelPath}".format(modelPath=modelPath))
            if not os.path.exists(modelPath):
                self.modelComboBox.removeItem(self.modelComboBox.findText(modelName))
                self.modelRemoved.emit(modelName)

    @pyqtSlot(bool, name='on_runModelPushButton_clicked')
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
            modelPath = os.path.join(self.defaultModelPath(), modelName)
        alg = QgsProcessingModelAlgorithm()
        alg.fromFile(modelPath)
        alg.initAlgorithm()
        param = {vl.name() : "memory:" for vl in alg.parameterDefinitions()}
        msg = self.tr("Would you like to run {model}").format(model=modelName)
        if not self.confirmAction(msg):
            return
        try:
            out = processing.run(alg, param)
                # "model:{modelName}".format(modelName=modelName.split(".")[0]), param
            # )
        except Exception as e:
            msg = self.tr("Unable to run {model}:\n{error}").format(model=modelName, error=str(e))
            self.confirmAction(msg, showCancel=False)
        for var, value in out.items():
            if isinstance(value, QgsMapLayer):
                value.setName("{model} {layername}".format(model=modelName, layername=var))
                self.addLayerToGroup(value, "DSGTools Validation Toolbar Output", modelName)

    def unload(self):
        """
        Method called whenever tool is being destructed. Blocks signals and clears
        all objects that it parents.
        """
        for w in self._widgets():
            w.blockSignals(True)
            del w
