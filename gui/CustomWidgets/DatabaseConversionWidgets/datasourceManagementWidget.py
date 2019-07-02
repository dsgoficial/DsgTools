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
from functools import partial

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
    activeWidgetAdded = pyqtSignal(DatasourceContainerWidget)
    activeWidgetRemoved = pyqtSignal(DatasourceContainerWidget)
    # setting signal to alert conversion tool about any datasource updates
    datasourceChangedSignal = pyqtSignal(AbstractDb)
    widgetUpdated = pyqtSignal(DatasourceContainerWidget)
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
        :param e: (DatasourceContainerWidget) widget to be added to the dict.
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
                container = DatasourceContainerWidget(source=source, isInput=inputPage)
                # connect removal widget signal to new widget
                container.removeWidget.connect(self.removeWidget)
                # connect datasource change signal to this class datasource signal change
                emitWidgetAlias = lambda newAbstract : self.datasourceChanged(
                                                            newAbstract=newAbstract,
                                                            containerWidget=container
                                                        )
                container.connectionWidget.selectionWidget.dbChanged.connect(emitWidgetAlias)
                # connect datasource change signal to its filters reset method
                container.connectionWidget.selectionWidget.dbChanged.connect(container.clearFilters)
                # connect filtering settings changed signal to this class signal on filtering settings change
                container.filterSettingsChanged.connect(self.containerFilterSettingsChanged)
                # add new driver container to GUI 
                self.datasourceLayout.addWidget(container)
                # update dict of active widgets
                self.addElementToDict(k=currentDbSource, e=container, d=self.activeDrivers)
                # reset all driver's groupboxes names
                self.resetWidgetsTitle()
                # emit active widget that has been added
                self.activeWidgetAdded.emit(container)
                # returns newly added widget
                return container

    def addMultiDatasourceWidgets(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        # identify source
        source = self.sourceNameDict[self.datasourceComboBox.currentText()]
        if source != DsgEnums.NoDriver:
            # get driver's multi selection dialog
            dlg = MultiDsWidgetFactory.getMultiDsSelector(driver=source)
            result = dlg.exec_()
            if not result:
                # in case Ok was selected
                for ds, dsPath in dlg.datasources.items():
                    # add new widget container for it
                    container = self.addDatasourceWidget()
                    # set datasource to it
                    container.setDatasource({ds : dsPath})

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
        :param w: (QWidget) driver container widget to be removed. 
        """
        # disconnect all widget connected signals
        w.blockSignals(True)
        # remove from active dict
        self.activeDrivers[self.tr(w.selectionWidgetName())].remove(w)
        self.datasourceLayout.removeWidget(w)
        # reset all driver's groupboxes names
        self.resetWidgetsTitle()
        # emit widget that has been removed
        self.activeWidgetRemoved.emit(w)
        # remove widget from GUI, remove its reference on a parent widget and delete it
        w.setParent(None)
        del w

    def datasourceChanged(self, newAbstract, containerWidget):
        """
        Keeps track of every container widget's abstract database change.
        """
        # if any abstractDb changes
        # # keep orignal abstract change signal behavior
        # self.datasourceChangedSignal.emit(newAbstract)
        # clear widget's filters
        containerWidget.clearFilters()
        # advise which widget was updated
        self.widgetUpdated.emit(containerWidget)

    def validate(self):
        """
        Validates container GUI parameters.
        :return: (str) invalidation reason.
        """
        if self.objectName() == 'datasourceManagementWidgetIn':
            pageError = self.tr('Input Error!')
        else:
            pageError = self.tr('Output Error!')
        for containers in self.activeDrivers.values():
            for container in containers:
                if not container.isValid():
                    return '{0} {1}: {2}'.format(pageError, container.groupBox.title(), container.validate())
        # validate selection widget
        return ''

    def isValid(self):
        """
        Validates selection widgets contents.
        :return: (bool) invalidation status.
        """
        for containers in self.activeDrivers.values():
            for container in containers:
                if not container.isValid():
                    return False
        # validate selection widget
        return True
