# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2020-01-17
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDockWidget, QLineEdit, QPushButton

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonPropWidget import ButtonPropWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
        self.orderedTableWidget.setHeaders({
            0 : {
                "header" : self.tr("Custom button"),
                "type" : "widget",
                "widget" : self.classificationButton,
                "setter" : "setText",
                "getter" : "text"
            },
            1 : {
                "header" : self.tr("Properties"),
                "type" : "widget",
                "widget" : self.setupButton,
                "setter" : "setText",
                "getter" : "text"
            }
        })

    def classificationButton(self, props=None):
        """
        Get a new instance of a CustomFeatureButton based on its properties.
        :param props: (dict) a map to custom button properties.
        :return: (QPushButton/CustomFeatureButton) new custom feature button.
        """
        if props is None:
            pb = QPushButton()
            pb.setText("Created button")
            pb.setToolTip(self.tr("No button property was given."))
            return pb

    def setupButton(self, tooltip=None):
        """
        Generates a new default setup push button.
        :param tooltip: (str) tooltip string to be exposed.
        :return: (QPushButton) new setup push button.
        """
        pb = QPushButton()
        pb.setText("")
        pb.setIcon(
            QIcon(
                os.path.join(
                    os.path.dirname(__file__), "..", "..", "..", "..",
                    "icons", "config.png"
                )
            )
        )
        if tooltip is not None:
            pb.setToolTip(tooltip)
        pb.setBaseSize(24, 24)
        return pb

    @pyqtSlot(bool, name="on_buttonPropsPushButton_clicked")
    def setupCurrentButton(self):
        """
        Opens setup form.
        """
        # button = self.currentButton()
        # props = button.properties()
        # dlg = ButtonPropWidget(props)
        dlg = ButtonPropWidget()
        ret = dlg.exec_()
        if ret:
            pass
