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
import sys
from collections import deque, OrderedDict
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QCursor, QMenu
from DsgTools.CustomWidgets.customTableSelector import CustomTableSelector
from DsgTools.CustomWidgets.customSnaperParameterSelector import CustomSnaperParameterSelector

class ProcessParametersDialog(QtGui.QDialog):
    WIDGETS = {str: QtGui.QLineEdit,
               unicode: QtGui.QLineEdit,
               int: QtGui.QSpinBox,
               float: QtGui.QDoubleSpinBox,
               list: CustomTableSelector,
               tuple: CustomSnaperParameterSelector,
               deque:QtGui.QComboBox,
               bool: QtGui.QCheckBox}
    GETTERS = {QtGui.QLineEdit: "text",
               QtGui.QSpinBox: "value",
               QtGui.QDoubleSpinBox: "value",
               CustomSnaperParameterSelector: "getParameters",
               CustomTableSelector: "getSelectedNodes",
               QtGui.QComboBox:"currentText",
               QtGui.QCheckBox: "isChecked"}
    SETTERS = {QtGui.QLineEdit: "setText",
               QtGui.QSpinBox: "setValue",
               QtGui.QDoubleSpinBox: "setValue",
               CustomSnaperParameterSelector: "setInitialState",
               CustomTableSelector: "setInitialState",
               QtGui.QComboBox:"addItems",
               QtGui.QCheckBox: "setChecked"}
    VALIDATORS = {QtGui.QLineEdit: lambda x: bool(len(x)),
                  QtGui.QSpinBox: lambda x: True,
                  QtGui.QDoubleSpinBox: lambda x: True,
                  CustomSnaperParameterSelector: lambda x: True,
                  CustomTableSelector: lambda x: True,
                  QtGui.QComboBox: lambda x: True,
                  QtGui.QCheckBox: lambda x: True}

    def __init__(self, parent, options, required=None, title=None):
        """
        Constructor
        """
        super(ProcessParametersDialog, self).__init__(parent)
        QApplication.restoreOverrideCursor()
        self.__widgets = dict()
        self.__values = dict()

        if title:
            self.setWindowTitle(title)

        self.required = required or list()
        if len(options) == 1:
            self.required.append(options.keys()[0])

        _firstWidget = None
        formLayout = QtGui.QFormLayout()
        for k, v in options.iteritems():
            if isinstance(v, list):
                if len(v)> 0 and isinstance(v[0], dict) == False:
                    v = [str(x) for x in v]

            label = QtGui.QLabel(beautifyText(k))
            widget = self.WIDGETS[type(v)]()
            if self.WIDGETS[type(v)] == QtGui.QDoubleSpinBox:
                widget.setDecimals(5)
                widget.setMaximum(sys.float_info.max)
                widget.setMinimum(sys.float_info.min)
            if self.WIDGETS[type(v)] == QtGui.QSpinBox:
                widget.setMaximum(1000000)
                widget.setMinimum(-1000000)
            
            if self.WIDGETS[type(v)] == CustomTableSelector:
                widget.setTitle(self.tr('Select classes'))
                headerList = [self.tr('Category'), self.tr('Layer Name'), self.tr('Geometry\nColumn'), self.tr('Geometry\nType'), self.tr('Layer\nType')]
                widget.setHeaders(headerList)
                getattr(widget, self.SETTERS[type(widget)])(v, unique=True)
            if self.WIDGETS[type(v)] == CustomSnaperParameterSelector:
                getattr(widget, self.SETTERS[type(widget)])(v[0], v[1], unique=True)
                widget.setTitle(self.tr('Select layers to be snapped'))
            else:
                getattr(widget, self.SETTERS[type(widget)])(v)

            if k in self.required:
                label.setStyleSheet("color: red;")

            self.__widgets[k] = (label, widget)
            formLayout.addRow(label, widget)

            if _firstWidget is None:
                _firstWidget = widget

        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QtGui.QFrame.Shape(0))  # no frame
        w = QtGui.QWidget()
        w.setLayout(formLayout)
        scrollArea.setWidget(w)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QtGui.QGridLayout()
        layout.addWidget(scrollArea)
        layout.addWidget(buttons)
        self.setLayout(layout)

        _firstWidget.setFocus()

    def accept(self):
        """
        Sets the parameters and closes the dialog
        """
        for k, (label, widget) in self.widgets.iteritems():
            value = getattr(widget, self.GETTERS[type(widget)])()
            self.__values[k] = value

        for k in self.required:
            value = self.values[k]
            label, widget = self.widgets[k]
            if not self.VALIDATORS[type(widget)](value) and widget.isVisible():
                widget.setFocus()
                return
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