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
from processing import Processing
from processing.tools import dataobjects
from processing.gui.MessageBarProgress import MessageBarProgress
from processing.gui.AlgorithmExecutor import execute
from processing.modeler.ModelerUtils import ModelerUtils
from qgis.core import (QgsProject,
                       QgsProcessingContext,
                       QgsApplication,
                       QgsMapLayer,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingOutputRasterLayer,
                       QgsProcessingOutputMapLayer,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingFeedback)
from qgis.PyQt.QtWidgets import QWidget, QMessageBox, QFileDialog
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'dataValidationTool.ui')
)

class DataValidationTool(QWidget, FORM_CLASS):
    # __defaultModelPath__ = os.path.join(
    #     os.path.dirname(__file__), "..", "..", "..", "..", "core", "Misc", "QGIS_Models"
    # )
    __defaultModelPath__ = ModelerUtils.modelsFolders()[0]
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
        dest = os.path.join(self.__defaultModelPath__, modelName)
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
            modelPath = os.path.join(self.__defaultModelPath__, modelName)
        msg = self.tr("Remove model '{modelName}'?".format(modelName=modelName))
        if self.confirmAction(msg):
            os.popen("rm {modelPath}".format(modelPath=modelPath))
            if not os.path.exists(modelPath):
                self.modelComboBox.removeItem(self.modelComboBox.findText(modelName))
                self.modelRemoved.emit(modelName)

    def runAlgorithm(self, algOrName, parameters, onFinish=None, feedback=None, context=None):
        """
        Copied from processing.Processing.Processing and modified.
        """
        if isinstance(algOrName, QgsProcessingAlgorithm):
            alg = algOrName
        else:
            alg = QgsApplication.processingRegistry().createAlgorithmById(algOrName)

        if feedback is None:
            feedback = QgsProcessingFeedback()

        if alg is None:
            msg = Processing.tr('Error: Algorithm {0} not found\n').format(algOrName)
            feedback.reportError(msg)
            raise QgsProcessingException(msg)

        if context is None:
            context = dataobjects.createContext(feedback)

        if context.feedback() is None:
            context.setFeedback(feedback)

        ok, msg = alg.checkParameterValues(parameters, context)
        if not ok:
            msg = Processing.tr('Unable to execute algorithm\n{0}').format(msg)
            feedback.reportError(msg)
            raise QgsProcessingException(msg)

        if not alg.validateInputCrs(parameters, context):
            feedback.pushInfo(
                Processing.tr('Warning: Not all input layers use the same CRS.\nThis can cause unexpected results.'))

        ret, results = execute(alg, parameters, context, feedback)
        if ret:
            feedback.pushInfo(
                Processing.tr('Results: {}').format(results))

            if onFinish is not None:
                onFinish(alg, context, feedback)
            else:
                # auto convert layer references in results to map layers
                for out in alg.outputDefinitions():
                    if out.name() not in results:
                        continue

                    if isinstance(out, (QgsProcessingOutputVectorLayer, QgsProcessingOutputRasterLayer, QgsProcessingOutputMapLayer)):
                        result = results[out.name()]
                        if not isinstance(result, QgsMapLayer):
                            layer = context.takeResultLayer(result) # transfer layer ownership out of context
                            if layer:
                                results[out.name()] = layer # replace layer string ref with actual layer (+ownership)
                    elif isinstance(out, QgsProcessingOutputMultipleLayers):
                        result = results[out.name()]
                        if result:
                            layers_result = []
                            for l in result:
                                if not isinstance(result, QgsMapLayer):
                                    layer = context.takeResultLayer(l) # transfer layer ownership out of context
                                    if layer:
                                        layers_result.append(layer)
                                    else:
                                        layers_result.append(l)
                                else:
                                    layers_result.append(l)

                            results[out.name()] = layers_result # replace layers strings ref with actual layers (+ownership)

        else:
            msg = Processing.tr("There were errors executing the algorithm.")
            feedback.reportError(msg)
            raise QgsProcessingException(msg)

        if isinstance(feedback, MessageBarProgress):
            feedback.close()
        return results

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
            modelPath = os.path.join(self.__defaultModelPath__, modelName)
        # it seems models can only be run through QGIS' model paths
        output = self.runAlgorithm(
                "model:drenagem_duplicada", {
                'dsgtools:identifyduplicatedgeometries_1:Flags Drenagem Duplicada' : 'memory:'
            })
        QgsProject.instance().addMapLayer(
            output['dsgtools:identifyduplicatedgeometries_1:Flags Drenagem Duplicada']
        )

    def unload(self):
        """
        Method called whenever tool is being destructed. Blocks signals and clears
        all objects that it parents.
        """
        for w in self._widgets():
            w.blockSignals(True)
            del w
        del self
