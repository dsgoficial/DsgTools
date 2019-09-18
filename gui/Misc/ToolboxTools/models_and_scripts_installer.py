# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-06-05
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
import shutil

# Import the PyQt and QGIS libraries
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QListWidgetItem, QDialog, QAbstractButton

from processing.core.Processing import Processing
from qgis.core import QgsMessageLog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'models_and_scripts_installer.ui'))

currentPath = os.path.dirname(__file__)

class ModelsAndScriptsInstaller(QDialog, FORM_CLASS):
    def __init__(self):
        """
        Constructor
        """
        super(ModelsAndScriptsInstaller, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.models = self.getModels()
        self.scripts = self.getScripts()

        self.createItems(self.modelsList, self.models)
        self.createItems(self.scriptsList, self.scripts)

    def __del__(self):
        pass

    def createItems(self, widget, names):
        """
        Create items 
        """
        for name in names:
            item = QListWidgetItem(widget)
            text = name.split(os.sep)[-1]
            item.setText(text)

    def scanFolder(self, folder, extension):
        """
        Scans folder for models and scripts
        """
        ret = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                ext = file.split('.')[-1]
                if ext == extension:
                    path = os.path.join(root, file.decode(encoding='UTF-8'))
                    ret.append(path)

        return ret

    def getModels(self):
        """
        Get models in the folder
        """
        modelspath = os.path.join(currentPath, '..', 'QGIS_Models')
        extension = 'model'
        return self.scanFolder(modelspath, extension)

    def getScripts(self):
        """
        Get scripts in the folder
        """
        scriptspath = os.path.join(currentPath, '..', 'QGIS_Scripts')
        extension = 'py'
        return self.scanFolder(scriptspath, extension)

    def copyFiles(self, widget, files, folder):
        """
        Copy selected files to the correct scripts/models folder location
        """
        for item in widget.selectedItems():
            text = item.text()
            for file in files:
                if text in file:
                    destination = os.path.join(folder, text)
                    try:
                        shutil.copy2(file, destination)
                    except IOError as e:
                        QgsMessageLog.logMessage(self.tr('Error copying file: ')+text+'\n'+e.strerror, "DSGTools Plugin", QgsMessageLog.INFO)
                        continue

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Clears the selection
        """
        if self.buttonBox.standardButton(button) == QDialogButtonBox.Reset:
            self.modelsList.clearSelection()
            self.scriptsList.clearSelection()

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Copy the files to the correct location
        """
        self.copyFiles(self.scriptsList, self.scripts, os.path.join(currentPath, '..', '..', '..', '..', 'processing', 'scripts'))
        Processing.initialize()
        self.copyFiles(self.modelsList, self.models, os.path.join(currentPath, '..', '..', '..', '..', 'processing', 'models'))
        Processing.initialize()
