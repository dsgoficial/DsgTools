# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-03-04
        git sha              : $Format:%H$
        copyright            : Cesar Saez (https://gist.github.com/csaez/8b1b456ec95d95c77d42#file-qdictbox-py)
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
import sys
from collections import deque, OrderedDict
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication, QMenu
from qgis.PyQt.QtGui import QCursor
from DsgTools.gui.CustomWidgets.SelectionWidgets.customTableSelector import CustomTableSelector
from DsgTools.gui.CustomWidgets.SelectionWidgets.customSnaperParameterSelector import CustomSnaperParameterSelector
from DsgTools.gui.CustomWidgets.SelectionWidgets.customReferenceAndLayersParameterSelector import CustomReferenceAndLayersParameterSelector
from DsgTools.gui.CustomWidgets.AdvancedInterfaceWidgets.auxLayerSelector import AuxLayerSelector
from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedRecursiveSnapWidget import OrderedRecursiveSnapWidget
from DsgTools.core.ValidationTools.ValidationProcesses.hierarchicalSnapLayerOnLayerProcess import HierarchicalSnapParameters

class ProcessParametersDialog(QtWidgets.QDialog):
    WIDGETS = {str: QtWidgets.QLineEdit,
               int: QtWidgets.QSpinBox,
               float: QtWidgets.QDoubleSpinBox,
               list: CustomTableSelector,
               tuple: CustomSnaperParameterSelector,
               deque:QtWidgets.QComboBox,
               OrderedDict:CustomReferenceAndLayersParameterSelector,
               HierarchicalSnapParameters:OrderedRecursiveSnapWidget,
               dict:AuxLayerSelector,
               bool: QtWidgets.QCheckBox}
    GETTERS = {QtWidgets.QLineEdit: "text",
               QtWidgets.QSpinBox: "value",
               QtWidgets.QDoubleSpinBox: "value",
               CustomSnaperParameterSelector: "getParameters",
               CustomTableSelector: "getSelectedNodes",
               QtWidgets.QComboBox:"currentText",
               CustomReferenceAndLayersParameterSelector:"getParameters",
               OrderedRecursiveSnapWidget:"getHierarchicalSnapDict",
               AuxLayerSelector:"getParameters",
               QtWidgets.QCheckBox: "isChecked"}
    SETTERS = {QtWidgets.QLineEdit: "setText",
               QtWidgets.QSpinBox: "setValue",
               QtWidgets.QDoubleSpinBox: "setValue",
               CustomSnaperParameterSelector: "setInitialState",
               CustomReferenceAndLayersParameterSelector: "setInitialState",
               OrderedRecursiveSnapWidget:"setInitialState",
               CustomTableSelector: "setInitialState",
               AuxLayerSelector: "setInitialState",
               QtWidgets.QComboBox:"addItems",
               QtWidgets.QCheckBox: "setChecked"}
    VALIDATORS = {QtWidgets.QLineEdit: lambda x: bool(len(x)),
                  QtWidgets.QSpinBox: lambda x: True,
                  QtWidgets.QDoubleSpinBox: lambda x: True,
                  CustomSnaperParameterSelector: lambda x: True,
                  CustomReferenceAndLayersParameterSelector: lambda x: True,
                  CustomTableSelector: lambda x: True,
                  HierarchicalSnapParameters: lambda x: True,
                  AuxLayerSelector: lambda x: True,
                  QtWidgets.QComboBox: lambda x: True,
                  QtWidgets.QCheckBox: lambda x: True}

    def __init__(self, parent, options, required=None, title=None, restoreOverride = True, assignedParameters = {}):
        """
        Constructor
        """
        super(ProcessParametersDialog, self).__init__(parent)
        self.restoreOverride = restoreOverride
        if self.restoreOverride:
            QApplication.restoreOverrideCursor()
        self.__widgets, self.__values = dict(), dict()
        if title:
            self.setWindowTitle(title)
        self.required = required or list()
        if len(options) == 1:
            self.required.append(list(options.keys())[0])
        self.setItems(options) 
        
    def setItems(self, options):
        _firstWidget = None
        layout = QtWidgets.QGridLayout()
        rowCount = 0
        for k, v in options.items():
            if isinstance(v, list):
                if len(v)> 0 and isinstance(v[0], dict) == False:
                    v = [str(x) for x in v]
            label = QtWidgets.QLabel(beautifyText(k))
            widget = self.WIDGETS[type(v)]()
            self.setWidgetParameters(widget, v, selectedDictList)
            _firstWidget = self.addToLayout(k, label, layout, widget, rowCount, _firstWidget)
            rowCount += 1
        self.setGuiLayout(_firstWidget, rowCount)
    
    def setWidgetParameters(self, widget, v, selectedDictList)
        if self.WIDGETS[type(v)] == QtWidgets.QDoubleSpinBox:
            widget.setDecimals(20)
            widget.setMaximum(sys.float_info.max)
            widget.setMinimum(sys.float_info.min)
            if k in selectedDictList:
                getattr(widget, self.SETTERS[type(widget)])(selectedDictList[k])
            else:
                getattr(widget, self.SETTERS[type(widget)])(v)
        elif self.WIDGETS[type(v)] == QtWidgets.QSpinBox:
            widget.setMaximum(1000000)
            widget.setMinimum(-1000000)
            if k in selectedDictList:
                getattr(widget, self.SETTERS[type(widget)])(selectedDictList[k])
            else:
                getattr(widget, self.SETTERS[type(widget)])(v)
        
        elif self.WIDGETS[type(v)] == CustomTableSelector:
            widget.setTitle(self.tr('Select classes'))
            headerList = [self.tr('Category'), self.tr('Layer Name'), self.tr('Geometry\nColumn'), self.tr('Geometry\nType'), self.tr('Layer\nType')]
            widget.setHeaders(headerList)
            selectedList = assignedParameters[k] if k in assignedParameters else []
            getattr(widget, self.SETTERS[type(widget)])(v, unique=True, selectedDictList = selectedList)

        elif self.WIDGETS[type(v)] == CustomSnaperParameterSelector:
            getattr(widget, self.SETTERS[type(widget)])(v[0], v[1], unique=True)
            widget.setTitle(self.tr('Select layers to be snapped'))

        elif self.WIDGETS[type(v)] == CustomReferenceAndLayersParameterSelector:
            widget.setTitle(self.tr('Select layers'))
            headerList = [self.tr('Category'), self.tr('Layer Name'), self.tr('Geometry\nColumn'), self.tr('Geometry\nType'), self.tr('Layer\nType')]
            widget.customTableSelectorWidget.setHeaders(headerList)
            getattr(widget, self.SETTERS[type(widget)])(v, unique=True)

        elif self.WIDGETS[type(v)] == OrderedRecursiveSnapWidget:
            getattr(widget, self.SETTERS[type(widget)])([v.values])

        else:
            getattr(widget, self.SETTERS[type(widget)])(v)
    
    def addToLayout(self, k, label, layout, widget, rowCount, _firstWidget):
        if k in self.required:
            label.setStyleSheet("color: red;")
        self.__widgets[k] = (label, widget)
        layout.addWidget(label, rowCount, 0)
        layout.addWidget(widget, rowCount, 1)
        if _firstWidget is None:
            _firstWidget = widget
        return _firstWidget

    def setGuiLayout(self, _firstWidget, rowCount):
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QtWidgets.QFrame.Shape(0))  # no frame
        w = QtWidgets.QWidget()
        w.setLayout(formLayout)
        scrollArea.setWidget(w)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(scrollArea)
        layout.addWidget(buttons, rowCount+1, 1)
        self.setLayout(layout)

        if _firstWidget:
            _firstWidget.setFocus()

    def accept(self):
        """
        Sets the parameters and closes the dialog
        """
        for k, (label, widget) in self.widgets.items():
            value = getattr(widget, self.GETTERS[type(widget)])()
            self.__values[k] = value

        for k in self.required:
            value = self.values[k]
            label, widget = self.widgets[k]
            if not self.VALIDATORS[type(widget)](value) and widget.isVisible():
                widget.setFocus()
                return
        if self.restoreOverride:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        return super(ProcessParametersDialog, self).accept()

    @property
    def widgets(self):
        """
        Gets the widgets
        """
        return self.__widgets

    @property
    def values(self):
        """
        Gets the values
        """
        return self.__values


def beautifyText(camelCasedText):
    """
    Makes the text more beautiful
    """
    rval = ""
    for i, ch in enumerate(camelCasedText):
        if i == 0:
            ch = ch.upper()
        elif ch.isupper():
            ch = " " + ch
        rval += ch
    return rval