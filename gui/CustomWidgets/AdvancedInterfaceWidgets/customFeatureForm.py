# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-23
        git sha              : $Format:%H$
        copyright            : (C) 2018 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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

import os, sys

from qgis.core import Qgis
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QSize, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QLabel,
                                 QDialog,
                                 QSpinBox,
                                 QLineEdit,
                                 QCheckBox,
                                 QGridLayout,
                                 QSpacerItem,
                                 QSizePolicy,
                                 QDoubleSpinBox)
from qgis.PyQt import uic, QtWidgets, QtGui

from DsgTools.core.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureForm.ui'))

class CustomFeatureForm(QDialog, FORM_CLASS):
    """
    Customized form tailor made for reclassification mode of DSGTools: Custom
    Feature Tool Box. This form was copied from `Ferramentas de Produção` and
    modified for the DSGTools plugin.
    """
    def __init__(self, fields, layerMap, attributeMap=None):
        """
        Class constructor.
        :param fields: (QgsFields) set of fields that will be applied to new
                       feature(s).
        :param layerMap: (dict) a map from vector layer to feature list to be
                         reclassified (allocated to another layer).
        :param attributeMap: (dict) a map from attribute name to its
                             (reclassified) value.
        """
        super(CustomFeatureForm, self).__init__()
        self.setupUi(self)
        self.fields = fields
        self.layerMap = layerMap
        self.attributeMap = attributeMap or dict()
        self._layersWidgets = dict()
        self.setupReclassifiedLayers()
        self.widgetsLayout = QGridLayout(self.scrollAreaWidgetContents)
        self._fieldsWidgets = dict()
        self.setupFields()
        self.setWindowTitle(self.tr("DSGTools Feature Reclassification Form"))
        self.messageBar = QgsMessageBar(self)

    def resizeEvent(self, e):
        """
        Just make sure if any alert box is being displayed, it matches the
        dialog size. Method reimplementation.
        :param e: (QResizeEvent) resize event related to this widget resizing.
        """
        self.messageBar.resize(
            QSize(
                self.geometry().size().width(),
                40 # this felt nicer than the original height (30)
            )
        )

    def setupReclassifiedLayers(self):
        """
        Fills GUI with the data for reclassified data. Dialog should allow user
        to choose whether he wants to reclassify all identified layers or just
        part of it.
        """
        layout = self.vLayout
        for l, fl in self.layerMap.items():
            cb = QCheckBox()
            size = len(fl)
            fCount = self.tr("features") if size > 1 else self.tr("feature")
            cb.setText("{0} ({1} {2})".format(l.name(), size, fCount))
            cb.setChecked(True)
            # just to avoid reading the layout when reading the form
            self._layersWidgets[l.name()] = cb
            layout.addWidget(cb)

    def setupFields(self):
        """
        Setups up all fields and fill up with available data on the attribute
        map.
        """
        utils = Utils()
        row = 0 # in case no fields are provided
        for row, f in enumerate(self.fields):
            fName = f.name()
            fMap = self.attributeMap[fName] if fName in self.attributeMap \
                        else None
            if fName in self.attributeMap:
                fMap = self.attributeMap[fName]
                if fMap["ignored"]:
                    w = QLineEdit()
                    w.setText(self.tr("Field is set to be ignored"))
                    value = None
                    enabled = False
                else:
                    value = fMap["value"]
                    enabled = fMap["editable"]
                if fMap["isPk"]:
                    # visually identify primary key attributes
                    text = '<p>{0} <img src=":/plugins/DsgTools/icons/key.png" '\
                           'width="16" height="16"></p>'.format(fName)
                else:
                    text = fName
            else:
                value = None
                enabled = True
                text = fName
            if fName in self.attributeMap and self.attributeMap[fName]["ignored"]:
                pass
            elif utils.fieldIsBool(f):
                w = QCheckBox()
                w.setChecked(False if value is None else value)
            elif utils.fieldIsFloat(f):
                w = QDoubleSpinBox()
                w.setValue(0 if value is None else value)
            elif utils.fieldIsInt(f):
                w = QSpinBox()
                w.setValue(0 if value is None else value)
            else:
                w = QLineEdit()
                w.setText("" if value is None else value)
            w.setEnabled(enabled)
            # also to make easier to read data
            self._fieldsWidgets[fName] = w
            label = QLabel(text)
            label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.widgetsLayout.addWidget(label, row, 0)
            self.widgetsLayout.addWidget(w, row, 1)
        self.widgetsLayout.addItem(
            QSpacerItem(
                20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding
            ), row + 1, 1, 1, 2
        ) # row, col, rowSpan, colSpan

    def updateAttributeMap(self):
        """
        Reads all filled data and updated attribute map with such values.
        """
        for fName, w in self._fieldsWidgets.items():
            if not fName in self.attributeMap:
                self.attributeMap[fName] = dict()
                self.attributeMap[fName]["ignored"] = False
                self.attributeMap[fName]["editable"] = True
            if self.attributeMap[fName]["ignored"]:
                continue
            w = self._fieldsWidgets[fName]
            if isinstance(w, QSpinBox) or isinstance(w, QDoubleSpinBox):
                self.attributeMap[fName]["value"] = w.value()
            elif isinstance(w, QCheckBox):
                self.attributeMap[fName]["value"] = w.isChecked()
            else:
                self.attributeMap[fName]["value"] = w.text()

    def readSelectedLayers(self):
        """
        Applies a filter over the layer/feature list map based on user
        selection.
        :return: (dict) filtered layer-feature list map.
        """
        filtered = dict()
        for l, fl in self.layerMap.items():
            if self._layersWidgets[l.name()].isChecked():
                filtered[l] = fl
        return filtered

    def readFieldMap(self):
        """
        Reads filled data into the form and sets it to a map from field name to
        field value to be set. Only fields allowed to be reclassified shall be
        exported in this method.
        :return: (dict) a map from field name to its output value.
        """
        fMap = dict()
        for fName, w in self._fieldsWidgets.items():
            if not fName in self.attributeMap:
                continue
            w = self._fieldsWidgets[fName]
            if isinstance(w, QSpinBox) or isinstance(w, QDoubleSpinBox):
                fMap[fName] = w.value()
            elif isinstance(w, QCheckBox):
                fMap[fName] = w.isChecked()
            else:
                fMap[fName] = w.text()
        return fMap

    @pyqtSlot()
    def on_okPushButton_clicked(self):
        """
        Verifies if at least one layer is selected and either warn user to
        select one, or closes with status 1 ("OK").
        """
        if len(self.readSelectedLayers()) > 0:
            self.updateAttributeMap()
            self.done(1)
        else:
            self.messageBar.pushMessage(
                self.tr('Invalid layer selection'),
                self.tr("select at least one layer for reclassification!"),
                level=Qgis.Warning,
                duration=5
            )
