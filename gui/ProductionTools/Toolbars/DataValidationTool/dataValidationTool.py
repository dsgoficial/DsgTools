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

from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'dataValidationTool.ui')
)

class DataValidationTool(QWidget, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """
        Class constructor.
        :param iface: A QGIS interface instance.
        :param parent: (QtWidgets) widget parent to new instance of DataValidationTool.
        """
        super(DataValidationTool, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

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

    def unload(self):
        """
        Method called whenever tool is being destructed. Blocks signals and clears
        all objects that it parents.
        """
        for w in self._widgets():
            w.blockSignals(True)
            del w
        del self
