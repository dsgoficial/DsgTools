# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtGui import QIntValidator

# DSGTools imports

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "contour_value.ui")
)


class ContourValue(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, contour_tool, parent=None):
        """
        Constructor
        """
        super(ContourValue, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.value_line_edit.setValidator(QIntValidator(0, 1000000))
        self.contour_tool = contour_tool

    @pyqtSlot(bool)
    def on_cancel_push_button_clicked(self):
        """
        Closes the dialog
        """
        self.done(0)

    @pyqtSlot()
    def on_ok_push_button_clicked(self):
        """
        Gets the first value entered by the user and return it
        :return: 1 - Success
        """
        value = self.value_line_edit.text()
        self.contour_tool.setFirstValue(int(value))
        self.done(1)
