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
from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.MultiDsSelectorWidgets.multiDsWidgetFactory import MultiDsWidgetFactory

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'datasourceManagementWidget.ui'))

class DatasourceManagementWidget(QtWidgets.QWizardPage, FORM_CLASS):
    """
    Class scope:
    1- manage input/output datasources selection;
    2- prepare the conversion mapping structure using the table as a means to translate user's intentions; and
    3- read filtering info to be applied to data.
    """
    # setting signal to alert conversion tool about any active widgets change
    activeWidgetsChanged = pyqtSignal()
    # setting signal to alert conversion tool about any datasource updates
    datasourceChangedSignal = pyqtSignal(AbstractDb)
    # filtering settings from widget container has changed signal
    containerFilterSettingsChanged = pyqtSignal(DatasourceContainerWidget)
    
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        """
        super(DatasourceManagementWidget, self).__init__()
        # define mapping from GUI to enum
        self.sourceNameDict = {
            self.tr('Select a datasource driver') : DsgEnums.NoDriver,
            'PostGIS' : DsgEnums.PostGIS,
            self.tr('PostGIS (create new database)') : DsgEnums.NewPostGIS,
            'SpatiaLite' : DsgEnums.SpatiaLite,
            self.tr('SpatiaLite (create new database)') : DsgEnums.NewSpatiaLite,
            'Shapefile' : DsgEnums.Shapefile,
            self.tr('Shapefile (create new database)') : DsgEnums.NewShapefile,
            'Geopackage' : DsgEnums.Geopackage,
            self.tr('Geopackage (create new database)') : DsgEnums.NewGeopackage
        }
        self.setupUi(self)
        # adds all available drivers to conversion to GUI
        self.fillSupportedDatasources()
        # keep track of all (in)active widgets on input/output GUI
        self.activeDrivers = dict()
        self.addSourcePushButton.setToolTip(self.tr('Add single datasource'))
        self.addMultiSourcePushButton.setToolTip(self.tr('Add multiple datasource'))
        # centralize all tool signals in order to keep track of all non-standard signals used
        self.connectClassSignals()

    def connectClassSignals(self):
        """
        Connects all tool generic behavior signals.
        """
        # add single datasource
        self.addSourcePushButton.clicked.connect(self.addDatasourceWidget)
        # add multiple datasources
        self.addMultiSourcePushButton.clicked.connect(self.addMultiDatasourceWidgets)

    def fillSupportedDatasources(self, inputPage=True):
        """
        Fills the datasource selection combobox with all supported drivers.
        :param inputPage: (bool) indicates if this object works as an input page.
        """
        # clear contents
        self.datasourceComboBox.clear()
        if inputPage:
            # if it's an input page, items should not include the option for a new datasource
            items = []
            for ds in self.sourceNameDict:
                if self.tr('new') in ds:
                    continue
                else:
                    items.append(ds)
        else:
            items = list(self.sourceNameDict.keys())
        self.datasourceComboBox.addItems(items)

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
        :return: (QWidget) newly added widget.
        """
        # get current text on datasource techonology selection combobox
        currentDbSource = self.datasourceComboBox.currentText()
        # identify if it's an input or output page call
        inputPage = (self.objectName() == 'datasourceManagementWidgetIn')
        if currentDbSource:
            # in case a valid driver is selected, add its widget to the interface
            source = self.sourceNameDict[currentDbSource]
            if source != DsgEnums.NoDriver:
                w = DatasourceContainerWidget(source=source, inputContainer=inputPage)
                # connect removal widget signal to new widget
                w.removeWidget.connect(self.removeWidget)
                # connect datasource change signal to this class datasource signal change
                w.connWidget.selectionWidget.dbChanged.connect(self.datasourceChanged)
                # connect datasource change signal to its filters reset method
                w.connWidget.selectionWidget.dbChanged.connect(w.clearFilters)
                # connect filtering settings changed signal to this class signal on filtering settings change
                w.filterSettingsChanged.connect(self.containerFilterSettingsChanged)
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

    def addMultiDatasourceWidgets(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        actionDict = {
            DsgEnums.NoDriver : lambda : None, # no action is executed in case a driver is not selected
            DsgEnums.PostGIS : lambda : MultiDsWidgetFactory.getMultiDsSelector(driver=DsgEnums.PostGIS).exec_(),
            DsgEnums.NewPostGIS : lambda : print('NADA A FAZER AGORA'),
            DsgEnums.SpatiaLite : lambda : self.addMultiFile(extensionFilter='SpatiaLite Databases (*.sqlite)'),
            DsgEnums.NewSpatiaLite : lambda : print('NADA A FAZER AGORA'),
            DsgEnums.Shapefile : lambda : print('NADA A FAZER AGORA'),
            DsgEnums.NewShapefile : lambda : print('NADA A FAZER AGORA'),
            DsgEnums.Geopackage : lambda : print('NADA A FAZER AGORA'),
            DsgEnums.NewGeopackage : lambda : print('NADA A FAZER AGORA')
        }
        # get current text on datasource techonology selection combobox
        currentDbSource = self.sourceNameDict[self.datasourceComboBox.currentText()]
        actionDict[currentDbSource]()

    def addMultiFile(self, extensionFilter=None):
        """
        Adds widgets for all selected files.
        """
        # get current text on datasource techonology selection combobox
        fList = self.getMultiFile(extensionFilter=extensionFilter)
        for dbName in fList:
            # add new widget to GUI
            w = self.addDatasourceWidget()
            # set db (all file-based drivers have a 'lineEdit' object due to their common child 'SelectFileWidget')
            w.connWidget.selectionWidget.connectionSelectorLineEdit.lineEdit.setText(dbName)

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
        # disconnect all widget connected signals
        try:
            w.removeWidget.disconnect(self.removeWidget)
        except:
            pass
        try:
            w.connWidget.selectionWidget.dbChanged.disconnect(self.datasourceChanged)
        except:
            pass
        # remove from active dict
        try:
            self.activeDrivers[w.connWidget.getSelectionWidgetName(source=w.connWidget.source)].remove(w)
        except:
            # THIS PAIR TRY-EXCEPT IS ONLY TILL NEW DATASOURCE OPTIONS ARE ADJUSTED ( VALUEERROR RAISED DUE TO HALF-IMPLEMENTATION)
            pass
        # remove widget from GUI, remove its reference on a parent widget and delete it
        self.datasourceLayout.removeWidget(w)
        w.setParent(None)
        del w
        # reset all driver's groupboxes names
        self.resetWidgetsTitle()
        # emit current active widgets changed signal
        self.activeWidgetsChanged.emit()

    def datasourceChanged(self, newDbAbstract):
        """
        Keeps track of every container widget's abstract database change.
        """
        # if any abstractDb changes
        self.datasourceChangedSignal.emit(newDbAbstract)
