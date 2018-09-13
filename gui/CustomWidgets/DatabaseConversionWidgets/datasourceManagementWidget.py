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
from qgis.PyQt.QtCore import pyqtSignal

from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.datasourceContainerWidget import DatasourceContainerWidget
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceManagementWidget.ui'))

class DatasourceManagementWidget(QtWidgets.QWizardPage, FORM_CLASS):
    """
    Class scope:
    1- manage input/output datasources selection;
    2- prepare the conversion mapping structure using the table as a means to translate user's intentions; and
    3- make the call to core code to do the actual conversion.
    """
    # setting signal to alert conversion tool about any active widgets change
    activeWidgetsChanged = pyqtSignal()
    # setting signal to alert conversion tool about any datasource updates
    datasourceChangedSignal = pyqtSignal(AbstractDb)

    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        """
        super(DatasourceManagementWidget, self).__init__()
        self.setupUi(self)
        # adds all available drivers to conversion to GUI
        self.fillSupportedDatasouces()
        # centralize all tool signals in order to keep track of all non-standard signals used
        self.connectClassSignals()
        # keep track of all (in)active widgets on input/output GUI
        self.activeDrivers = dict()
        self.inactiveDrivers = dict()
        self.addSourcePushButton.setToolTip(self.tr('Add single datasource.'))
        self.addMultiSourcePushButton.setToolTip(self.tr('Add multiple datasource.'))

    def connectClassSignals(self):
        """
        Connects all tool generic behavior signals.
        """
        self.addSourcePushButton.clicked.connect(self.addDatasourceWidget)
        self.addMultiSourcePushButton.clicked.connect(self.addMultiDatasourceWidgets)
        pass

    def fillSupportedDatasouces(self):
        """
        Fills the datasource selection combobox with all supported drivers.
        """
        driversList = [DatasourceContainerWidget.NoDriver,
                        DatasourceContainerWidget.PostGIS, DatasourceContainerWidget.NewPostGIS,
                        DatasourceContainerWidget.SpatiaLite, DatasourceContainerWidget.NewSpatiaLite
                    ]
        self.datasourceComboBox.addItems(driversList)

    def addElementToDict(self, k, e, d):
        """
        Adds widget to a dict composed by list as values and driver names as key.
        :param k: (str) new widget's driver name.
        :param e: (QWidget) widget to be added to the dict.
        :param d: (dict) dictionary to be updated.
        :return: (bool) operation success status.
        """
        try:
            if k not in d:
                d[k] = [e]
            else:
                if e not in d[k]:
                    d[k].append(e)
            return e in d[k]
        except:
            return False

    def addDatasourceWidget(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        :return: (QWidget) newly added widget.
        """
        # get current text on datasource techonology selection combobox
        currentDbSource = self.datasourceComboBox.currentText()
        # identify if it's an input or output page call
        inputPage = (self.objectName() == 'datasourceManagementWidgetIn')
        if currentDbSource:
            # in case a valid driver is selected, add its widget to the interface
            # first checks if there are any widgets already created
            inactiveWidgets = self.inactiveDrivers[currentDbSource] if currentDbSource in self.inactiveDrivers else []
            if inactiveWidgets:
                # if there are inactive widgets, reuse them instead of instantianting new ones
                w = self.inactiveDrivers[currentDbSource][0]
                # remove widget from inactive dict
                self.inactiveDrivers[currentDbSource].remove(w)
                # re-display widget on GUI
                w.show()
            else:
                # if no unused widget is found, a new one will be instantiated
                w = DatasourceContainerWidget(source=currentDbSource, inputContainer=inputPage)
                # connect removal widget signal to new widget
                w.removeWidget.connect(self.removeWidget)
                # connect
                w.connWidget.dbChanged.connect(self.datasourceChanged)
                # add new driver container to GUI 
                self.datasourceLayout.addWidget(w)
            # update dict of active widgets
            self.addElementToDict(k=currentDbSource, e=w, d=self.activeDrivers)
            # reset all driver's groupboxes names
            self.resetWidgetsTitle()
            # emit signal advising that there is a new active widget
            self.activeWidgetsChanged.emit()
            # returns newly added widget
            return w
        else:
            # if no tech is selected, inform user and nothing else
            pass

    def addMultiDatasourceWidgets(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        actionDict = {
            DatasourceContainerWidget.NoDriver : lambda : None, # no action is executed in case a driver is not selected
            DatasourceContainerWidget.PostGIS : lambda : print('NADA A FAZER AGORA'),
            DatasourceContainerWidget.NewPostGIS : lambda : print('NADA A FAZER AGORA'),
            DatasourceContainerWidget.SpatiaLite : lambda : self.addMultiFile(extensionFilter='SpatiaLite Databases (*.sqlite)'),
            DatasourceContainerWidget.NewSpatiaLite : lambda : print('NADA A FAZER AGORA')
        }
        # get current text on datasource techonology selection combobox
        currentDbSource = self.datasourceComboBox.currentText()
        actionDict[currentDbSource]()

    def addMultiFile(self, extensionFilter=None):
        """
        Adds widgets for all selected files.
        """
        # get current text on datasource techonology selection combobox
        currentDbSource = self.datasourceComboBox.currentText()
        fList = self.getMultiFile(extensionFilter=extensionFilter)
        for dbName in fList:
            # add new widget to GUI
            w = self.addDatasourceWidget()
            # set db (all file-based drivers have a 'lineEdit' object due to their common child 'SelectFileWidget')
            w.connWidget.connectionSelectorLineEdit.lineEdit.setText(dbName)

    def getMultiFile(self, extensionFilter=None):
        """
        Opens dialog multiple file selection and gets file list.
        :param extensionFilter: (str) file extensions to be filtered.
        :return: (list-of-str) list containing all filenames for selected files.
        """
        fd = QtWidgets.QFileDialog()
        # get current text on datasource techonology selection combobox
        currentDbSource = self.datasourceComboBox.currentText()
        fileList = fd.getOpenFileNames(caption=self.tr("Select a {0}").format(currentDbSource), filter=extensionFilter)[0]
        return fileList

    def resetWidgetsTitle(self):
        """
        Resets all widgets containers titles.
        """
        hideAlias = lambda w : w.hide()
        for driverName, widgetList in self.activeDrivers.items():
            if not widgetList:
                # if there are no active widgets for current driver, there's nothing to be updated
                continue
            map(hideAlias, widgetList)
            for idx, w in enumerate(widgetList):
                # if there are widgets from chosen driver, reset it's group box name
                w.show()
                w.setGroupWidgetName(name='{0} #{1}'.format(driverName, idx + 1))

    def removeWidget(self, w):
        """
        Removes driver widget from GUI.
        :param w: (QWidget) driver widget to be removed. 
        """
        # hide widget from GUI
        w.hide()
        # remove from active dict
        self.activeDrivers[w.source].remove(w)
        self.activeWidgetsChanged.emit()
        # update dict of inactive widgets
        self.addElementToDict(k=w.source, e=w, d=self.inactiveDrivers)
        # reset all driver's groupboxes names
        self.resetWidgetsTitle()

    def datasourceChanged(self, newDbAbstract):
        """
        Keeps track of every container widget's abstract database change.
        """
        # if any abstractDb changes
        self.datasourceChangedSignal.emit(newDbAbstract)
