# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-23
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

from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot

from DsgTools.core.dsgEnums import DsgEnums

import os

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "multiNewDsSelector.ui")
)


class MultiNewDsSelector(QDialog, FORM_CLASS):
    """
    Class designed to control multiple (new) datasource selection widget.
    """

    def __init__(self, parent=None):
        """
        Class constructor
        """
        super(MultiNewDsSelector, self).__init__(parent)
        self.setupUi(self)
        self.edgv = ""
        self.crs = None
        self.numberOfDs = 0
        self.fillEdgvVersions()
        # to keep parallel with the other drivers
        self.datasources = dict()

    def fillEdgvVersions(self):
        """
        Populates EDGV combo box with available versions.
        """
        versions = [
            self.tr("EDGV Version..."),
            "EDGV 2.1.3",
            "EDGV 2.1.3 F Ter" "EDGV 2.1.3 Pro",
            "EDGV 3.0",
            "EDGV 3.0 Pro",
        ]
        self.edgvComboBox.addItems(versions)

    def amount(self):
        """
        Gets the amount of datasources to be created.
        :return: (int) amount of datasources to be created.
        """
        return self.spinBox.value()

    def edgvVersion(self):
        """
        Returns current selected EDGV version.
        :return: (str) EDGV version.
        """
        edgv = self.edgvComboBox.currentText()
        return edgv if not edgv is None and edgv != self.tr("EDGV Version...") else ""

    def authId(self):
        """
        Returns current selected EDGV version.
        :return: (str) EDGV version.
        """
        crs = self.getCrs()
        return crs.authid() if not crs is None and crs.isValid() else ""

    def getCrs(self):
        """
        Returns current selected EDGV version.
        :return: (QgsCoordinateReferenceSystem) current selected CRS.
        """
        crs = self.mQgsProjectionSelectionWidget.crs()
        return crs if not crs is None and crs.isValid() else None

    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        """
        Validates widget's contents and updates its attributes, if valid.
        :return: (int) execution's code.
        """
        # to keep parallel with the other drivers - clear previous info if Ok is pressed
        self.datasources = dict()
        if self.isValid():
            for i in range(self.amount()):
                # add an entry for each desired datasource
                # in here, we may change for an automatic datasource name to be passed on as dict key
                self.datasources[i] = {"edgv": self.edgvVersion(), "crs": self.getCrs()}
            self.close()
            return 0
        QMessageBox.warning(self, self.tr("Warning!"), self.validate())
        return 1

    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        """
        Closes dialog.
        """
        self.close()
        return 2

    def validate(self):
        """
        Validates current widget. To be validated, it is necessary:
        - a valid NEW datasource name;
        - a valid server selection;
        - a valid EDGV version selection; and
        - a valid projection selection.
        :return: (str) invalidation reason.
        """
        # check amount of servers selection
        if self.amount() == 0:
            return self.tr("Select the amount of datasources to be created.")
        # check if a valid EDGV version was selected
        if not self.edgvVersion():
            return self.tr("Invalid EDGV version.")
        # check if a valid projection was selected
        if not self.getCrs() or "EPSG" not in self.authId():
            return self.tr("Invalid CRS.")
        # if all tests were positive, widget has a valid selection
        return ""

    def isValid(self):
        """
        Validates selection widgets contents.
        :return: (bool) invalidation status.
        """
        msg = self.validate()
        return msg == ""
