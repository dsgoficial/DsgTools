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
        email                : borba@dsg.eb.mil.br
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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFileDialog


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'selectFileWidget.ui'))

class SelectFileWidget(QtGui.QWidget, FORM_CLASS):
    filesSelected = pyqtSignal()
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.fileNameList = []
        self.lineEdit.setReadOnly(True)
        self.caption = ''
        self.filter = ''
        self.type = 'single'

    @pyqtSlot(bool)
    def on_selectFilePushButton_clicked(self):
        fd = QFileDialog()
        if self.type == 'multi':
            self.fileNameList = fd.getOpenFileNames(caption=self.caption,filter=self.filter)
            selectedFiles = ', '.join(self.fileNameList)
        elif self.type == 'single':
            selectedFiles = fd.getOpenFileName(caption=self.caption,filter=self.filter)
            if selectedFiles <> '':
                self.fileNameList = selectedFiles
        elif self.type == 'dir':
             selectedFiles = fd.getExistingDirectory(directory = os.path.expanduser('~'), caption=self.caption,options=QFileDialog.ShowDirsOnly)
             if selectedFiles <> '':
                 self.fileNameList = [selectedFiles]
        self.lineEdit.setText(selectedFiles)
        self.filesSelected.emit()
    
    def resetAll(self):
        self.lineEdit.clear()
    
    def setTitle(self,text):
        self.label.setText(text)
    
    def setCaption(self, caption):
        self.caption = caption
    
    def setFilter(self,filter):
        self.filter = filter
    
    def setType(self,type):
        self.type = type