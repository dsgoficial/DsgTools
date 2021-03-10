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
from qgis.gui import QgsColorButton
from qgis.PyQt import QtCore, QtWidgets, uic
from qgis.PyQt.QtCore import Qt, QSize, pyqtSlot
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QVBoxLayout

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'colorSelectorWidget.ui'))


class ColorSelectorWidget(QtWidgets.QWidget, FORM_CLASS):
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
        """Connects the mColorButton with the pyqt signal."""
        return self.mColorButton.colorChanged.connect(self.updateColor)

    def getCurrentColor(self):
        """Gets the current color name from mColorButton."""
        return self.mColorButton.color().name()

    def setCurrentColor(self, color):
        """Sets the color in the mColorButton and in the lineEdit."""
        self.mColorButton.setColor(QColor(color))
        self.lineEdit.setText(color)

    def widgetSizeHint(self):
        """Handles the minimum size for the composed widget."""
        mColorButtonSize = self.mColorButton.minimumSizeHint()
        lineEditSize = self.lineEdit.minimumSizeHint()
        minW = mColorButtonSize.width() + lineEditSize.width()
        minH = (mColorButtonSize.height() + lineEditSize.height()) // 2
        self.setMinimumSize(QSize(minW,minH))
