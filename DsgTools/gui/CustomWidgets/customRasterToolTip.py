# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-03-29
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "createDatabaseCustomization.ui")
)


class CreateDatabaseCustomization(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, iface):
        """Constructor."""
        super(self.__class__, self).__init__()
        self.setupUi(self)

    def setToolUse(self, enabled):
        self.toolCheckBox.setEnabled(enabled)
