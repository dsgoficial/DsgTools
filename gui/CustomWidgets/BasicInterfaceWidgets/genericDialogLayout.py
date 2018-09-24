# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-24
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

from qgis.PyQt import QtWidgets, uic

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'genericDialogLayout.ui'))

class GenericDialogLayout(QtWidgets.QDialog, FORM_CLASS):
    """
    Widget composed by an empty layout. It is supposed to be used as based for dynamic GUI. 
    """
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to new instance of GenericDialogLayout.
        """
        super(GenericDialogLayout, self).__init__(parent)
        self.setupUi(self)

    def hideButtons(self):
        """
        Hides Ok and Cancel push buttons from GUI.
        """
        self.okPushButton.hide()
        self.cancelPushButton.hide()
