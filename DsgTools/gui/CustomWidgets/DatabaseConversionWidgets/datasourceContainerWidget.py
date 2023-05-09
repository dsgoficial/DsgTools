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
from qgis.gui import QgsFieldExpressionWidget, QgsCollapsibleGroupBox
from qgis.utils import iface
from qgis.core import QgsProject

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.genericDialogLayout import (
    GenericDialogLayout,
)
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.filterDialog import (
    FilterDialog,
)
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.datasourceSelectionWidgetFactory import (
    DatasourceSelectionWidgetFactory,
)

import os

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "datasourceContainerWidget.ui")
)


class DatasourceContainerWidget(QtWidgets.QWidget, FORM_CLASS):
    """
    Widget resposinble for adequating GUI to chosen data driver.
    """

    # signal to be emitted when deletion button is clicked - emits itself (QWidget)
    removeWidget = pyqtSignal(QtWidgets.QWidget)
    # signal emitted to advise about filtering options change
    filterSettingsChanged = pyqtSignal(QtWidgets.QWidget)

    def __init__(self, source, isInput, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) widget parent to newly instantiated DataSourceManagementWidget object.
        :param source: (str) driver codename to have its widget produced.
        :param isInput: (bool) indicates whether the chosen database is supposed to be a reading/input widget or writting/output one.
        """
        super(DatasourceContainerWidget, self).__init__()
        self.setupUi(self)
        self.source = source
        self.addDatasourceSelectionWidget()
        if not isInput:
            # output widget should not have filtering options
            self.filterPushButton.hide()
        # set filtering config
        self.filterDlg = None
        self.filterPushButton.setToolTip(
            self.tr("Click to set datasource filter options")
        )
        self.removePushButton.setToolTip(self.tr("Remove this datasource widget"))

    def setGroupWidgetName(self, name=None):
        """
        Sets the name to the group added.
        :param name: (str) name for the group.
        """
        self.groupBox.setTitle("{0}".format(name))

    def addDatasourceSelectionWidget(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        """
        # in case a valid driver is selected, add its widget to the interface
        self.connectionWidget = DatasourceSelectionWidgetFactory.getSelectionWidget(
            source=self.source
        )
        self.driverLayout.addWidget(self.connectionWidget.selectionWidget)
        self.connectionWidget.selectionWidget.dbChanged.connect(
            lambda: self.refreshFilterDialog
        )

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        # temporarily, it'll be set to current db name
        return self.connectionWidget.getDatasourceConnectionName()

    def getDatasource(self):
        """
        Gets the datasource selected on current widget.
        :return: (object) the object representing the target datasource according to its driver.
        """
        return self.connectionWidget.getDatasource() if self.connectionWidget else None

    def setDatasource(self, newDatasource):
        """
        Sets datasource to selection widget.
        :param newDatasource: (object) varies according to driver.
        """
        if self.connectionWidget:
            self.connectionWidget.setDatasource(newDatasource)

    @pyqtSlot(bool)
    def on_removePushButton_clicked(self):
        """
        Emits widget removal signal when remove button is clicked.
        """
        # finally, emits removal signal
        self.removeWidget.emit(self)

    def refreshFilterDialog(self):
        """
        Resets filter dialog to its initial state.
        """
        if self.filterDlg:
            # if dialog is already created, old signals must be blocked
            self.filterDlg.blockSignals(True)
            # and clear it
            del self.filterDlg
            self.filterDlg = None
        self.filterDlg = FilterDialog(
            {
                l: {
                    "layer": self.connectionWidget.getLayerByName(l),
                    "featureCount": fc,
                }
                for l, fc in self.connectionWidget.getLayersDict().items()
            },
            {
                l: {
                    "layer": self.connectionWidget.getComplexLayerByName(l),
                    "featureCount": fc,
                }
                for l, fc in self.connectionWidget.getComplexDict().items()
            },
            self.connectionWidget.getDatasource(),
        )
        self.filterDlg.setWindowTitle(
            "{0}: {2} ({1})".format(
                self.groupBox.title(),
                self.connectionWidget.getDatasourcePath(),
                self.connectionWidget.getDatasourceConnectionName(),
            )
        )

    @pyqtSlot(bool)
    def on_filterPushButton_clicked(self):
        """
        Opens filter dialog. Filters are updated as Ok push button on this dialog is clicked. If cancel is pressed,
        no update to filters contents will be made. This dialog is repopulated as filter push button from container
        is pressed.
        """
        # filter dialog is only built on the first execution
        if self.filterDlg is None:
            self.refreshFilterDialog()
        if self.filterDlg.exec_() == 0:
            # in case execution changed anything - e.g. if Ok was pressed
            self.filterSettingsChanged.emit(self)

    def clearFilters(self):
        """
        Clear current filter settings.
        """
        if self.filterDlg is not None:
            self.filterDlg.blockSignals(True)
            del self.filterDlg
            self.filterDlg = None

    def filters(self):
        """
        Gets current filter selection. If filter button was not pushed, an empty dict
        is returned.
        :return: (dict) a map to current filters applied.
        """
        return (
            self.filterDlg.filters()
            if self.filterDlg is not None
            else {"layer_filter": dict(), "spatial_filter": dict()}
        )

    def driver(self):
        """
        Gets current datasource driver disposed for selection.
        :return: (DsgEnums) driver enumerator.
        """
        return self.source

    def selectionWidgetName(self):
        """
        Gets current datasource driver's name disposed for selection.
        :return: (DsgEnums) driver enumerator.
        """
        return self.connectionWidget.getSelectionWidgetName(source=self.driver())

    def validate(self):
        """
        Validates container GUI parameters.
        :return: (str) invalidation reason.
        """
        # validate selection widget
        return self.connectionWidget.validate()

    def isValid(self):
        """
        Validates selection widgets contents.
        :return: (bool) invalidation status.
        """
        return self.validate() == ""
