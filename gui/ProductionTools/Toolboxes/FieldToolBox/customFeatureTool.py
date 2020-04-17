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
from qgis.utils import iface
from qgis.core import QgsProject
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtGui import QColor, QPalette
from qgis.PyQt.QtWidgets import (QWidget,
                                 QPushButton,
                                 QDockWidget,
                                 QVBoxLayout,
                                 QScrollArea,
                                 QSpacerItem,
                                 QSizePolicy)

from DsgTools.core.Utils.utils import Utils
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonSetupWidget import ButtonSetupWidget
from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    # tool mode codes
    Extract, Reclassify = range(2)
    ActiveLayer, AllLayers = range(100, 102)

    def __init__(self, parent=None, setups=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget that 'contains' this tool.
        :param setups: (list-of-dict) a list of states for CustomButtonSetup
                       objects to be set to the GUI.
        """
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
        self._setups = dict()
        self._order = dict()
        self._shortcuts = dict()
        self._qgisActions = Utils().allQgisActions()
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
                                "show" if x else "hide")())
        self.toolBehaviourSwitch.stateChanged.connect(self.toolModeChanged)
        self.tabWidget.setTabPosition(self.tabWidget.West)
        self.bFilterLineEdit.returnPressed.connect(self.createResearchTab)

    def fillSetupComboBox(self):
        """
        Fills profiles' combo boxes with available setup items.
        """
        self.setupComboBox.clear()
        self.setupComboBox.addItem(self.tr("Select a buttons profile..."))
        self.setupComboBox.addItems(self.buttonSetupNames("asc"))

    def setButtonSetups(self, setups):
        """
        Replaces/defines current setup associated to this GUI.
        :param setups: (list-of-dict) a list of states for CustomButtonSetup
                         objects to be set to the GUI.
        """
        for s in self._setup:
            del self._setups[s]
        for p in setups:
            s = CustomButtonSetup()
            s.setState(p)
            self._setups[s.name()] = s
        self.fillSetupComboBox()

    def buttonSetups(self, order=None):
        """
        Retrieves current available button profiles (setups) names. 
        :return: (list-of-CustomFeatureSetup) available profiles names.
        """
        return {
            "asc": lambda: sorted(self._setups.values(),
                                    key=lambda x: x.name()),
            "desc": lambda: sorted(self._setups.values(),
                                    key=lambda x: x.name(),
                                    reverse=True),
            None: lambda: list(self._setups.values())
        }[order]()

    def buttonSetupNames(self, order=None):
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
        w.setObjectName("buttonWidget") # to make it easier to find
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
        self.setTabButtonsActive(self.tabWidget.count() - 1)

    def resetButtonWidgets(self):
        """
        Button widgets are created eveytime a tab is created. In order to not
        waste too much memory on non-used widgets, they'd be removed 
        """
        self.currentButtonSetup().clearWidgets()

    def restoreShortcuts(self):
        """
        Dynamic shortcutting overrides defined shortcuts. This method restore
        original shortcuts to all buttons from current setup.
        """
        for setup, shortcuts in self._shortcuts.items():
            for b, s in shortcuts.items():
                self.buttonSetup(setup).button(b).setShortcut(s)
        # after that registered buttons may be cleared
        self._shortcuts = dict()

    def allocateDynamicShortcuts(self):
        """
        Allocates dynamic shortcuts (restricted to 1-9 keys) to current tab's
        buttons.
        """
        # first registrate current button's shortcuts
        self._shortcuts[self.currentButtonSetupName()] = dict()
        d = self._shortcuts[self.currentButtonSetupName()]
        for i, b in enumerate(self.getButtonsFromTab(self.tabWidget.currentIndex())):
            if i == 9:
                break
            d[b.name()] = b.shortcut()
            b.setShortcut(str(i + 1))

    def getButtonsFromTab(self, tabIdx):
        """
        Gets all registered buttons on a given tab.
        :param tabIdx: (int) targeted tab index.
        :return: (list-of-CustomFeatureButton) registered buttons on tab.
        """
        bl = list()
        s = self.currentButtonSetup()
        w = self.tabWidget.widget(tabIdx)
        if w is not None:
            for c in w.children():
                if "viewport" in c.objectName().lower():
                    for cc in c.children():
                        if cc.objectName() == "buttonWidget":
                            l = cc.layout()
                            for i in range(l.count()):
                                b = l.itemAt(i).widget()
                                if b is None:
                                    continue
                                bl.append(s.button(b.text().rsplit(" [")[0]))
                            break
                    break
        return bl

    @pyqtSlot(int, name="on_tabWidget_currentChanged")
    def setTabButtonsActive(self, idx):
        """
        Defines current tab buttons as active (all others are disabled).
        :param idx: (int) tab index set as active.
        """
        s = self.currentButtonSetup()
        if s is None:
            return
        s.setEnabled(False)
        for b in self.getButtonsFromTab(idx):
            b.setEnabled(True)
        self.restoreShortcuts()
        if s.dynamicShortcut():
            self.allocateDynamicShortcuts()

    @pyqtSlot(int, name="on_setupComboBox_currentIndexChanged")
    def setCurrentButtonSetup(self, setup=None):
        """
        Sets GUI to a new setup.
        :param setup: (str) button setup name.
        :*obs: param setup may be an int if this method is called from signal
               triggerring.
        """
        self.clearTabs()
        self.bFilterLineEdit.setText("")
        for s in self.buttonSetups():
            if s is not None and s.isEnabled():
                s.setEnabled(False)
        isSetup = self.setupComboBox.currentIndex() != 0
        self.editSetupPushButton.setEnabled(isSetup)
        self.removePushButton.setEnabled(isSetup)
        self.bFilterLineEdit.setEnabled(isSetup)
        if isinstance(setup, str) and setup in self.buttonSetupNames():
            self.setupComboBox.setCurrentText(self.currentButtonSetupName())
        if isSetup:
            s = self.currentButtonSetup()
            s.setButtonsCheckable(
                bool(self.toolMode() ^ 1))
            self.resetButtonWidgets()
            for b in s.buttons():
                b.setCallback(self.toolCallback)
                b.setShortcutCallback(self.shortcutActivated)
        self.createTabs()
        # this needs to be after tab creation
        self.setTabButtonsActive(0)

    @pyqtSlot(bool, name="on_editSetupPushButton_clicked")
    def editCurrentSetup(self):
        """
        Opens button setup configuration GUI to edit current button setup.
        """
        setup = self.currentButtonSetup()
        # before editing current, check restore any potential modified shortcut
        self.restoreShortcuts()
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
                while newSetup.name() in self.buttonSetupNames():
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
        if setup.name() in self.buttonSetupNames():
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
            if baseName in self.buttonSetupNames():
                i = 0
                setups = self.buttonSetupNames()
                while s.name() in setups:
                    i += 1
                    s.setName("{0} ({1})".format(baseName, i))
            self._order[s.name()] = dlg.buttonsOrder()
            self.addButtonSetup(s)

    def layerMode(self):
        """
        Reads from GUI which mode did the user set for layer selection: either
        reclassify selected features from all compatible loaded layers (geom
        type) on canvas or just the active layer.
        :return: (int) layer mode code.
        """
        return self.ActiveLayer if self.layerSelectionSwitch.currentState() == 0\
            else self.AllLayers

    def toolMode(self):
        """
        Identifies current set tool mode, whether it's either feature
        extraction or layer and field update (reclassification).
        :return: (int) tool mode code.
        """
        return self.toolBehaviourSwitch.currentState()

    def setToolMode(self, mode):
        """
        Defines whether tool will perform feature extraction or layer and field
        update (reclassification). Method defaults to feature extraction.
        :param mode: (int) tool mode code.
        """
        mode = mode if mode in (0, 1) else self.Extract
        self.toolBehaviourSwitch.setState(mode)

    @pyqtSlot(int)
    def toolModeChanged(self, newMode):
        """
        A slot to handle tool mode updates.
        :param newMode: (int) new mode code.
        """
        for s in self.buttonSetups():
            s.setButtonsCheckable(bool(newMode ^ 1))

    def featureExtractionButton(self):
        """
        Retrieves currently checked button to be used as feature extraction
        button.
        :return: (CustomFeatureButton) checked button.
        """
        s = self.currentButtonSetup()
        return s.checkedButton() if s is not None else None

    def featuresToBeReclassified(self, b):
        """
        Identifies all selected features from layers to be reclassified. It
        looks for tool mode for layer search, and retrieves either currently
        active layer's selected features or all selected features from all
        layers. It is important to notice QGIS behaviour: all layers will only
        consider visible layers (checked on layer list).
        :param b: (CustomFeatureButton) button to be used for reclassification.
        :return: (dict) a map from layer to its features for reclassification.
        """
        rMap = dict()
        if b is not None and b.checkLayer():
            geomType = b.vectorLayer().geometryType()
            if self.layerMode() == self.AllLayers:
                layers = iface.mapCanvas().layers()
            else:
                l = iface.activeLayer()
                layers = [] if l is None else [l]
            for l in layers:
                # im not sure whether it's a recent modification, but map layers
                # are hashable
                if l.geometryType() == geomType:
                    feats = l.selectedFeatures()
                    if feats:
                        rMap[l] = feats
        return rMap

    def createFeature(self, fields, geom, attributeMap, layerDefs, 
                        coordTransformer=None):
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

    def shortcutActivated(self):
        """
        Shortcut may be activated whilst tool is in extract mode and in that
        mode, callbacks from action triggering is disconnected whenever the
        button is unchecked. This method is connected to shortcut activation
        event in order to make sure the requested button is properly set.
        """
        if self.toolMode() == self.Extract:
            sh = self.sender()
            sid = sh.id()
            s = self.currentButtonSetup()
            for b in s.buttons():
                if b.shortcutId() == sid and not b.isChecked():
                    s.toggleButton(b, True)
                    b.action().trigger()
                    return

    def toolCallback(self):
        """
        Method that channels the incoming requests from setup buttons to the
        correct action to be executed. Method is used as callback for every
        registered button.
        """
        # callback is set from action triggering, hence it is the sender
        a = self.sender()
        s = self.currentButtonSetup()
        if a is None or s is None:
            return
        for button in s.buttons():
            if button.action().text() == a.text():
                break
        else:
            # if button is not identified, somehow call was made from none of
            # current setup's buttons
            return
        if button.checkLayer():
            vl = button.vectorLayer()
            if not vl.isEditable():
                vl.startEditing()
            iface.setActiveLayer(vl)
        if self.toolMode() == self.Extract:
            if not button.isChecked():
                s.toggleButton(button, True)
            print("Extracting feature for button {0}, using tool {1}"\
                    .format(button.name(), button.digitizingTool()))
        else:
            reclassify = self.featuresToBeReclassified(button)
            msg = ""
            for l, fl in reclassify.items():
                msg += "{0} ({1} features)\n".format(l.name(), len(fl))
            print("Reclassifying features for button {0} ({1})"\
                    .format(button.name(), msg))
            # create the custom form and opt for showing it or not to user
        self.setMapTool(button)

    def setMapTool(self, button):
        """
        Whenever a button is called it sets current map tool for feature
        extraction as defined in its properties, or sets the DSGTools: Generic
        Selector tool, if reclassification mode is set.
        """
        if self.toolMode() == self.Extract:
            tool = button.digitizingTool()
            if tool == "default":
                ts = [
                    self.tr("Add Line Feature"),
                    self.tr("Add Polygon Feature"),
                    self.tr("Add Point Feature")
                ]
                for t in ts:
                    if t in self._qgisActions:
                        toolName = t
                        break
            elif tool == "circle":
                toolName = self.tr("Add Circle from 2 Points")
            else:
                toolName = button.supportedTools()[tool]
        else:
            toolName = self.tr("DSGTools: Generic Selector")
        # incomplete i18n will raise errors in here... i don't know any other
        # way of how to set map tools from their names as of now, though...
        # not sure about this...
        iface.mapCanvas().unsetMapTool(iface.mapCanvas().mapTool())
        self._qgisActions[toolName].trigger()

    def toolState(self):
        """
        Retrieves a map with all parameters that indicates current tool setup.
        :return: (dict) a map to all parameters for current tool state.
        """
        return dict()

    def setToolState(self, state):
        """
        Sets tool to a given state.
        :param state: (dict) a map to all parameters for current tool state.
        """
        pass

    def saveStateToProject(self):
        """
        Saves current tool state to the QGIS project.
        """
        pass

    def restoreStateFromProject(self):
        """
        Restores current tool state from project variable state.
        """
        pass

    def unload(self):
        """
        Clears all components.
        """
        pass