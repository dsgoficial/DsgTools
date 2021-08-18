# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-12-19
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QWidget, QFormLayout, QLabel

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.dsgCustomComboBox import DsgCustomComboBox

class AuxLayerSelector(QWidget):
    def __init__(self, parent=None):
        super(AuxLayerSelector, self).__init__(parent)
        self.layout = QFormLayout()
    
    def setInitialState(self, initDict):
        """
        Sets widget interface with initDict entries. Keys are labels and values are list of items for each combobox corresponding to each key.
        """
        for key, value in list(initDict.items()):
            label = QLabel(key)
            widget = DsgCustomComboBox()
            widget.addItems(value)
            self.layout.addRow(label, widget)
        self.setLayout(self.layout)
    
    def resetLayout(self):
        """
        Resets current widget layout.
        """
        self.layout = QFormLayout()
        self.setLayout(self.layout)
    
    def getParameters(self):
        """
        Gets current values fom each widget as a dictionary.
        """
        returnDict = dict()
        for i in range(self.layout.rowCount()):
            key = self.layout.itemAt(i, QFormLayout.LabelRole).text()
            value = self.layout.itemAt(i, QFormLayout.FieldRole).currentText()
            returnDict[key] = value
        return returnDict