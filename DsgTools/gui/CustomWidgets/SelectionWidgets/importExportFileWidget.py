# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-01
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
import json
import os
from pathlib import Path

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, QDir
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QFileDialog


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "importExportFileWidget.ui")
)


class ImportExportFileWidget(QtWidgets.QWidget, FORM_CLASS):
    fileSelected = pyqtSignal(str, str)
    fileExported = pyqtSignal(str)

    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.lineEdit.setReadOnly(True)
        self.exportFilePushButton.setEnabled(False)
        self.caption = ""
        self.filter = ""
        self.fileName = None
        self.fileContent = None

    @pyqtSlot(bool)
    def on_selectFilePushButton_clicked(self):
        """
        Selects the correct way to choose files according to the type
        """
        fd = QFileDialog()
        fd.setDirectory(QDir.homePath())
        selectedFile = fd.getOpenFileName(caption=self.caption, filter=self.filter)
        if isinstance(selectedFile, tuple):
            self.fileName = Path(selectedFile[0]).name
        selectedFile = (
            selectedFile[0] if isinstance(selectedFile, tuple) else selectedFile
        )
        self.lineEdit.setText(self.fileName)
        if selectedFile == "":
            self.fileContent = None
            return
        with open(selectedFile, "r") as f:
            self.fileContent = f.read()
        self.exportFilePushButton.setEnabled(True)
        self.fileSelected.emit(self.fileName, self.fileContent)

    @pyqtSlot(bool)
    def on_exportFilePushButton_clicked(self):
        if self.fileContent is None:
            raise Exception("Invalid file content.")
        fd = QFileDialog()
        fd.setDirectory(QDir.homePath())
        filename = fd.getSaveFileName(caption=self.caption, filter=self.filter)
        filename = (
            filename[0]
            if Path(filename[0]).suffix
            in map(
                lambda x: x.strip(),
                self.filter.replace("(", "").replace(")", "").split("*")[1::],
            )
            else f"{filename[0]}.{self.filter}"
        )
        if ".model3" not in filename or ".model" not in filename:
            filename = filename + ".model3"
        with open(filename, "w") as f:
            f.write(self.fileContent)
        self.fileExported.emit(filename)

    def resetAll(self):
        """
        Resets all
        """
        self.lineEdit.clear()

    def setTitle(self, text):
        """
        Sets the label title
        """
        self.label.setText(text)

    def setCaption(self, caption):
        """
        Sets the caption
        """
        self.caption = caption

    def setFilter(self, filter):
        """
        Sets the file filter
        """
        self.filter = filter

    def setType(self, type):
        """
        Sets selection type (e.g multi, single, dir)
        """
        self.type = type

    def setFile(self, fileName, fileContent):
        self.fileName = fileName
        self.fileContent = fileContent
        self.lineEdit.setText(self.fileName)
        self.exportFilePushButton.setEnabled(
            self.fileName is not None and self.fileContent is not None
        )
        self.fileSelected.emit(self.fileName, self.fileContent)

    def getFile(self):
        return {"fileName": self.fileName, "fileContent": self.fileContent}
