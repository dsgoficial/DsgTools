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
import json

from qgis.PyQt import uic
from qgis.utils import iface
from qgis.core import (Qgis,
                       NULL,
                       QgsFeature,
                       QgsProject,
                       QgsVectorLayer,
                       QgsExpressionContextUtils)
from qgis.gui import QgsAttributeEditorContext, QgsAttributeDialog
from qgis.PyQt.QtCore import Qt, QTimer, pyqtSlot
from qgis.PyQt.QtGui import QColor, QPalette
from qgis.PyQt.QtWidgets import (QAction,
                                 QWidget,
                                 QFileDialog,
                                 QPushButton,
                                 QDockWidget,
                                 QVBoxLayout,
                                 QScrollArea,
                                 QSpacerItem,
                                 QSizePolicy)

from DsgTools.core.Utils.utils import Utils, MessageRaiser
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.featureHandler import FeatureHandler
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler
from DsgTools.core.GeometricTools.attributeHandler import AttributeHandler
from DsgTools.gui.ProductionTools.MapTools.Acquisition.polygon import Polygon
from DsgTools.gui.ProductionTools.MapTools.FreeHandTool.models.acquisitionFree import AcquisitionFree
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.buttonSetupWidget import ButtonSetupWidget
from DsgTools.gui.ProductionTools.Toolboxes.CustomFeatureToolBox.customButtonSetup import CustomButtonSetup
from DsgTools.gui.CustomWidgets.AdvancedInterfaceWidgets.customFeatureForm import CustomFeatureForm

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customFeatureTool.ui'))

QGIS_ACTIONS = Utils().allQgisActions()

class CustomFeatureTool(QDockWidget, FORM_CLASS):
    # tool mode codes
    Extract, Reclassify = range(2)
    ActiveLayer, AllLayers = range(100, 102)
    __VERSION = '0.1'

    def __init__(self, parent=None, setups=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget that 'contains' this tool.
        :param setups: (list-of-dict) a list of states for CustomButtonSetup
                       objects to be set to the GUI.
        """
        super(CustomFeatureTool, self).__init__(parent)
        self.setupUi(self)
        self._timer = QTimer(self)
        self._setups = dict()
        self._order = dict()
        self._shortcuts = dict()
        self._enabled = False
        self._featId = None
        # disable tool when a non-digitizing map tool is set
        iface.mapCanvas().mapToolSet.connect(self._mapToolSet)
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
        self.bFilterLineEdit.textEdited.connect(self.createResearchTab)
        self.bFilterLineEdit.returnPressed.connect(self.createResearchTab)
        self.visibilityChanged.connect(self.setToolEnabled)
        # importing multiple button setups is under review and, for now, is
        # going to be HIDDEN for now. If the feature is not requested till next
        # major version update, then it should be wiped from code.
        self.importPushButton.hide()
        self.exportPushButton.hide()
        # a request of integration with other systems: hide edition buttons
        # from the user in order for the DSG activity manager system (SAP) be
        # the only source of input buttons, forcing conformity on its
        # production lines. This should not be the default, but API callable! 
        self._buttonsHidden = False
        project = QgsProject.instance()
        project.writeProject.connect(self.saveStateToProject)
        project.readProject.connect(self.restoreStateFromProject)
        # at first, dock is not initiated (optimize loading time), so calls
        # will not be perceived by toold => manual restoration on init
        self.restoreStateFromProject()

    def clear(self):
        """
        Clears all input data and sets tool to its initial state.
        """
        self.clearTabs()
        while self._setups:
            sName, s = self._setups.popitem()
            self._order.pop(sName, None)
            if s is None:
                continue
            s.setEnabled(False)
            s.__del__() # setups were lingering, needed direct del call
        self.fillSetupComboBox()
        self.setToolMode(self.Extract)
        self.setLayerMode(self.ActiveLayer)
        self.setKeywordSet({})
        self.setZoomLevel(0)

    @pyqtSlot(bool)
    def setToolEnabled(self, enabled):
        """
        Sets tools callbacks and buttons disabled / enabled, regardless of
        current selection. This means shortcuts and all buttons, setups, signal
        emittion and so forth will be blocked / unblocked.
        :param enabled: (bool) whether this dock widget should be enabled.
        """
        for s in self.buttonSetups():
            if s is not None and s.isEnabled():
                s.setEnabled(False)
        for l in QgsProject.instance().mapLayers().values():
            if not isinstance(l, QgsVectorLayer):
                continue
            try:
                l.featureAdded.disconnect(self._registerAddedFeature)
                l.editCommandEnded.disconnect(self._handleAddedFeature)
            except TypeError:
                pass
        if enabled:
            b = self.featureExtractionButton()
            self.setCurrentButtonSetup(self.currentButtonSetup())
            if b is not None:
                self.setMapToolFromButton(b)
                if b.checkLayer():
                    self.setSuppressFormOption(b.vectorLayer(), False)
        else:
            self.setMapTool("pan")
            self.resetSuppressFormOption()
        self._enabled = enabled

    def fillSetupComboBox(self):
        """
        Fills profiles' combo boxes with available setup items.
        """
        self.setupComboBox.clear()
        self.setupComboBox.addItem(self.tr("Select a buttons profile..."))
        self.setupComboBox.addItems(self.buttonSetupNames("asc"))

    def warnReclassified(self, recMap, outLayer):
        """
        Raises warning message to the user that features have been reclassified
        (and logs it).
        :param recMap: (dict) map from layer name to feature count of
                       reclassified feature successfully saved to output layer.
        :param outLayer: (str) layer to have features reclassified to.
        """
        msgItems = list()
        for l, featCount in recMap.items():
            if featCount == 1:
                msgItems.append(self.tr("{0} (1 feature)").format(l))
            else:
                msgItems.append(
                    self.tr("{0} ({1} features)").format(l, featCount))
        total = sum(recMap.values())
        if total > 1:
            title = self.tr("Reclassified features")
        else:
            title = self.tr("Reclassified feature")
        mr = MessageRaiser()
        msg = "{0} to layer {1}".format(", ".join(msgItems), outLayer)
        mr.raiseIfaceMessage(title, msg, Qgis.Success, 5)
        mr.logMessage("{0}: {1}.".format(title, msg), level=Qgis.Success)

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
        self.tabWidget.blockSignals(True)
        self.tabWidget.clear()
        self.tabWidget.blockSignals(False)
        self.setTabButtonsActive(0)

    def currentTab(self):
        """
        Retrieves current displayed tab index.
        :return: (int) current tab index.
        """
        return self.tabWidget.currentIndex()

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

    def setKeywordSet(self, kws):
        """
        Fills a keyword set to the GUI.
        :param kws: (set-of-str) keywords to be set.
        """
        return self.bFilterLineEdit.setText(" ".join(kws))

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
        waste too much memory on non-used widgets, they'd be removed.
        """
        self.currentButtonSetup().clearWidgets()

    def restoreShortcuts(self):
        """
        Dynamic shortcutting overrides defined shortcuts. This method restore
        original shortcuts to all buttons from current setup.
        """
        while self._shortcuts:
            setup, shortcuts = self._shortcuts.popitem()
            for btn, sh in shortcuts.items():
                self.buttonSetup(setup).button(btn).setShortcut(sh)

    def allocateDynamicShortcuts(self):
        """
        Allocates dynamic shortcuts (restricted to 1-9 keys) to current tab's
        buttons.
        """
        currentSetup = self.currentButtonSetupName()
        self._shortcuts[currentSetup] = dict()
        d = self._shortcuts[currentSetup]
        for i, b in enumerate(self.getButtonsFromTab(self.currentTab())):
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
                                bl.append(s.button(b.text().rsplit(" [", 1)[0]\
                                           .replace("&", "")))
                            break
                    break
        return bl

    @pyqtSlot(int, name="on_tabWidget_currentChanged")
    def setTabButtonsActive(self, idx):
        """
        Defines current tab buttons as active (all others are disabled).
        :param idx: (int) tab index set as active.
        """
        self.restoreShortcuts()
        s = self.currentButtonSetup()
        if s is None:
            return
        s.setEnabled(False)
        for b in self.getButtonsFromTab(idx):
            b.setEnabled(True)
        if s.dynamicShortcut():
            self.allocateDynamicShortcuts()

    def setCurrentTab(self, tab):
        """
        Sets a tab as active.
        :param tab: (int) tab index to be set as active.
        """
        if tab < self.tabWidget.count():
            self.tabWidget.setCurrentIndex(tab)
            self.setTabButtonsActive(tab)

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
            if s.isEnabled():
                s.setEnabled(False)
        for l in QgsProject.instance().mapLayers().values():
            # make sure all layers are disconnected from handling method
            if not isinstance(l, QgsVectorLayer):
                continue
            try:
                l.featureAdded.disconnect(self._registerAddedFeature)
                l.editCommandEnded.disconnect(self._handleAddedFeature)
            except TypeError:
                pass
        self.resetSuppressFormOption()
        b = self.featureExtractionButton()
        if b is not None:
            self.setMapToolFromButton(b)
            if b.checkLayer():
                self.setSuppressFormOption(b.vectorLayer(), False)
        else:
            self.setMapTool("pan")
        isSetup = self.setupComboBox.currentIndex() > 0
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
            layers = list()
            for b in s.buttons():
                b.setCallback(self.toolCallback)
                b.setShortcutCallback(self._shortcutActivated)
                b.toggled.connect(self._buttonToggled)
                l = b.vectorLayer()
                if l is not None and l.name() not in layers:
                    # avoid connecting more than once the same layer
                    l.featureAdded.connect(self._registerAddedFeature)
                    l.editCommandEnded.connect(self._handleAddedFeature)
                    layers.append(l.name())
        self.createTabs()
        # this needs to be after tab creation
        self.setTabButtonsActive(0)

    @pyqtSlot(bool, name="on_editSetupPushButton_clicked")
    def editCurrentSetup(self):
        """
        Opens button setup configuration GUI to edit current button setup.
        """
        self.restoreShortcuts()
        setup = self.currentButtonSetup()
        setup.setEnabled(False)
        # before editing current, check restore any potential modified shortcut
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
            self.resizeButtons()
        else:
            self.setCurrentTab(self.currentTab())

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

    @pyqtSlot(bool, name="on_removePushButton_clicked")
    def removeButtonSetup(self, setup):
        """
        Removes a setup from current set of setups.
        :param: (str) name for the setup to be removed.
        """
        if isinstance(setup, bool):
            # if a boolean is passed, call was from GUI button
            setup = self.currentButtonSetupName()
        if setup in self.buttonSetupNames():
            title = self.tr("DSGTools Custom Feature Tool: confirm removal")
            msg = self.tr("Would like to delete setup {0}?").format(setup)
            if not MessageRaiser().confirmAction(self, msg, title):
                return
            self.restoreShortcuts()
            self._order.pop(setup, None)
            setup = self._setups.pop(setup, None)
            if setup is None:
                return
            setup.setEnabled(False)
            del setup
            self.setupComboBox.removeItem(self.setupComboBox.currentIndex())

    def layerMode(self):
        """
        Reads from GUI which mode did the user set for layer selection: either
        reclassify selected features from all compatible loaded layers (geom
        type) on canvas or just the active layer.
        :return: (int) layer mode code.
        """
        return self.ActiveLayer if self.layerSelectionSwitch.currentState() == 0\
            else self.AllLayers

    def setLayerMode(self, mode):
        """
        Sets layer mode to GUI.
        :param mode: (int) layer mode code.
        """
        self.layerSelectionSwitch.setState(1 if mode == self.AllLayers else 0)

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
        self.setMapTool("pan")
        if self.toolMode() == self.Reclassify:
            self.resetSuppressFormOption()

    def featureExtractionButton(self):
        """
        Retrieves currently checked button to be used as feature extraction
        button.
        :return: (CustomFeatureButton) checked button.
        """
        s = self.currentButtonSetup()
        return s.checkedButton() if s is not None else None

    def _registerAddedFeature(self, featId):
        """
        In order to avoid corrupting the undo stack for the layer, feature
        added signal will be used to identify potential feature modifications.
        :param featId: (int) ID for the recently added feature.
        """
        if self.sender() is None:
            # manual calls are not allowed to modify tool's target feature
            # since it's a feature extraction operation
            return
        self._featId = featId

    def blockFields(self, layer, attrMap):
        """
        Checks attribute map for editable fields and blocks the others.
        :param layer: (QgsVectorLayer) layer to have its fields allowed to be
                      edited.
        :param attrMap: (dict) attribute map as from CustomFeatureButton.
        """
        editFormConfig = layer.editFormConfig()
        for idx, f in enumerate(layer.fields()):
            if f.name() not in attrMap or not attrMap[f.name()]["editable"]:
                editFormConfig.setReadOnly(idx, True)
        layer.setEditFormConfig(editFormConfig)

    def setFieldsEditable(self, layer):
        """
        Allows all fields to be editable.
        :param layer: (QgsVectorLayer) layer to have its fields allowed to be
                      edited.
        """
        editFormConfig = layer.editFormConfig()
        for idx in range(len(layer.fields())):
            editFormConfig.setReadOnly(idx, False)
        layer.setEditFormConfig(editFormConfig)

    def _handleAddedFeature(self):
        """
        Method designed to work exclusively from a feature added signal call.
        It has an important role on the feature extraction flow as "gate
        keeper" for attribute setting: identifies tool conditions and mode in
        order to define whether current feature extraction should be handled by
        this tool or if it's a "external" feature extraction process.
        """
        b = self.featureExtractionButton()
        inLayer = self.sender()
        added = True
        if b is None or not isinstance(inLayer, QgsVectorLayer)\
           or inLayer.name() != b.layer() or self._featId is None:
            # if there are no active buttons, tool is idle
            # if method was not sent from a vector layer, nothing to do either
            # only managed calls are from active button's layer
            # if no feature was just added, no good as well
            return
        editBuffer = inLayer.editBuffer()
        if editBuffer is None or not editBuffer.isFeatureAdded(self._featId):
            return
        feature = editBuffer.addedFeatures()[self._featId]
        # make sure feat is editted only when it was JUST added to the layer
        self._featId = None
        # update ignored values from map
        attrMap = b.attributeMap()
        defVals = LayerHandler().getDefaultValues(inLayer)
        feature = AttributeHandler(iface).setFeatureAttributes(
            feature, attrMap)
        for attr, props in attrMap.items():
            # the setFeatureAttributes method sets ignored values to None. If
            # the attribute has a provider's default or it was provided through
            # the map, it should be applied anyway ('ignored' does not make
            # sense to the feature extraction mode process)
            if not props["ignored"]:
                continue
            if attr in defVals:
                # default value > value from the map (priority order)
                feature[attr] = defVals[attr]
            else:
                feature[attr] = props["value"]
        if b.openForm():
            self.blockFields(inLayer, attrMap)
            form = QgsAttributeDialog(inLayer, feature, False)
            form.blockSignals(True)
            form.attributeForm().blockSignals(True)
            form.setMode(int(QgsAttributeEditorContext.SingleEditMode))
            added = form.exec_() == 1 # should the feature be added after all?
            self.setFieldsEditable(inLayer)
            if added:
                grand, minor, _ = Qgis.QGIS_VERSION.split(".", 2)
                if grand == "3" and int(minor) < 15:
                    updtFeat = form.attributeForm().feature()
                    # QGIS 3.15.x and less does not have "currentFormFeature"
                    for f in feature.fields():
                        field = f.name()
                        feature[field] = updtFeat[field]
                else:
                    feature = form.attributeForm().currentFormFeature()
        def updateFeatureWrapper():
            """
            A wrapper to make sure undo stack is set properly, avoiding crashes
            upon undoing and updates the stack to the modified feature command.
            """
            # added feature ("original") command is still registered and
            # feature extraction may only be registered onto the stack if it is
            # the tool's modification
            stack = inLayer.undoStack()
            cmd = stack.command(stack.count() - 1)
            # no easy way to identify the attribute modification command, so
            # this solution achieves it in a non-optimal form, by checking the
            # commands's stack label (displayed to the user). "supports"
            # EN, PT-BR, ES and PT-PT
            attrChanged = cmd.text().lower() in (
                "attributes changed", "atributos cambiados",
                "atributos modificados", "atributos alterados"
            )
            cmd.undo()
            cmd.setObsolete(True)
            stack.undo()
            if added:
                if b.openForm() and attrChanged:
                    # if form was opened and confirmed, layer will have an
                    # 'Attributes changed' edit command stacked as well
                    stack.undo()
                # insert the modified feature command into the stack
                inLayer.beginEditCommand("dsgtools custom feature")
                # avoid circular calls
                inLayer.featureAdded.disconnect(self._registerAddedFeature)
                inLayer.editCommandEnded.disconnect(self._handleAddedFeature)
                inLayer.addFeature(feature)
                inLayer.featureAdded.connect(self._registerAddedFeature)
                inLayer.endEditCommand()
                inLayer.editCommandEnded.connect(self._handleAddedFeature)
            self._timer.blockSignals(True)
            self._timer.setParent(None)
            del self._timer
            self._timer = QTimer(self)
        self._timer.start(1)
        self._timer.timeout.connect(updateFeatureWrapper)
        iface.mapCanvas().refresh()

    def setSuppressFormOption(self, layer, openForm=None):
        """
        Sets whether feature form for a layer is suppressed.
        :param layer: (QgsVectorLayer) layer to have its form suppression option
                      set.
        :param openForm: (bool) whether form should be displayed upon feature
                         extraction.
        :return: (CustomFeatureButton) checked button.
        """
        setup = layer.editFormConfig()
        option = {
            False: setup.SuppressOn,
            True: setup.SuppressOff,
            None: setup.SuppressDefault
        }[openForm]
        setup.setSuppress(option)
        layer.setEditFormConfig(setup)

    def resetSuppressFormOption(self):
        """
        Sets suppress form option to QGIS default for all layers on canvas.
        """
        for layer in QgsProject.instance().mapLayers().values():
            if not isinstance(layer, QgsVectorLayer):
                continue
            self.setSuppressFormOption(layer)

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
                layers = [l] if isinstance(l, QgsVectorLayer) else []
            for l in layers:
                if not isinstance(l, QgsVectorLayer):
                    continue
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
        Gets a list of features from a layer and adds it to a new layer with a
        new set of attributes and removes it from previous layer.
        :param featList: (list-of-QgsFeature) all features to be reclassified.
        :param prevLayer: (QgsVectorLayer) layer to have its reclassified from.
        :param newLayer: (QgsVectorLayer) layer to receive reclassified
                         features.
        :param newAttributeMap: (dict) a map to new features' attribute values.
        :return: (list-of-QgsFeature) all reclassified features.
        """
        lh = LayerHandler()
        defs = lh.getDestinationParameters(newLayer)
        defVals = lh.getDefaultValues(newLayer)
        transformer = lh.getCoordinateTransformer(prevLayer, newLayer)
        removeFeats = list()
        addFeats = set()
        fields = newLayer.fields()
        pFields = [f.name() for f in prevLayer.fields()]
        for f in featList:
            for field, propsMap in newAttributeMap.items():
                if propsMap["ignored"]:
                    if not propsMap["isPk"] and field in pFields \
                       and f[field] != NULL:
                        # preference is for previous filled value
                        propsMap["value"] = f[field]
                    elif field in defVals:
                        # then default value from layer provider
                        propsMap["value"] = defVals[field]
                    # as last priority, the value filled up at the map setup
                    # may be used
            addFeats.add(
                self.createFeature(
                    fields, f.geometry(), newAttributeMap, defs, transformer)
            )
            removeFeats.append(f.id())
        prevLayer.beginEditCommand("dsgtools reclassification (removed)")
        prevLayer.startEditing()
        prevLayer.deleteFeatures(removeFeats)
        prevLayer.updateExtents()
        prevLayer.endEditCommand()
        newLayer.beginEditCommand(
            "dsgtools reclassification (added from '{0}')".format(
                prevLayer.name())
        )
        newLayer.startEditing()
        newLayer.addFeatures(addFeats)
        newLayer.updateExtents()
        newLayer.endEditCommand()
        return addFeats

    def reclassify(self, recMap, layer, attrMap):
        """
        Applies feature reclassification method to the reclassification map.
        :recMap: (dict) a map from layer to feature list to be reclassified.
        :param attrMap: (dict) a map from field name to value on new layer.
        :param layer: (QgsVectorLayer) layer to receive all reclassified feats.
        """
        addedFeats = dict()
        for prevLayer, featList in recMap.items():
            fl = self.reclassifyFeatures(featList, prevLayer, layer, attrMap)
            addedFeats[prevLayer.name()] = len(fl)
        return addedFeats

    @pyqtSlot(bool)
    def _buttonToggled(self, checked):
        """
        Handles tool setup and pre-callback handling when a button is toggled.
        :param checked: (bool) whether button is being set to checked.
        """
        button = self.sender()
        if button is None:
            # method is supposed to be used exclusively as a slot
            return
        if checked:
            button.action().trigger()
        else:
            # button is being disabled
            self.resetSuppressFormOption()
            self.setMapTool("pan")

    def _shortcutActivated(self):
        """
        Shortcut may be activated whilst tool is in extract mode and in that
        mode, callbacks from action triggering is disconnected whenever the
        button is unchecked. This method is connected to shortcut activation
        event in order to make sure the requested button is properly set.
        """
        sh = self.sender()
        if self.toolMode() == self.Reclassify or sh is None:
            # method should be exclusively a slot to some signal
            return
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
        if isinstance(a, QAction):
            for button in s.buttons():
                if button.action().text() == a.text():
                    break
            else:
                # if button is not identified, call isn't from current setup
                return
        else:
            # somehow, event called from action leads to sender being the
            # button in here through button toggling handling method
            button = a
        if not button.checkLayer():
            msg = self.tr("layer '{0}' not loaded. Can't use button '{1}'.")\
                      .format(button.layer(), button.name())
            MessageRaiser().raiseIfaceMessage(
                self.tr("DSGTools feature reclassification"),
                msg, Qgis.Warning, 5
            )
            return
        vl = button.vectorLayer()
        if not vl.isEditable():
            vl.startEditing()
        # reset any of previous modifications
        self.resetSuppressFormOption()
        # forms for button's layer are manually called and handled
        self.setSuppressFormOption(vl, False)
        if self.toolMode() == self.Extract:
            if not button.isChecked():
                s.toggleButton(button, True)
        else:
            reclassify = self.featuresToBeReclassified(button)
            if not reclassify:
                msg = self.tr("could not reclassify using button {0} (no "
                              "compatible features selected)")\
                        .format(button.name())
                MessageRaiser().raiseIfaceMessage(
                    self.tr("DSGTools feature reclassification"),
                    msg, Qgis.Warning, 5
                )
                return
            attrMap = button.attributeMap()
            if button.openForm():
                form = CustomFeatureForm(vl, reclassify, attrMap)
                form.setWindowTitle(self.tr("{0} (receiving layer: {1})")\
                        .format(form.windowTitle(), vl.name()))
                if not form.exec_():
                    return
                # modified values should be used for feature reclassification
                reclassify = form.readSelectedLayers()
                attrMap = form.attributeMap
            reclassified = self.reclassify(reclassify, vl, attrMap)
            self.warnReclassified(reclassified, vl.name())
            # reclassification applies its effect immediately and should not
            # interfere on QGIS usual behaviour
            self.setSuppressFormOption(vl)
        iface.setActiveLayer(vl)
        iface.mapCanvas().refresh()
        self.setMapToolFromButton(button)

    def _mapToolSet(self, new, old):
        """
        Method that handles map tool changes whenever Custom Feature Tool is on
        feature extraction mode.
        :param new: (QgsMapTool) newly set map tool.
        :param old: (QgsMapTool) previously set map tool (the one that got
                    changed).
        """
        s = self.currentButtonSetup()
        b = self.featureExtractionButton()
        isRec = self.toolMode() == self.Reclassify
        if s is None or isRec or b is None or self.sender() is None:
            return
        def isToolAllowed(tool):
            if isinstance(tool, Polygon) or isinstance(tool, AcquisitionFree):
                return True
            tool = iface.mapCanvas().mapTool()
            a = tool.action() if hasattr(tool, "action") else None
            allowedQgisTools = ["mActionAddFeature", "mActionCircle2Points"]
            if a is not None and a.objectName() in allowedQgisTools:
                return True
            return False
        if not isToolAllowed(new):
            # widgets are not updated
            b.setChecked(False)
            self.resetSuppressFormOption()

    def setMapTool(self, tool):
        """
        Sets current map tool based on its name.
        :param tool: (str) non-i18n tool name to be set as active.
        """
        iface.mapCanvas().mapToolSet.disconnect(self._mapToolSet)
        # this is necessary to access the "singleton" DsgTools object
        # did not come up with a better solution yet
        from DsgTools.core.Utils import tools
        iface.mapCanvas().unsetMapTool(iface.mapCanvas().mapTool())
        if tool == "default":
            # default feature extraction tool from QGIS
            iface.actionAddFeature().trigger()
        elif tool == "circle2points":
            grand, minor, _ = Qgis.QGIS_VERSION.split(".", 2)
            if grand == "3" and int(minor) <= 10:
                # QGIS 3.10.x and less does not have "actionCircle2Points"
                iface.mainWindow().findChild(QAction, "mActionCircle2Points")\
                                  .trigger()
            else:
                # QGIS circle extraction from 2 points
                iface.actionCircle2Points().trigger()
        elif tool == "pan":
            # QGIS Pan Map tool (default navigation map tool)
            iface.actionPan().trigger()
        elif tool in tools.mapToolsNames():
            tools.mapTool(tool).toolAction.trigger()
        iface.mapCanvas().mapToolSet.connect(self._mapToolSet)

    def setMapToolFromButton(self, button):
        """
        Whenever a button is called it sets current map tool for feature
        extraction as defined in its properties, or sets the DSGTools: Generic
        Selector tool, if reclassification mode is set.
        :param button: (CustomFeatureButton) button to have its map tool set to
                       canvas.
        """
        if self.toolMode() == self.Extract:
            tool = button.digitizingTool() if button else "default"
        else:
            tool = "genericTool"
        self.setMapTool(tool)

    def zoomLevel(self):
        """
        Reads zoom level defined by user from GUI.
        :return: (int) zoom level chosen by user. It is allowed 3 levels:
                 normal (0 - 8px), large (1 - 12px) and largest (2 - 16px).
        """
        return int(self.slider.value())

    def setZoomLevel(self, lvl):
        """
        Sets zoom level to the GUI and setups.
        :param lvl: (int) zoom level chosen by user. It is allowed 3 levels:
                    normal (0 - 8px), large (1 - 12px) and largest (2 - 16px).
        """
        if lvl == self.zoomLevel():
            return
        self.slider.setValue(lvl)
        self.resizeButtons()

    @pyqtSlot(int, name="on_slider_valueChanged")
    def resizeButtons(self):
        """
        Sets the font size for each displayed button.
        """
        defaultSize = QPushButton().font().pointSize()
        size = int(defaultSize * (1 + 0.5 * self.zoomLevel()))
        for s in self.buttonSetups():
            s.setButtonsSize(size)

    def _exportSetup(self, setup):
        """
        Some of setup's properties are not serializable. This method allows all
        settings to be exported by adjusting such methods. Map is modified
        in-place.
        :param setup: (dict) map read from an imported JSON.
        """
        for idx, props in enumerate(setup["buttons"]):
            kws = props["keywords"]
            setup["buttons"][idx]["keywords"] = tuple(kws)
        return setup

    def toolState(self):
        """
        Retrieves a map with all parameters that indicates current tool setup.
        :return: (dict) a map to all parameters for current tool state.
        """
        """
        Exports current setup's saved state to a file.
        :return: (bool) whether setup was exported.
        """
        b = self.featureExtractionButton()
        self.restoreShortcuts() # to not "forget" buttons originals shortcuts
        state = {
            "setups": [
                self._exportSetup(s.state()) for s in  self.buttonSetups()
            ],
            "buttonsOrder": self._order,
            "currentSetup": self.currentButtonSetupName(),
            "activeButton": "" if b is None else b.name(),
            "toolMode": self.toolMode(),
            "layerMode": self.layerMode(),
            "activeTab": self.currentTab(),
            "zoom": self.zoomLevel(),
            "keywords": list(self.readButtonKeywords()),
            "enabled": self._enabled,
            "version": self.__VERSION
        }
        s = self.currentButtonSetup()
        if s is not None and s.dynamicShortcut():
            self.allocateDynamicShortcuts()
        return state

    def _importSetup(self, setup):
        """
        When exported to JSON, some of setup's settings have their type
        modified, such as: sets/tuples are stored as lists. This method fixes
        such modifications in order to avoid TypeError to be thrown. Map is
        updated in-place.
        :param setup: (dict) map read from an imported JSON.
        """
        for idx, props in enumerate(setup["buttons"]):
            kws = props["keywords"]
            setup["buttons"][idx]["keywords"] = set(kws)
            # tuples and list are misinterpreted when exported
            col = props["color"]
            setup["buttons"][idx]["color"] = tuple(col)

    def setToolState(self, state):
        """
        Sets tool to a given state.
        :param state: (dict) a map to all parameters for current tool state.
        """
        s = self.currentButtonSetup()
        if s is not None and s.dynamicShortcut():
            self.allocateDynamicShortcuts()
        self.clear()
        if not state or not state["setups"]:
            self.setToolEnabled(False)
            return
        self._order = state["buttonsOrder"]
        for s in state["setups"]:
            self._importSetup(s)
            setup = CustomButtonSetup()
            setup.setState(s)
            self.addButtonSetup(setup)
        if state["currentSetup"]:
            self.setCurrentButtonSetup(state["currentSetup"])
        setup = self.currentButtonSetup()
        # signals are not triggered when values are manually changed
        self.setToolMode(state["toolMode"])
        v = self.toolBehaviourSwitch.state() # updt layer mode exhibition
        self.toolBehaviourSwitch.stateChanged.emit(v)
        self.setLayerMode(state["layerMode"])
        self.setZoomLevel(state["zoom"])
        self.resizeButtons()
        if state["keywords"]:
            # does not matter if it is a list (it'll just iterate over it)
            self.setKeywordSet(state["keywords"])
            self.bFilterLineEdit.returnPressed.emit()
        self.setCurrentTab(state["activeTab"])
        b = setup.button(state["activeButton"]) if setup is not None else None
        if b is not None and state["toolMode"] == self.Extract:
            setup.toggleButton(b, True)
            b.toggled.emit(True)
        if setup.dynamicShortcut():
            self.allocateDynamicShortcuts()

    @pyqtSlot()
    def saveStateToProject(self):
        """
        Saves current tool state to the QGIS project.
        """
        self.restoreShortcuts()
        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(),
            "dsgtools_cfttoolbox_state",
            json.dumps(self.toolState())
        )
        if self.currentButtonSetupName():
            self.allocateDynamicShortcuts()

    def restoreStateFromProject(self):
        """
        Restores current tool state from project variable state.
        """
        state = json.loads(
            QgsExpressionContextUtils.projectScope(QgsProject.instance())\
                    .variable("dsgtools_cfttoolbox_state") or "{}"
        )
        self.setToolState(state)

    # @pyqtSlot()
    # def on_importPushButton_clicked(self):
    #     """
    #     Loads setups from a file.
    #     """
    #     fd = QFileDialog()
    #     filename = fd.getOpenFileName(
    #         caption=self.tr("Import a DSGTools button profile set"),
    #         filter=self.tr("DSGTools button profile set (*.setups)")
    #     )
    #     filename = filename[0] if isinstance(filename, tuple) else filename
    #     if not filename:
    #         return
    #     with open(filename, "r", encoding="utf-8") as fp:
    #         self.setToolState(json.load(fp))
    #     msg = self.tr("current state imported from '{0}'.").format(filename)
    #     MessageRaiser().raiseIfaceMessage(
    #         self.tr("DSGTools Custom Feature"), msg, Qgis.Success)

    # @pyqtSlot()
    # def on_exportPushButton_clicked(self):
    #     """
    #     Saves current set of setups state to a file.
    #     """
    #     fd = QFileDialog()
    #     filename = fd.getSaveFileName(
    #         caption=self.tr("Export a DSGTools button profile set"),
    #         filter=self.tr("DSGTools button profile set (*.setups)")
    #     )
    #     filename = filename[0] if isinstance(filename, tuple) else filename
    #     if not filename:
    #         return False
    #     with open(filename, "w", encoding="utf-8") as fp:
    #         fp.write(json.dumps(self.toolState(), indent=4))
    #     ret = os.path.exists(filename)
    #     if ret:
    #         msg = self.tr("current state exported to '{0}'.").format(filename)
    #         lvl = Qgis.Success
    #     else:
    #         msg = self.tr("unable to export current state to '{0}'.")\
    #                   .format(filename)
    #         lvl = Qgis.Critical
    #     MessageRaiser().raiseIfaceMessage(
    #         self.tr("DSGTools Custom Feature"), msg, lvl)
    #     return ret

    def hideToolEditButton(self, hide):
        """
        This method allows all button setups edition calls from buttons on the
        GUI to be hidden from (or displayed to) the user. This allows the tool
        state to be handled exclusively by API calls from external services,
        such as SAP.
        :param hide: (bool) whether buttons should be hidden from the GUI.
        """
        if hide == self._buttonsHidden:
            return
        tools = [
            # self.importPushButton,
            # self.exportPushButton,
            self.editSetupPushButton,
            self.addPushButton,
            self.removePushButton
        ]
        method = "hide" if hide else "show"
        for t in tools:
            getattr(t, method)()
        self._buttonsHidden = hide

    def isToolEditButtonHidden(self):
        """
        Identifies whether button setup GUI buttons are hidden from the user.
        :return: (bool) button setup edit GUI buttons visibility status.
        """
        return bool(self._buttonsHidden)

    def unload(self):
        """
        Clears all components.
        """
        self.setToolEnabled(False)
        self.setParent(None)
        self.visibilityChanged.disconnect(self.setToolEnabled)
        project = QgsProject.instance()
        project.writeProject.disconnect(self.saveStateToProject)
        project.readProject.disconnect(self.restoreStateFromProject)
        iface.mapCanvas().mapToolSet.disconnect(self._mapToolSet)
