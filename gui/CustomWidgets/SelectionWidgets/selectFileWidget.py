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
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, QDir
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QFileDialog


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'selectFileWidget.ui'))

class SelectFileWidget(QtWidgets.QWidget, FORM_CLASS):
    filesSelected = pyqtSignal()
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.fileNameList = []
        self.lineEdit.setReadOnly(True)
        self.caption = ''
        self.filter = ''
        self.type = 'single'

    @pyqtSlot(bool)
    def on_selectFilePushButton_clicked(self):
        """
        Selects the correct way to choose files according to the type
        """
        fd = QFileDialog()
        fd.setDirectory(QDir.homePath())
        if self.type == 'multi':
            self.fileNameList = fd.getOpenFileNames(caption=self.caption, filter=self.filter)
            selectedFiles = ', '.join(self.fileNameList[0])
        elif self.type == 'single':
            selectedFiles = fd.getOpenFileName(caption=self.caption, filter=self.filter)
            if isinstance(selectedFiles, tuple):
                self.fileNameList = selectedFiles[0]
        elif self.type == 'dir':
             selectedFiles = fd.getExistingDirectory(directory=os.path.expanduser('~'), caption=self.caption, options=QFileDialog.ShowDirsOnly)
             if selectedFiles != '':
                 self.fileNameList = [selectedFiles]
        selectedFiles = selectedFiles[0] if isinstance(selectedFiles, tuple) else selectedFiles
        self.lineEdit.setText(selectedFiles)
        self.filesSelected.emit()
    
    def resetAll(self):
        """
        Resets all
        """
        self.lineEdit.clear()
        self.fileNameList = []
    
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