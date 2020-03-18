# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2020-01-17
        git sha              : $Format:%H$
        copyright            : (C) 2020 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtGui import QColor, QPalette
from qgis.PyQt.QtWidgets import (QWidget,
                                 QPushButton,
                                 QDockWidget,
                                 QVBoxLayout,
                                 QScrollArea,
                                 QSpacerItem,
                                 QSizePolicy)

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonSetupWidget import ButtonSetupWidget
from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    def __init__(self, parent=None, setups=None):
        """
        Class constructor.
        :param parent: (QtWidgets.*) any widget that 'contains' this tool.
        :param setups: (list-of-dict) a list of states for CustomButtonSetup
                       objects to be set to the GUI.
        """
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
        self._setups = dict()
        self._order = dict()
        if setups:
            self.setButtonSetups(setups)
        self.fillSetupComboBox()
        self.layerSelectionSwitch.setStateAName(self.tr("Active layer"))
        self.layerSelectionSwitch.setStateBName(self.tr("All layers"))
        self.layerSelectionSwitch.hide()
        self.toolBehaviourSwitch.setStateAName(self.tr("Feature extraction"))
        self.toolBehaviourSwitch.setStateBName(self.tr("Reclassify"))
        self.toolBehaviourSwitch.stateChanged.connect(
            lambda x: getattr(self.layerSelectionSwitch,
                                "show" if x else "hide")()
        )
        self.tabWidget.setTabPosition(self.tabWidget.West)
        self.bFilterLineEdit.returnPressed.connect(self.createResearchTab)

    def fillSetupComboBox(self):
        """
        Fills profiles' combo boxes with available setup items.
        """
        self.setupComboBox.clear()
        self.setupComboBox.addItem(self.tr("Select a buttons profile..."))
        self.setupComboBox.addItems(list(self._setups.keys()))

    def setButtonSetups(self, setups):
        """
        Replaces/defines current setup associated to this GUI.
        :param setups: (list-of-dict) a list of states for CustomButtonSetup
                         objects to be set to the GUI.
        """
        self.setupComboBox.clear()
        self.setupComboBox.addItem(self.tr("Select a button profile..."))
        for s in self._setup:
            del self._setups[s]
        for p in setups:
            s = CustomButtonSetup()
            s.setState(p)
            self._setups[s.name()] = s
        self.setupComboBox.addItems(self.buttonSetups("asc"))

    def buttonSetups(self, order=None):
        """
        Retrieves current available button profiles (setups) names. 
        :return: (list-of-str) available profiles names.
        """
        return {
            "asc": lambda: sorted(self._setups.keys()),
            "desc": lambda: sorted(self._setups.keys(), reverse=True),
            None: lambda: list(self._setups.keys())
        }[order]()

    def buttonSetup(self, profile):
        """
        Retrieves a button profile object from its name. 
        :param profile: (str) profile to be retrieved.
        :return: (CustomButtonSetup) requested profile.
        """
        return self._setups[profile] if profile in self._setups else None

    def currentButtonSetupName(self):
        """
        Retrieves current active button profile name.
        :return: (str) current profile's name.
        """
        if self.setupComboBox.currentIndex() == 0:
            return ""
        return self.setupComboBox.currentText()

    def currentButtonSetup(self):
        """
        Retrieves current active button profile.
        :return: (CustomButtonSetup) requested profile.
        """
        return self.buttonSetup(self.currentButtonSetupName())

    def allButtons(self):
        """
        Retrieves all buttons from current buttons setup.
        :return: (list-of-CustomFeatureButton) all buttons from current setup.
        """
        s = self.currentButtonSetup()
        return s.buttons() if s is not None else []

    def clearTabs(self):
        """
        Clears all tabs created for the buttons.
        """
        self.tabWidget.clear()

    def newTab(self, tabTitle, buttonList=None):
        """
        Adds a new tab to tab widget.
        :param tabTitle: (str) tab title text.
        :param buttonList: (list-of-CustomFeatureButton) buttons to be added to
                           the new tab.
        """
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        w = QWidget()
        layout = QVBoxLayout()
        self.tabWidget.addTab(scroll, tabTitle)
        if buttonList is not None:
            # buttons must respect order defined by user on setup GUI
            order = self._order[self.currentButtonSetupName()]
            buttonList = sorted(buttonList, key=lambda i: order[i.name()])
            for row, b in enumerate(buttonList):
                layout.insertWidget(row, b.newWidget())
            layout.addItem(
                QSpacerItem(
                    20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding
                )
            )
        w.setLayout(layout)
        scroll.setWidget(w)

    def createTabs(self):
        """
        Creates and populates all tabs for current button profile.
        """
        s = self.currentButtonSetup()
        if s is None:
            return
        groups = s.groupButtons()
        for cat in s.categories():
            self.newTab(cat or self.tr("No category"), groups[cat])

    def readButtonKeywords(self):
        """
        Reads typed in keywords from GUI.
        :return: (set-of-str) all typed in keywords.
        """
        words = self.bFilterLineEdit.text().strip()
        return set([w for w in words.split(" ") if w.strip()])

    def checkKeywordSet(self, kws):
        """
        Matches buttons to all given keywords.
        :param kws: (set-of-str) keywords to be matched.
        :return: (list-of-CustomFeatureButton) all matched buttons.
        """
        return self.currentButtonSetup().checkKeywordSet(kws)

    @pyqtSlot()
    def createResearchTab(self):
        """
        Creates a tab for researched buttons. If research tab is already
        created, it is cleared and repopulated.
        """
        kws = self.readButtonKeywords()
        for tab in range(self.tabWidget.count(), 0, -1):
            if self.tr("Searched buttons") in self.tabWidget.tabText(tab):
                self.tabWidget.removeTab(tab)
                break
        buttons = self.checkKeywordSet(kws) if kws else self.allButtons()
        txt = self.tr("Searched buttons ({0})").format(len(buttons))
        self.newTab(txt, buttons)
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    @pyqtSlot(int, name="on_setupComboBox_currentIndexChanged")
    def setCurrentButtonSetup(self, profile=None):
        """
        Sets GUI to a new profile.
        """
        self.clearTabs()
        self.bFilterLineEdit.setText()
        isSetup = self.setupComboBox.currentIndex() != 0
        self.editSetupPushButton.setEnabled(isSetup)
        self.removePushButton.setEnabled(isSetup)
        self.bFilterLineEdit.setEnabled(isSetup)
        if isinstance(profile, str) and profile in self.buttonSetups():
            self.setupComboBox.setCurrentText(self.currentButtonSetupName())
        self.createTabs()

    @pyqtSlot(bool, name="on_editSetupPushButton_clicked")
    def editCurrentSetup(self):
        """
        Opens button setup configuration GUI to edit current button setup.
        """
        setup = self.currentButtonSetup()
        dlg = ButtonSetupWidget()
        dlg.setSetup(setup)
        ret = dlg.exec_()
        if ret:
            newSetup = dlg.readSetup()
            newName = newSetup.name()
            if newName != setup.name():
                i = 0
                oldName = setup.name()
                del self._order[oldName]
                while newSetup.name() in self.buttonSetups():
                    i += 1
                    newSetup.setName("{0} ({1})".format(newName, i))
                newName = newSetup.name()
                self._setups[newName] = self._setups.pop(oldName)
                idx = self.setupComboBox.currentIndex()
                self.setupComboBox.setItemText(idx, newSetup.name())
            self._order[newName] = dlg.buttonsOrder()
            self.setupComboBox.setItemData(
                self.setupComboBox.currentIndex(),
                newSetup.description(),
                Qt.ToolTipRole
            )
            setup.setState(newSetup.state())
            self.setCurrentButtonSetup(setup)

    def addButtonSetup(self, setup):
        """
        Adds a setup to the available setups. Newly added profile will be set
        as active.
        :param setup: (CustomButtonSetup) button setup to be added.
        """
        if setup.name() in self.buttonSetups():
            # raise error message
            return
        self._setups[setup.name()] = setup
        self.setupComboBox.addItem(setup.name())
        self.setupComboBox.setItemData(
            self.setupComboBox.findText(setup.name()),
            setup.description(),
            Qt.ToolTipRole
        )
        self.setupComboBox.setCurrentText(setup.name())

    @pyqtSlot()
    def on_addPushButton_clicked(self):
        """
        Adds a configured setup to the available profiles.
        """
        dlg = ButtonSetupWidget()
        ret = dlg.exec_()
        if ret:
            s = dlg.readSetup()
            baseName = s.name()
            if baseName in self.buttonSetups():
                i = 0
                setups = self.buttonSetups()
                while s.name() in setups:
                    i += 1
                    s.setName("{0} ({1})".format(baseName, i))
            self._order[s.name()] = dlg.buttonsOrder()
            self.addButtonSetup(s)

    def createFeature(self, fields, geom, attributeMap, layerDefs, coordTransformer=None):
        """
        Creates a new feature to be added to a layer. These features may be
        pre-set with a collection of attributes.
        :param fields: (QgsFields) all feature's fields.
        :param geom: (QgsGeometry) new feature's geometry.
        :param attributeMap: (dict) a map from field name to its value.
        :param layerDefs: (dict) a map to layer definitions such as geometry
                          type, multipart definition, etc.
        :param coordTransformer: () object for coordinate transformation.
        """
        fh = FeatureHandler()
        gh = GeometryHandler()
        if coordTransformer is not None:
            geom = gh.reprojectWithCoordinateTransformer(geom, coordTransformer)
        return fh.newFeature(geom, fields, attributeMap)

    def reclassifyFeatures(self, featList, prevLayer, newLayer, newAttributeMap):
        """
        Reclassifies a list of feature.
        :param featList: (list-of-QgsFeature) all features to be reclassified.
        :param prevLayer: (QgsVectorLayer) layer to have its reclassified from.
        :param newLayer: (QgsVectorLayer) layer to receive reclassified
                         features.
        :param newAttributeMap: (dict) a map to new features' attribute values.
        :return: (list-of-QgsFeature) all reclassified features.
        """
        fh = FeatureHandler()
        lh = LayerHandler()
        defs = lh.getDestinationParameters(newLayer)
        transformer = lh.getCoordinateTransformer(prevLayer, newLayer)
        removeFeats = list()
        addFeats = set()
        fields = newLayer.fields()
        for f in featList:
            addFeats.add(
                self.createFeature(
                    fields, f.geometry(), newAttributeMap, defs, transformer)
            )
            removeFeats.append(f.id())
        prevLayer.startEditing()
        prevLayer.deleteFeatures(removeFeats)
        prevLayer.updateExtents()
        newLayer.startEditing()
        newLayer.addFeatures(addFeats)
        newLayer.updateExtents()
        return addFeats

    def setActiveMapTool(self, tool):
        """
        Sets a map tool as active on QGIS canvas.
        :param tool: (str) tool's name.
        """
        actions = {
            self.tr("Pan Map"): None,
            self.tr("QGIS default feature extraction tool"): None,
            self.tr("DSGTools: Free Hand Acquisition"): None,
            self.tr("QGIS Circle extraction tool"): None,
            self.tr("DSGTools: Right Degree Angle Digitizing"): None
        }
