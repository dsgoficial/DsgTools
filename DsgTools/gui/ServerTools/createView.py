# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-12-14
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
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtWidgets import QAbstractItemView, QApplication, QMessageBox
from qgis.PyQt.QtGui import QCursor

# DSGTools imports

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "createView.ui"))


class CreateView(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, abstractDb, dbName, parent=None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.abstractDb = abstractDb
        self.dBLineEdit.setText(dbName)
        self.dBLineEdit.setReadOnly(True)
        self.viewTypeDict = {0: "VIEW", 1: "MATERIALIZED VIEW"}
        self.inheritanceType = {0: "FROM ONLY", 1: "FROM"}

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Creates view with resolved domain values
        """
        createViewClause = self.viewTypeDict[self.viewTypeComboBox.currentIndex()]
        fromClause = self.inheritanceType[self.inheritanceTypeComboBox.currentIndex()]
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.abstractDb.createResolvedDomainViews(createViewClause, fromClause)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(
                self,
                self.tr("Success!"),
                self.tr("Views created successfully on database ")
                + self.dBLineEdit.text(),
            )
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
