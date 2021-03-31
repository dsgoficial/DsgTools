# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by  Francisco Alves Camello Neto -
                                    Surveying Technician @ Brazilian Army
        email                : camello.francisco@eb.mil.br
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
import re
from qgis.gui import QgsColorButton
from qgis.PyQt import QtCore, QtWidgets, uic
from qgis.PyQt.QtCore import Qt, QSize, pyqtSlot
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QWidget, QLineEdit

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'colorSelectorWidget.ui'))


class ColorSelectorWidget(QWidget, FORM_CLASS):
    """
    Widget to simultaneously get the color and shows the color name
    and vice-versa.
    """
    mColorButton = QgsColorButton()
    lineEdit = QLineEdit()

    def __init__(self, parent=None):
        """Constructor."""
        super(ColorSelectorWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.widgetSizeHint()
        self.colorChanged()
        self.lineEdit.textEdited.connect(self.setCurrentColor)

    @QtCore.pyqtSlot()
    def updateColor(self):
        """
        Emits a pyqtsignal to update a qlineEdit with the correspondent
        color name.
        """
        color = self.mColorButton.color().name()
        self.lineEdit.setText(color)

    def colorChanged(self):
        """
        Connects the mColorButton with the pyqt signal.
        :return: (signal): emitted whenever a new color is set for the button.
        """
        return self.mColorButton.colorChanged.connect(self.updateColor)

    def getCurrentColor(self):
        """
        Gets the current color name from mColorButton.
        :return: (QColor): return the color's name in double hex format #RRGGBB.
        """
        return self.mColorButton.color().name()

    def setCurrentColor(self, color):
        """
        Sets the color both in the mColorButton and lineEdit.
        :param (str) color: hex RGB code, color name, or a list of RGB numbers.
        """
        listColor = re.search("\\d{1,3},\\d{1,3},\\d{1,3}", color)
        if listColor:
            color = listColor.string.split(',')
            rgb = QColor(int(color[0]),int(color[1]),int(color[2]))
            self.mColorButton.setColor(rgb)
        else:
            self.mColorButton.setColor(QColor(color))
            self.lineEdit.setText(color)

    def widgetSizeHint(self):
        """
        Sets the minimum size for the composed widget to fit it with
        the OTW's resize policies.
        """
        mColorButtonSize = self.mColorButton.size()
        lineEditSize = self.lineEdit.size()
        minW = mColorButtonSize.width() + lineEditSize.width() + 5
        minH = (mColorButtonSize.height() + lineEditSize.height()) // 2
        self.setMinimumSize(QSize(minW,minH))
