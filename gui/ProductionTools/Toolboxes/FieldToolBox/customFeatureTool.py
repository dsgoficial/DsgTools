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
from qgis.PyQt.QtGui import QColor, QPalette
from qgis.PyQt.QtWidgets import QDockWidget, QPushButton

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonPropWidget import ButtonPropWidget
from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None, buttonProps=None):
        """
        Class constructor.
        :param parent: (QtWidgets.*) any widget that 'contains' this tool.
        :param buttonProps: (dict) a map to pre-set buttons to be setup on the
                            interface.
        """
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
        self.buttonSetup = CustomButtonSetup(buttonProps)
        self.tableSetup()

    def tableSetup(self):
        """
        Configures table for button display.
        """
        table = self.orderedTableWidget
        table.clear()
        table.setHeaders({
            0 : {
                "header" : self.tr("Custom button"),
                "type" : "widget",
                "widget" : self.newButton,
                "setter" : "setText",
                "getter" : "text"
            }
        })
        table.setSectionResizeMode(0, "interactive")
        table.setSectionResizeMode(0, "resizetocontents")
        table.moveUpPushButton.hide()
        table.moveDownPushButton.hide()
        # table.addPushButton.hide()
        # table.removePushButton.hide()

    def newButton(self, props=None):
        """
        Get a new instance of a CustomFeatureButton based on its properties.
        :param props: (dict) a map to custom button properties.
        :return: (QPushButton/CustomFeatureButton) new custom feature button.
        """
        from random import randint
        if props is None:
            pb = QPushButton()
            pb.setText("Created button [{0}]".format(chr(randint(48, 57))))
            pb.setToolTip(self.tr("No button property was given."))
        else:
            # handle CustomFeatureButton obj in here
            pb = QPushButton()
        pal = QPalette()
        pal.setColor(
            pal.Button,
            QColor(randint(0, 255), randint(0, 255), randint(0, 255), 100)
        )
        pb.setPalette(pal)
        pb.update()
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
