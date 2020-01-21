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
from qgis.PyQt.QtCore import pyqtSlot, QObject
from qgis.PyQt.QtGui import QIcon, QColor, QPalette
from qgis.PyQt.QtWidgets import QDockWidget, QLineEdit, QPushButton

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonPropWidget import ButtonPropWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
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

class CustomFeatureButton(QObject):
    """
    Class designed to handle actions, properties and settings for buttons. It
    includes info about its styling, shortcuts and other user-defined
    caracteristics. This object MUST be serializable, since it'll be used for
    data perpetuation and state definition/loading.
    """
    # enumerator for working layer mode
    ActiveLayer, AllLayers = range(2)

    def __init__(self, props=None):
        """
        Class constructor.
        :param props: (dict) a map to button's properties.
        """
        super(CustomFeatureButton, self).__init__()
        self._props = {
            "openForm": False,
            "color": "#ffffff",
            "tooltip": "",
            "category": "",
            "shortcut": "",
            "layerMode": CustomFeatureButton.ActiveLayer
        }
        self.setProperties(props)

    def setProperties(self, props):
        """
        Modify current button properties. Only valid properties are modified
        (caveat: it still may accept invalid values).
        :param props: (dict) a map to button's new properties.
        :return: (dict) a map to current button properties.
        """
        if props is not None:
            for prop in self._props.keys():
                if prop in props:
                    self._props[prop] = props[prop]
        return dict(self._props)

    def properties(self):
        """
        Retrieves button's properties.
        :return: (dict) a map to current button properties.
        """
        # methods should return a copy of value entry in order for it no to be
        # accidentally modified 
        return dict(self._props)

    def toggleLayerMethod(self):
        """
        Toggles current layer method selection mode.
        :return: (int) current layer selection mode.
        """
        mode = self._props["layerMode"] ^ 1
        self._props["layerMode"] = mode
        return mode

    def setOpenForm(self, policy):
        """
        Defines whether current button suppresses feature form.
        :param policy: (bool) whether form should be displayed.
        """
        if type(policy) == bool: 
            self._props["openForm"] = policy
        else:
            raise TypeError(
                self.tr("Policy must be a boolean ({0}).").format(type(policy))
            )

    def openForm(self):
        """
        Retrieves current form displaying policy.
        :return: (bool) whether form is set to be displayed.
        """
        return bool(self._props["openForm"])

    def setToolTip(self, tooltip):
        """
        Defines button tool tip text.
        :param tooltip: (str) button's tool tip text.
        """
        if type(policy) == bool: 
            self._props["tooltip"] = tooltip
        else:
            raise TypeError(
                self.tr("Tool tip must be a str ({0}).").format(type(policy))
            )

    def toolTip(self):
        """
        Button's tool tip text.
        :return: (str) button's tool tip text.
        """
        return bool(self._props["tooltip"])

    def setToolTip(self, tooltip):
        """
        Defines button tool tip text.
        :param tooltip: (str) button's tool tip text.
        """
        if type(policy) == bool: 
            self._props["tooltip"] = tooltip
        else:
            raise TypeError(
                self.tr("Tool tip must be a str ({0}).").format(type(policy))
            )

    def toolTip(self):
        """
        Button's tool tip text.
        :return: (str) button's tool tip text.
        """
        return bool(self._props["tooltip"])
