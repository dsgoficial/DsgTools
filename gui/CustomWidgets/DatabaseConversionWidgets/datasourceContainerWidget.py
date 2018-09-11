# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-09-05
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

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot

from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.connectionComboBox import ConnectionComboBox
from DsgTools.gui.CustomWidgets.ConnectionWidgets.AdvancedConnectionWidgets.databaseFileLineEdit import DatabaseFileLineEdit
# from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import SelectFileWidget

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceContainerWidget.ui'))

class DatasourceContainerWidget(QtWidgets.QWidget, FORM_CLASS):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """
    # signal to be emitted when deletion button is clicked - emits itself (QWidget)
    removeWidget = pyqtSignal(QtWidgets.QWidget)

    def __init__(self, source, inputContainer, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        :param source: (str) driver codename to have its widget produced.
        :param inputContainer: (bool) indicates whether the chosen database is supposed to be a reading/input widget or writting/output one.
        """
        super(DatasourceContainerWidget, self).__init__()
        self.setupUi(self)
        self.source = source
        self.addDatasourceSelectionWidget(source=source)
        self.setGroupWidgetName(name=source)
        if not inputContainer:
            # output widget should not have filtering options
            self.layerFilterPushButton.hide()

    def setGroupWidgetName(self, name=None):
        """
        Sets the name to the group added.
        :param name: (str) name for the group.
        """
        self.groupBox.setTitle('{0}'.format(name))

    def getWidget(self, source):
        """
        Gets the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        :return: (QWidget) driver widget, if it's supported by conversion tool.
        """
        widgetDict = {
            'PostGIS' : ConnectionComboBox(),
            'SpatiaLite' : DatabaseFileLineEdit()
            # 'SpatiaLite' : SelectFileWidget()
        }
        return widgetDict[source] if source in widgetDict else None

    def addDatasourceSelectionWidget(self, source):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        # get current text on datasource techonology selection combobox
        if source:
            # in case a valid driver is selected, add its widget to the interface
            self.connWidget = self.getWidget(source=source)
            self.driverLayout.addWidget(self.connWidget)
        else:
            # if no tech is selected, inform user and nothing else
            self.connWidget = None

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        # temporarily, it'll be set to current db name
        methodDict = {
            # using lamda functions in order to not get the method triggered whilst this dict is being instantiated
            'PostGIS' : lambda : self.getPostgisConnectionName(),
            'SpatiaLite' : lambda : self.getSpatialiteConnectionName()
        }
        return methodDict[self.source]()

    def getPostgisConnectionName(self):
        """
        Gets the PostGIS connection name.
        """
        return self.connWidget.connectionSelectorComboBox.currentText()

    def getSpatialiteConnectionName(self):
        """
        Gets the SpatiaLite connection name.
        """
        n = self.connWidget.connectionSelectorLineEdit.lineEdit.text()
        # n is a path and so it'll be something like /PATH/TO/datasource.sqlite or C:\PATH\TO\datasource.sqlite
        splitChar = '/' if '/' in n else '\\'
        ret = n.split(splitChar)[-1].split('.')[0] if n else ''
        return ret

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (object) the object representing the target datasource according to its driver. 
        """
        return self.connWidget.abstractDb if self.connWidget else None

    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        """
        Emits widget removal signal when remove button is clicked.
        """
        self.removeWidget.emit(self)
