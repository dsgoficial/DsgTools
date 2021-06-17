# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

from functools import partial

from qgis.core import Qgis, QgsProject, QgsVectorLayer, QgsMapLayerProxyModel
from qgis.gui import QgsMessageBar, QgsMapLayerComboBox, QgsFieldExpressionWidget
from qgis.PyQt.QtCore import QSize, QRegExp
from qgis.PyQt.QtGui import QRegExpValidator
from qgis.PyQt.QtWidgets import (QWidget,
                                 QCheckBox,
                                 QComboBox,
                                 QLineEdit,
                                 QVBoxLayout)
from processing.gui.wrappers import (WidgetWrapper,
                                     DIALOG_STANDARD,
                                     DIALOG_MODELER,
                                     DIALOG_BATCH)

from DsgTools.core.GeometricTools\
             .spatialRelationsHandler import (SpatialRule,SpatialRelationsHandler)
from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets\
             .orderedTableWidget import OrderedTableWidget

class EnforceSpatialRuleWrapper(WidgetWrapper):
    __ATTRIBUTE_MAP_VERSION = 0.2
    def __init__(self, *args, **kwargs):
        super(EnforceSpatialRuleWrapper, self).__init__(*args, **kwargs)
        self.messageBar = QgsMessageBar(self.panel)
        self.panel.resizeEvent = self.resizeEvent
        self._lastError = ""

    def resizeEvent(self, e):
        """
        Resize QgsMessageBar to widget's width
        """
        self.messageBar.resize(
            QSize(
                self.panel.parent().geometry().size().width(),
                30
            )
        )

    def ruleNameWidget(self):
        """
        Retrieves the widget for reading/setting rule name.
        :return: (QLineEdit)
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Set a name for this spatial rule..."))
        return le

    def mapLayerComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget. 
        """
        cb = QgsMapLayerComboBox()
        cb.setFilters(QgsMapLayerProxyModel.VectorLayer)
        return cb

    def mapLayerModelDialog(self):
        """
        Retrieves widget for map layer selection in a model dialog setup.
        :return: (QLineEdit) map layer setter widget for processing dialog
                 mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Type a vector layer's name..."))
        return le

    def filterExpressionWidget(self):
        """
        Retrieves a new widget for filtering expression setting.
        :return: (QgsFieldExpressionWidget) snap mode selection widget.
        """
        return QgsFieldExpressionWidget()

    def predicateComboBox(self):
        """
        Retrieves widget for spatial predicate selection.
        :return: (QComboBox) a combo box with all available predicates.
        """
        cb = QComboBox()
        cb.addItems(
            list(SpatialRelationsHandler().availablePredicates().values())
        )
        return cb

    def de9imWidget(self):
        """
        Creates a new widget to handle DE-9IM masks as input.
        :return: (QLineEdit) a line edit with a DE-9IM text validator.
        """
        le = QLineEdit()
        regex = QRegExp("[FfTt012\*]{9}")
        le.setValidator(QRegExpValidator(regex, le))
        le.setPlaceholderText(self.tr("Type in a DE-9IM as 'T*F0*F21*'..."))
        return le

    def cardinalityWidget(self):
        """
        Retrieves a widget for cardinality setting.
        :return: (QLineEdit) cardinality widget with its content validation
                 applied.
        """
        le = QLineEdit()
        regex = QRegExp("[0-9\*]\.\.[0-9\*]")
        le.setValidator(QRegExpValidator(regex, le))
        le.setPlaceholderText("1..*")
        return le

    def useDE9IM(self):
        """
        Identifies whether user chose to input predicate as a DE-9IM mask.
        :return: (bool) whether GUI should handle the DE-9IM mask widget over
                 the combo box selection.
        """
        return self.panel.cb.isChecked()

    def _checkCardinalityAvailability(self, row):
        """
        Checks if the cardinality for the rule at a given row is available.
        Cardinality is only handled when predicate is provided through the
        combo box options and are not available for the "NOT" options.
        :param row: (int) row to have its cardinality checked.
        :return: (bool) whether cardinality is available
        """
        otw = self.panel.otw
        if self.useDE9IM():
            # if user is using the DE-9IM input, cardinality won't be
            # managed
            otw.itemAt(row, 7).setEnabled(True)
            return True
        predicate = otw.getValue(row, 3)
        handler = SpatialRelationsHandler()
        noCardinality = predicate in (
            handler.DISJOINT, handler.NOTEQUALS, handler.NOTINTERSECTS,
            handler.NOTTOUCHES, handler.NOTCROSSES, handler.NOTWITHIN,
            handler.NOTOVERLAPS, handler.NOTCONTAINS
        )
        otw.itemAt(row, 7).setEnabled(not noCardinality)
        if noCardinality:
            otw.setValue(row, 7, "")
        return not noCardinality

    def postAddRowStandard(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        :param row: (int) row to have its widgets setup.
        """
        # in standard GUI, the layer selectors are QgsMapLayerComboBox, and its
        # layer changed signal should be connected to the filter expression
        # widget setup
        otw = self.panel.otw
        for col in [1, 5]:
            mapLayerComboBox = otw.itemAt(row, col)
            filterWidget = otw.itemAt(row, col + 1)
            mapLayerComboBox.layerChanged.connect(filterWidget.setLayer)
            mapLayerComboBox.layerChanged.connect(
                partial(filterWidget.setExpression, "")
            )
            # first setup is manual though
            vl = mapLayerComboBox.currentLayer()
            if vl:
                filterWidget.setLayer(vl)
        predicateWidget = otw.itemAt(row, 3)
        predicateWidget.currentIndexChanged.connect(
            partial(self._checkCardinalityAvailability, row)
        )
        # also triggers the action for the first time it is open
        self._checkCardinalityAvailability(row)

    def postAddRowModeler(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        :param row: (int) row to have its widgets setup.
        """
        otw = self.panel.otw
        def checkLayerBeforeConnect(le, filterExp):
            lName = le.text().strip()
            for layer in QgsProject.instance().mapLayersByName(lName):
                if isinstance(layer, QgsVectorLayer) and layer.name() == lName:
                    filterExp.setLayer(layer)
                    return
            filterExp.setLayer(None)
        for col in [1, 5]:
            le = otw.itemAt(row, col)
            filterWidget = otw.itemAt(row, col + 1)
            le.editingFinished.connect(
                partial(checkLayerBeforeConnect, le, filterWidget)
            )
        predicateWidget = otw.itemAt(row, 3)
        predicateWidget.currentIndexChanged.connect(
            partial(self._checkCardinalityAvailability, row)
        )
        self._checkCardinalityAvailability(row)

    def standardPanel(self):
        """
        Returns the table prepared for the standard Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        widget = QWidget()
        layout = QVBoxLayout()
        # added as an attribute in order to make it easier to be read
        widget.cb = QCheckBox()
        widget.cb.setText(self.tr("Use DE-9IM inputs"))
        layout.addWidget(widget.cb)
        widget.otw = OrderedTableWidget(headerMap={
            0 : {
                "header" : self.tr("Rule name"),
                "type" : "widget",
                "widget" : self.ruleNameWidget,
                "setter" : "setText",
                "getter" : "text"
            },
            1 : {
                "header" : self.tr("Layer A"),
                "type" : "widget",
                "widget" : self.mapLayerComboBox,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            },
            2 : {
                "header" : self.tr("Filter A"),
                "type" : "widget",
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            3 : {
                "header" : self.tr("Predicate"),
                "type" : "widget",
                "widget" : self.predicateComboBox,
                "setter" : "setCurrentIndex",
                "getter" : "currentIndex"
            },
            4 : {
                "header" : self.tr("DE-9IM mask predicate"),
                "type" : "widget",
                "widget" : self.de9imWidget,
                "setter" : "setText",
                "getter" : "text"
            },
            5 : {
                "header" : self.tr("Layer B"),
                "type" : "widget",
                "widget" : self.mapLayerComboBox,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            },
            6 : {
                "header" : self.tr("Filter B"),
                "type" : "widget",
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            7 : {
                "header" : self.tr("Cardinality"),
                "type" : "widget",
                "widget" : self.cardinalityWidget,
                "setter" : "setText",
                "getter" : "text"
            }
        })
        def handlePredicateColumns(checked):
            """
            Predicate input widgets are mutually exclusively: the user may only
            input data through either of them. This method manages hiding and
            showing correct columns in accord to the user selection.
            :param checked: (bool) whether the DE-9IM usage checkbox is ticked.
            """
            widget.otw.tableWidget.hideColumn(3 if checked else 4)
            widget.otw.tableWidget.showColumn(4 if checked else 3)
        widget.cb.toggled.connect(handlePredicateColumns)
        widget.cb.toggled.emit(widget.cb.isChecked())
        widget.otw.setHeaderDoubleClickBehaviour("replicate")
        widget.otw.rowAdded.connect(self.postAddRowStandard)
        layout.addWidget(widget.otw)
        widget.setLayout(layout)
        return widget

    def batchPanel(self):
        """
        Returns the table prepared for the batch Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        return self.standardPanel()

    def modelerPanel(self):
        """
        Returns the table prepared for the modeler Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        widget = QWidget()
        layout = QVBoxLayout()
        # added as an attribute in order to make it easier to be read
        widget.cb = QCheckBox()
        widget.cb.setText(self.tr("Use DE-9IM inputs"))
        layout.addWidget(widget.cb)
        widget.otw = OrderedTableWidget(headerMap={
            0 : {
                "header" : self.tr("Rule name"),
                "type" : "widget",
                "widget" : self.ruleNameWidget,
                "setter" : "setText",
                "getter" : "text"
            },
            1 : {
                "header" : self.tr("Layer A"),
                "type" : "widget",
                "widget" : self.mapLayerModelDialog,
                "setter" : "setText",
                "getter" : "text"
            },
            2 : {
                "header" : self.tr("Filter A"),
                "type" : "widget",
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            3 : {
                "header" : self.tr("Predicate"),
                "type" : "widget",
                "widget" : self.predicateComboBox,
                "setter" : "setCurrentIndex",
                "getter" : "currentIndex"
            },
            4 : {
                "header" : self.tr("DE-9IM mask predicate"),
                "type" : "widget",
                "widget" : self.de9imWidget,
                "setter" : "setText",
                "getter" : "text"
            },
            5 : {
                "header" : self.tr("Layer B"),
                "type" : "widget",
                "widget" : self.mapLayerModelDialog,
                "setter" : "setText",
                "getter" : "text"
            },
            6 : {
                "header" : self.tr("Filter B"),
                "type" : "widget",
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            7 : {
                "header" : self.tr("Cardinality"),
                "type" : "widget",
                "widget" : self.cardinalityWidget,
                "setter" : "setText",
                "getter" : "text"
            }
        })
        def handlePredicateColumns(checked):
            """
            Predicate input widgets are mutually exclusively: the user may only
            input data through either of them. This method manages hiding and
            showing correct columns in accord to the user selection.
            :param checked: (bool) whether the DE-9IM usage checkbox is ticked.
            """
            widget.otw.tableWidget.hideColumn(3 if checked else 4)
            widget.otw.tableWidget.showColumn(4 if checked else 3)
        widget.cb.toggled.connect(handlePredicateColumns)
        widget.cb.toggled.emit(widget.cb.isChecked())
        widget.otw.setHeaderDoubleClickBehaviour("replicate")
        widget.otw.rowAdded.connect(self.postAddRowModeler)
        layout.addWidget(widget.otw)
        widget.setLayout(layout)
        return widget

    def createPanel(self):
        return {
            DIALOG_MODELER : self.modelerPanel,
            DIALOG_STANDARD : self.standardPanel,
            DIALOG_BATCH : self.batchPanel
        }[self.dialogType]()
    
    def createWidget(self):
        self.panel = self.createPanel()
        self.panel.otw.showSaveLoadButtons(True)
        self.panel.otw.extension = ".rules"
        self.panel.otw.fileType = self.tr("Set of DSGTools Spatial Rules")
        self.panel.otw.setMetadata({
            "version": self.__ATTRIBUTE_MAP_VERSION
        })
        return self.panel
    
    def parentLayerChanged(self, layer=None):
        pass
    
    def setLayer(self, layer):
        pass
    
    def setValue(self, value):
        """
        Sets back parameters to the GUI. Method reimplementation.
        :param value: (list-of-SpatialRule) list of spatial rules to be set.
        """
        if not value:
            return
        otw = self.panel.otw
        useDE9IM = value[0].get("useDE9IM", False)
        self.panel.cb.setChecked(useDE9IM)
        # signal must be triggered to adjust the correct column display
        self.panel.cb.toggled.emit(useDE9IM)
        isNotModeler = self.dialogType != DIALOG_MODELER
        for rule in value:
            # GUI was crashing when passing SpatialRule straight up
            rule = SpatialRule(**rule, checkLoadedLayer=False)
            # we want to check whether the layer is loaded as this does not
            # work properly with the map layer combobox. on the modeler it
            # won't matter as it is a line edit
            if not rule.isValid(checkLoaded=isNotModeler):
                # alert the user somehow
                continue
            otw.addRow({
                0: rule.ruleName(),
                1: rule.layerA(),
                2: rule.filterA(),
                3: rule.predicateEnum(),
                4: rule.predicateDE9IM(),
                5: rule.layerB(),
                6: rule.filterB(),
                7: rule.cardinality()
            })

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an 
        algorithm call (e.g. Processing toolbox).
        """
        ruleList = list()
        otw = self.panel.otw
        useDe9im = self.useDE9IM()
        for row in range(otw.rowCount()):
            ruleList.append(
                SpatialRule(
                    name=otw.getValue(row, 0).strip(), # or \
                            # self.tr("Spatial Rule #{n}".format(n=row + 1)),
                    layer_a=otw.getValue(row, 1),
                    filter_a=otw.getValue(row, 2),
                    predicate=otw.getValue(row, 3),
                    de9im_predicate=otw.getValue(row, 4),
                    layer_b=otw.getValue(row, 5),
                    filter_b=otw.getValue(row, 6),
                    cardinality=otw.getValue(row, 7) or "1..*",
                    useDE9IM=useDe9im,
                    checkLoadedLayer=False
                ).asDict()
            )
        return ruleList

    def readModelerPanel(self):
        """
        Reads widget's contents when process' parameters are set from a modeler
        instance.
        """
        return self.readStandardPanel()

    def readBatchPanel(self):
        """
        Reads widget's contents when process' parameters are set from a batch
        processing instance.
        """
        return self.readStandardPanel()

    def validate(self, pushAlert=False):
        """
        Validates fields. Returns True if all information are filled correctly.
        :param pushAlert: (bool) whether invalidation reason should be
                          displayed on the widget.
        :return: (bool) whether set of filled parameters if valid.
        """
        inputMap = {
            DIALOG_STANDARD : self.readStandardPanel,
            DIALOG_MODELER : self.readModelerPanel,
            DIALOG_BATCH : self.readBatchPanel
        }[self.dialogType]()
        if len(inputMap) == 0:
            if pushAlert:
                self.messageBar.pushMessage(
                    self.tr("Please provide at least 1 spatial rule."),
                    level=Qgis.Warning,
                    duration=5
                )
            return False
        for row, rule in enumerate(inputMap):
            # GUI was crashing when passing SpatialRule straight up
            rule = SpatialRule(**rule)
            if not rule.isValid():
                if pushAlert:
                    self.messageBar.pushMessage(
                        self.tr("{0} (row {1}).")\
                            .format(rule.validate(), row + 1),
                        level=Qgis.Warning,
                        duration=5
                    )
                return False
        return True

    def value(self):
        """
        Retrieves parameters from current widget. Method reimplementation.
        :return: (dict) value currently set to the GUI.
        """
        if self.validate(pushAlert=True):
            return {
                DIALOG_STANDARD : self.readStandardPanel,
                DIALOG_MODELER : self.readModelerPanel,
                DIALOG_BATCH : self.readBatchPanel
            }[self.dialogType]()
    
    def postInitialize(self, wrappers):
        pass
