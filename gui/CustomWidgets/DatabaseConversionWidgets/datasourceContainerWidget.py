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
from qgis.gui import QgsFieldExpressionWidget

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.genericDialogLayout import GenericDialogLayout
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.datasourceSelectionWidgetFactory import DatasourceSelectionWidgetFactory

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
        self.addDatasourceSelectionWidget()
        if not inputContainer:
            # output widget should not have filtering options
            self.filterPushButton.hide()
        # set filtering config
        self.filterDialog = None
        self.filters = {
            'layer' : dict(),
            'layer_filter' : dict(),
            'spatial_filter' : []
                # spatial filter dictionaty form
                # {
                #     'layer_name' : (str) layer_name,
                #     'filter_type' : (str) cut, buffer, intersect, etc
                #     'topological_relation' : (str) rule_string - inside, outside, buffer distance, etc
                # }
            }

    def setGroupWidgetName(self, name=None):
        """
        Sets the name to the group added.
        :param name: (str) name for the group.
        """
        self.groupBox.setTitle('{0}'.format(name))

    def addDatasourceSelectionWidget(self):
        """
        Adds the widget according to selected datasource on datasource combobox on first page.
        :param source: (str) driver name.
        """
        # in case a valid driver is selected, add its widget to the interface
        self.connWidget = DatasourceSelectionWidgetFactory.getSelectionWidget(source=self.source)
        self.driverLayout.addWidget(self.connWidget.selectionWidget)

    def getDatasourceConnectionName(self):
        """
        Gets the datasource connection name.
        :return: (str) datasource connection name.
        """
        # temporarily, it'll be set to current db name
        return self.connWidget.getDatasourceConnectionName()

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
        # finally, emits removal signal
        self.removeWidget.emit(self)

    def getNewLayerFilterLayout(self):
        """
        Gets the minimum filter structure (e.g. for a layer) inside a layout to be set to filter dialog.
        :return: (QVBoxLayout) 
        """
        # layout = QtWidgets.QVBoxLayout()
        # checkBox = QtWidgets.QCheckBox()
        # filterExpression = QgsFieldExpressionWidget()
        # layout.addWidget(checkBox)
        # layout.addWidget(filterExpression)
        return QtWidgets.QCheckBox(), QgsFieldExpressionWidget()

    @pyqtSlot(bool)
    def on_filterPushButton_clicked(self):
        """
        Opens filter dialog. Filters are updated as Ok push button on this dialog is clicked. If cancel is pressed,
        no update to filters contents will be made. This dialog is repopulated as filter push button from container
        is pressed. 
        """
        if self.filterDialog:
                # if dialog is already created, old signals must be blocked
                self.filterDialog.blockSignals(True)
                # and clear it
                self.filterDialog = None
        if self.connWidget:
            if not self.connWidget.getDatasourcePath():
                # in case a connection path is not found, a connection was not made ('generic text' is selected)
                return
            # instantiate a new filter dialog
            filterDlg = GenericDialogLayout()
            # set dialog title to current datasource path
            title = '{0}: {1}'.format(self.groupBox.title(), self.connWidget.getDatasourcePath())
            filterDlg.setWindowTitle(title)
            # get layers dict
            layers = self.connWidget.getLayersDict()
            # get layouts for checkboxes and filter expression widgets
            checkBoxLayout, filterExpressionLayout = QtWidgets.QVBoxLayout(), QtWidgets.QVBoxLayout()
            filterDlg.hLayout.addLayout(checkBoxLayout)
            filterDlg.hLayout.addLayout(filterExpressionLayout)
            # control dict for each new checkbox added
            widgets = dict()
            for layerName, featCount in layers.items():
                widgets[layerName] = dict()
                widgets[layerName]['checkBox'], widgets[layerName]['fieldExpression'] = dict(), dict()
                widgets[layerName]['checkBox'], widgets[layerName]['fieldExpression'] = self.getNewLayerFilterLayout()
                # allow filtering option only when layer is marked to be filtered
                widgets[layerName]['checkBox'].toggled.connect(widgets[layerName]['fieldExpression'].setEnabled)
                # add a new checkbox widget to layout for each layer found and a field expression widget
                # widgets[layerName]['checkBox'] = QtWidgets.QCheckBox()
                # widgets[layerName]['fieldExpression'] = QgsFieldExpressionWidget()
                msg = self.tr('{0} ({1} features)') if featCount > 1 else self.tr('{0} ({1} feature)')
                widgets[layerName]['checkBox'].setText(msg.format(layerName, featCount))
                if not self.filters['layer'] or layerName in self.filters['layer']:
                    # in case no filters are added or if layer is among the filtered ones, set it checked
                    widgets[layerName]['checkBox'].setChecked(True)
                layout = QtWidgets.QHBoxLayout()
                checkBoxLayout.addWidget(widgets[layerName]['checkBox'])
                filterExpressionLayout.addWidget(widgets[layerName]['fieldExpression'])
            self.filterDlg = filterDlg
            # connect cancel push button to close method
            closeAlias = lambda : self.filterDlg.close()
            self.filterDlg.cancelPushButton.clicked.connect(closeAlias)
            # connect Ok push button from Filter Dialog to filter dict update method
            self.filterDlg.okPushButton.clicked.connect(self.resetLayerFilters)
            # for last, open dialog            
            self.filterDlg.exec_()

    def resetLayerFilters(self):
        """
        Prepares filter dialog for current dataset in a given row.
        """
        # reset filters already set
        self.filters = {
            'layer' : dict(),
            'layer_filter' : dict(),
            'spatial_filter' : []
                # spatial filter dictionaty form
                # {
                #     'layer_name' : (str) layer_name,
                #     'filter_type' : (str) cut, buffer, intersect, etc
                #     'topological_relation' : (str) rule_string - inside, outside, buffer distance, etc
                # }
            }
        for widgetIdx in range(self.filterDlg.layout.count()):
            layerLayout = self.filterDlg.layout.itemAt(widgetIdx).layout()
            checkBox = layerLayout.itemAt(0).widget()
            filterExpression = layerLayout.itemAt(1).widget()
            if checkBox.isChecked():
                # filters will be applicable only if layer is supposed to be converted 
                # label format is: layer_name (feat_count feature's')
                # for some reason the char '&' got into the labels... i honestly don't know how/why
                label = checkBox.text().replace('&', '')
                featCount = label.split(' (')[1].split(' ')[0]
                layerName = label.split(' (')[0]
                # fill layer selection filter info
                self.filters['layer'].update({ layerName : int(featCount) })
                expression = filterExpression.currentText()
                if expression:
                    # fill layer features filter expression info only if an expression is found
                    self.filters['layer_filter'].update({ layerName : expression })
        self.filterDlg.close()
