# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-16
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from builtins import str
from builtins import range
import os, importlib

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import (
    QMessageBox,
    QApplication,
    QFileDialog,
    QMenu,
    QHeaderView,
)
from qgis.PyQt.QtGui import QCursor

# DsgTools imports
from DsgTools.gui.CustomWidgets.SelectionWidgets.listSelector import ListSelector
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.BasicPropertyWidgets.genericParameterSetter import (
    GenericParameterSetter,
)

from qgis.core import QgsMessageLog
import json

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "genericCompactPropertyManagerWidget.ui")
)


class GenericCompactPropertyManagerWidget(QtWidgets.QWidget, FORM_CLASS):
    Add, Remove, Import, Export, Update = list(range(5))

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(GenericCompactPropertyManagerWidget, self).__init__(parent)
        self.setupUi(self)
        self.genericDbManager = None
        self.textDict = {
            "EarthCoverage": self.tr("Earth Coverage"),
            "Customization": self.tr("Customization"),
            "Style": self.tr("Style"),
            "ValidationConfig": self.tr("Validation"),
            "Permission": self.tr("Permissions"),
            "AttributeRules": self.tr("Attribute Rules Configuration"),
            "SpatialRules": self.tr("Spatial Rules Configuration"),
            "Generic": self.tr("Generic Property"),
            "ValidationWorkflow": self.tr("Validation Workflow"),
        }
        self.widgetName = self.textDict[self.getWhoAmI()]
        self.changeTooltips(self.widgetName)
        self.parent = parent

    def refresh(self):
        """
        Refreshes interface
        """
        self.propertyComboBox.clear()
        if self.genericDbManager:
            propertyList = list(
                self.genericDbManager.getPropertyPerspectiveDict(
                    viewType=DsgEnums.Property
                ).keys()
            )
            propertyList.sort()
            self.propertyComboBox.addItems(propertyList)

    def getWhoAmI(self):
        return (
            str(self.__class__)
            .split(".")[-1]
            .replace("'>", "")
            .replace("CompactPropertyManagerWidget", "")
        )

    def instantiateManagerObject(self, abstractDb, dbDict, edgvVersion):
        """
        Reimplemented in each child.
        """
        pass

    def setParameters(self, abstractDb):
        """
        1. Get abstract db
        2. Instantiate manager object
        """
        self.abstractDb = abstractDb
        self.genericDbManager = self.instantiateManagerObject(
            abstractDb,
            {self.abstractDb.db.databaseName(): self.abstractDb},
            self.abstractDb.getDatabaseVersion(),
        )
        self.refresh()

    def changeTooltips(self, propertyName):
        """
        Changes all buttons' tooltips according to propertyName
        """
        self.createPropertyPushButton.setToolTip(
            self.tr("Add {0}").format(propertyName)
        )
        self.removePropertyPushButton.setToolTip(
            self.tr("Remove {0}").format(propertyName)
        )
        self.importPropertyPushButton.setToolTip(
            self.tr("Import {0}").format(propertyName)
        )
        self.exportPropertyPushButton.setToolTip(
            self.tr("Export {0}").format(propertyName)
        )
        self.updatePropertyPushButton.setToolTip(
            self.tr("Update {0}").format(propertyName)
        )

    def enableButtons(self, enabled):
        """
        Enables or disables all buttons according to boolean enabled
        """
        self.createPropertyPushButton.setEnabled(enabled)
        self.removePropertyPushButton.setEnabled(enabled)
        self.importPropertyPushButton.setEnabled(enabled)
        self.exportPropertyPushButton.setEnabled(enabled)
        self.updatePropertyPushButton.setEnabled(enabled)

    def getWhoAmI(self):
        return (
            str(self.__class__)
            .split(".")[-1]
            .replace("'>", "")
            .replace("CompactPropertyManagerWidget", "")
        )

    def getParameterDict(self):
        """
        This is used to get ui state
        Returns a dict in the format:
        {
            'selectedConfig':--name of the selected config--,
        }
        """
        parameterDict = dict()
        parameterDict["selectedConfig"] = self.propertyComboBox.currentText()
        return parameterDict

    def setInterface(self, parameterDict):
        """
        Uses parameterDict to populate interface
        Sets the interface with a dict in the format:
        {
            'selectedConfig':--name of the selected config--,
        }
        """
        if "selectedConfig" in parameterDict:
            idx = self.propertyComboBox.findText(
                parameterDict["selectedConfig"], flags=Qt.MatchFlags
            )
            if idx != -1:
                self.propertyComboBox.setCurrentIndex(idx)

    @pyqtSlot(bool)
    def on_createPropertyPushButton_clicked(self):
        """
        1. Open custom manager according to property type;
        2. Use manager to apply to database
        """
        dlg = GenericParameterSetter(hideDbUi=True)
        if not dlg.exec_():
            return
        propertyName = dlg.getParameters()
        if propertyName == "":
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("Warning! Enter a {0} name!").format(self.widgetName),
            )
            return
        if propertyName in list(
            self.genericDbManager.getPropertyPerspectiveDict(
                viewType=DsgEnums.Property
            ).keys()
        ):
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("Warning! {0} name already exists!").format(self.widgetName),
            )
            return
        setupDict = self.populateConfigInterface(self.abstractDb)
        if setupDict:
            self.genericDbManager.createAndInstall(
                propertyName,
                setupDict,
                self.genericDbManager.edgvVersion,
                dbList=[self.abstractDb.db.databaseName()],
            )
            self.refresh()
            QMessageBox.information(
                self,
                self.tr("Success!"),
                self.tr("{0} configuration {1} created successfuly!").format(
                    self.widgetName, propertyName
                ),
            )

    @pyqtSlot(bool)
    def on_removePropertyPushButton_clicked(self):
        """
        Removes property from database and promps if user wants to delete from server as well.
        """
        pass

    @pyqtSlot(bool)
    def on_importPropertyPushButton_clicked(self):
        """
        Imports a property file into dsgtools_admindb
        """
        fd = QFileDialog()
        widgetType = self.getWhoAmI()
        filename = fd.getOpenFileName(
            caption=self.captionDict[widgetType], filter=self.filterDict[widgetType]
        )
        if filename == "":
            QMessageBox.warning(
                self, self.tr("Warning!"), self.tr("Warning! Select a file to import!")
            )
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.importSetting(filename)
            settingName = os.path.basename(fullFilePath).split(".")[0]
            self.genericDbManager.installSetting(
                settingName, dbList=[self.abstractDb.db.databaseName()]
            )
            QApplication.restoreOverrideCursor()
            QMessageBox.information(
                self,
                self.tr("Sucess!"),
                self.tr(
                    "Success! {0} successfully imported and installed in {1}."
                ).format(widgetType, settingName),
            )
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(
                self,
                self.tr("Error!"),
                self.tr("Error! Problem importing {0}: {1}").format(
                    widgetType, ":".join(e.args)
                ),
            )
        self.refresh()

    @pyqtSlot(bool)
    def on_exportPropertyPushButton_clicked(self):
        """
        Export selected properties.
        """
        exportPropertyList = [self.propertyComboBox.currentText()]
        if exportPropertyList == []:
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("Warning! Select a profile to export!"),
            )
            return
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption=self.tr("Select a folder to output"))
        folder = folder[0] if isinstance(folder, tuple) else folder
        if folder == "":
            # QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a output!'))
            return
        edgvVersion = self.genericDbManager.edgvVersion
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            for exportProperty in exportPropertyList:
                self.genericDbManager.exportSetting(exportProperty, edgvVersion, folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(
                self,
                self.tr("Success!"),
                self.tr("Success! {0} successfully exported.").format(self.widgetName),
            )
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(
                self,
                self.tr("Error!"),
                self.tr("Error! Problem exporting {0}: {1}").format(
                    self.widgetName, ":".join(e.args)
                ),
            )

    @pyqtSlot(bool)
    def on_updatePropertyPushButton_clicked(self):
        """
        Updates property.
        1. Get propertyName
        2. Get propertyDict
        3. Instantiate config interface and get new dict
        4. Update property
        """
        propertyName = self.propertyComboBox.currentText()
        propertyDict = self.genericDbManager.getPropertyPerspectiveDict(
            viewType=DsgEnums.Property
        )
        if propertyName not in list(propertyDict.keys()):
            QMessageBox.critical(
                self,
                self.tr("Error!"),
                self.tr("Error! Problem getting {0}: Invalid property {1}").format(
                    self.widgetName, propertyName
                ),
            )
            return
        parameterDict = self.genericDbManager.getSetting(
            propertyName, self.genericDbManager.edgvVersion
        )
        setupDict = self.populateConfigInterface(
            self.abstractDb, jsonDict=parameterDict
        )
        if setupDict:
            try:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                self.genericDbManager.updateSetting(propertyName, setupDict)
                QApplication.restoreOverrideCursor()
                QMessageBox.information(
                    self,
                    self.tr("Success!"),
                    self.tr("Success! Property {0} successfully updated.").format(
                        propertyName
                    ),
                )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(
                    self,
                    self.tr("Error!"),
                    self.tr("Error! Problem updating {0}").format(propertyName),
                )

    def populateConfigInterface(self, abstractDb, jsonDict=None):
        return None
