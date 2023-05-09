# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-06
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QApplication,
    QFileDialog,
)
from qgis.PyQt.QtGui import QCursor


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "listSelector.ui")
)


class ListSelector(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, originList, destinationList, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.originList = originList
        self.destinationList = destinationList
        self.listCustomSelector.setTitle(self.tr("Select"))
        self.listCustomSelector.setFromList(
            list(originList), unique=True
        )  # passes a copy using list(<list object>)
        self.listCustomSelector.setToList(list(destinationList))

    def getSelected(self):
        return self.listCustomSelector.toLs

    def getInputAndOutputLists(self):
        return (self.listCustomSelector.fromLs, self.listCustomSelector.toLs)

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.done(0)

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.done(0)
