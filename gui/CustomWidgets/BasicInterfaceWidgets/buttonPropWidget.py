# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-08-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from qgis.core import QgsMessageLog
from qgis.PyQt.QtGui import QIcon, QColor, QKeySequence
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtWidgets import (QWidget,
                                 QCheckBox,
                                 QFileDialog,
                                 QMessageBox,
                                 QRadioButton,
                                 QTableWidgetItem)

from DsgTools.gui.ProductionTools.Toolboxes.FieldToolBox.customButtonSetup import CustomButtonSetup, CustomFeatureButton

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'buttonPropWidget.ui'))

class ButtonPropWidget(QWidget, FORM_CLASS):
    def __init__(self, parent=None, button=None):
        """
        Class constructor.
        :param parent: (QtWidgets.*) any widget that 'contains' this tool.
        :param buttonProps: (CustomFeatureButton) button to be managed.
        """
        super(ButtonPropWidget, self).__init__(parent)
        self.setupUi(self)
        self.button = button or CustomFeatureButton()
        self.fillToolComboBox()
        self.colorCheckBox.toggled.connect(self.mColorButton.setEnabled)
        self.tooltipCheckBox.toggled.connect(self.toolTipLineEdit.setEnabled)
        self.categoryCheckBox.toggled.connect(self.categoryLineEdit.setEnabled)
        self.keywordCheckBox.toggled.connect(self.keywordLineEdit.setEnabled)
        self.shortcutCheckBox.toggled.connect(self.shortcutWidget.setEnabled)
        self.mMapLayerComboBox.layerChanged.connect(self.updateFieldTable)
        self.attributeTableWidget.setHorizontalHeaderLabels([
            self.tr("Attribute"), self.tr("Value"),
            self.tr("Editable"), self.tr("Ignored")
        ])
        self.updateFieldTable()

    def confirmAction(self, msg, title=None, showNo=True):
        """
        Raises a message box that asks for user confirmation.
        :param msg: (str) message requesting for confirmation to be shown.
        :param showNo: (bool) whether No button should be exposed.
        :return: (bool) whether action was confirmed.
        """
        mb = QMessageBox()
        title = msg or self.tr("Confirm action")
        if showNo:
            return QMessageBox.question(
                self, title, msg, QMessageBox.Yes | QMessageBox.No
            ) == QMessageBox.Yes
        else:
            return QMessageBox.question(
                self, title, msg, QMessageBox.Ok) == QMessageBox.Ok

    def fillToolComboBox(self):
        """
        Sets a up available feature extraction tool to GUI.
        """
        self.toolComboBox.clear()
        # make sure those keys are EXACTLY the same as in "supportedTools"
        # method, from CustomFeatureButton
        tools = {
            self.tr("QGIS default feature extraction tool"): QIcon(""),
            self.tr("DSGTools: Free Hand Acquisition"): \
                QIcon(':/plugins/DsgTools/icons/free_hand.png'),
            self.tr("QGIS Circle extraction tool"): \
                QIcon(':/plugins/DsgTools/icons/circle.png'),
            self.tr("DSGTools: Right Degree Angle Digitizing"): \
                QIcon(':/plugins/DsgTools/icons/home.png')
        }
        for idx, (tool, icon) in enumerate(tools.items()):
            self.toolComboBox.insertItem(idx, tool)
            if idx != 0:
                self.toolComboBox.setItemIcon(idx, icon)

    def setButtonName(self, name):
        """
        Sets button name to GUI.
        :param name: (str) name to be set to GUI.
        """
        self.nameLineEdit.setText(name)

    def buttonName(self):
        """
        Reads button name from GUI.
        :return: (str) button name read from GUI.
        """
        return self.nameLineEdit.text().strip()
    
    def setAcquisitionTool(self, tool):
        """
        Sets button's acquisition tool to GUI.
        :param tool: (str) a supported acquisition tool to be set.
        """
        tool = CustomFeatureButton().supportedTools()[tool]
        self.toolComboBox.setCurrentText(tool)

    def acquisitionTool(self):
        """
        Reads current acquisition tool.
        :return: (str) current acquisition tool.
        """
        tools = {v: k for k, v in \
                    CustomFeatureButton().supportedTools().items()}
        return tools[self.toolComboBox.currentText()]

    def setUseColor(self, useColor):
        """
        Sets whether button will have a custom color set as read from GUI.
        :param useColor: (bool) whether button should use a custom color
                         palette.
        """
        self.colorCheckBox.setChecked(useColor)

    def useColor(self):
        """
        Reads whether button will have a custom color from GUI.
        :return: (bool) whether button should use a custom color
                        palette.
        """
        return self.colorCheckBox.isChecked()

    def setColor(self, color):
        """
        Sets custom color to the color widget.
        :param color: (str/tuple) color to be set.
        """
        if isinstance(color, str):
            color = QColor(color)
        else:
            color = QColor(*color)
        self.mColorButton.setColor(color)

    def color(self):
        """
        Reads custom color to be set to widget as read from GUI.
        :return: (tuple) color to be used.
        """
        return self.mColorButton.color().getRgb()

    def setUseToolTip(self, useToolTip):
        """
        Defines if button will have a tool tip assigned to it as read from GUI.
        :param useToolTip: (bool) whether button will have a tool tip assigned.
        """
        self.tooltipCheckBox.setChecked(useToolTip)

    def useToolTip(self):
        """
        Reads if the button will have a tool tip assigned to it from GUI.
        :return: (bool) whether the button will have a tool tip assigned.
        """
        return self.tooltipCheckBox.isChecked()

    def setToolTip(self, tooltip):
        """
        Sets a tool tip for the active button widget.
        :param tooltip: (str) tool tip to be set.
        """
        self.toolTipLineEdit.setText(tooltip)

    def toolTip(self):
        """
        Reads the tool tip for the button from GUI.
        :param tooltip: (str) tool tip to be used.
        """
        return self.toolTipLineEdit.text()

    def setUseCategory(self, useCat):
        """
        Sets button's category/group to GUI.
        :param useCat: (bool) whether button will have a category assigned.
        """
        self.categoryCheckBox.setChecked(useCat)

    def useCategory(self):
        """
        Reads button's category/group from GUI.
        :return: (bool) whether button will have a category assigned.
        """
        return self.categoryCheckBox.isChecked()

    def setCategory(self, cat):
        """
        Assigns a category/group to the active button.
        :param cat: (str) category to be set.
        """
        self.categoryLineEdit.setText(cat)

    def category(self):
        """
        Reads the assigned category/group to the active button from GUI.
        :return: (str) category to be used.
        """
        return self.categoryLineEdit.text()

    def setUseKeywords(self, useKw):
        """
        Sets whether active button should have keywords for button searching.
        :param useKw: (bool) whether button will have keywords assigned to it.
        """
        self.keywordCheckBox.setChecked(useKw)

    def useKeywords(self):
        """
        Reads whether active button should have keywords for button searching
        from GUI.
        :return: (bool) whether button will have keywords assigned to it.
        """
        return self.keywordCheckBox.isChecked()

    def setKeywords(self, kws):
        """
        Sets button's keywords for button searching.
        :param kws: (set-of-str) set of keywords to be assigned to the button.
        """
        self.keywordLineEdit.setText(" ".join(kws))

    def keywords(self):
        """
        Reads button's keywords for button searching from GUI.
        :return: (set-of-str) set of keywords to be assigned to the button.
        """
        return set(self.keywordLineEdit.text().strip().split(" "))

    def setUseShortcut(self, useShortcut):
        """
        Sets whether active button should have a shortcut assigned to it.
        :param useShortcut: (bool) whether button will have a shortcut assigned.
        """
        self.shortcutCheckBox.setChecked(useShortcut)

    def useShortcut(self):
        """
        Reads whether active button should have a shortcut assigned to it from GUI.
        :return: (bool) whether button will have a shortcut assigned.
        """
        return self.shortcutCheckBox.isChecked()

    def checkShortcut(self, s):
        """
        Verifies if a shortcut is already set to any action on QGIS.
        :param s: (str) shortcut to be checked.
        :return: (str) action associated with given shortcut.
        """
        if s == "":
            return ""
        for m in dir(iface):
            if m.startswith("action") and \
               getattr(iface, m)().shortcut().toString().lower() == s.lower():
                return getattr(iface, m)().text()
        return ""

    def setShortcurt(self, s, autoReplace=True):
        """
        Assigns a shortcut to trigger active button's action.
        :param s: (str) new shortcut to be set.
        :param autoReplace: (bool) whether a confirmation from the user is
                            necessary in order to replace existing shortcuts.
        """
        s = s.replace(" ", "")
        action = self.checkShortcut(s)
        if not autoReplace and action != "":
            txt = self.tr("Shortcut {s} is already assigned to {a}, would you "
                        "like to replace it?").format(s=s, a=action)
            if not self.confirmAction(txt, self.tr("Replace shortcut")):
                return
        self.shortcutWidget.setShortcut(QKeySequence.fromString(s))

    def shortcut(self):
        """
        Assigned shortcut read from GUI.
        :return: (str) shortcut to be used.
        """
        s = self.shortcutWidget.getShortcut(True)
        return s.toString() if s != 0 else ""

    def setOpenForm(self, openForm):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :param openForm: (bool) whether feature form should be opened.
        """
        self.openFormCheckBox.setChecked(openForm)

    def openForm(self):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :return: (bool) whether feature form should be opened.
        """
        return self.openFormCheckBox.isChecked()

    def setAttributeMap(self, attrMap):
        """
        Sets the attribute value map for current button to GUI.
        :param attrMap: (dict) a map from each field and its value to be set. 
        """
        pass

    def attributeMap(self):
        """
        Reads the field map data and set it to a button attribute map format.
        :return: (dict) read attribute map. 
        """
        return dict()

    def setLayer(self, layer):
        """
        Sets current layer selection on GUI.
        :param layer: (str) name for the layer to be set.
        """
        if layer != "":
            self.mMapLayerComboBox.setCurrentText(layer)
        else:
            self.mMapLayerComboBox.setCurrentIndex(0)

    def layer(self):
        """
        Reads current layer selection from GUI.
        :return: (str) name for the selected layer.
        """
        return self.mMapLayerComboBox.currentText()

    def updateFieldTable(self, layer=None):
        """
        Updates current displayed fields based on current layer selection.
        :param layer: (QgsVectorLayer) layer to have its fields exposed. 
        """
        layer = layer or self.mMapLayerComboBox.currentLayer()
        self.attributeTableWidget.setRowCount(0)
        fields = layer.fields()
        self.attributeTableWidget.setRowCount(len(fields))
        for row, field in enumerate(fields):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsEditable) # not editable
            item.setText(field.name())
            self.attributeTableWidget.setItem(row, 0, item)
            self.attributeTableWidget.setCellWidget(row, 2, QCheckBox())
            self.attributeTableWidget.setCellWidget(row, 3, QCheckBox())

    def setButton(self, button):
        """
        Sets button properties to the GUI.
        :param button:  (CustomFeatureButton) button to be set to the GUI.
        """
        self.setButtonName(button.name())
        self.setAcquisitionTool(button.acquisitionTool())
        self.setUseColor(button.useColor())
        self.setColor(button.color())
        self.setUseToolTip(bool(button.toolTip()))
        self.setToolTip(button.toolTip())
        self.setUseCategory(bool(button.category()))
        self.setCategory(button.category())
        self.setUseKeywords(bool(button.keywords()))
        self.setKeywords(button.keywords())
        self.setUseShortcut(bool(button.shortcut()))
        self.setShortcurt(button.shortcut())
        self.setOpenForm(button.openForm())
        self.setLayer(button.layer())
        self.updateFieldTable()
        self.setAttributeMap(button.attributeMap())
        self.mColorButton.setEnabled(button.useColor())
        self.toolTipLineEdit.setEnabled(bool(button.toolTip()))
        self.categoryLineEdit.setEnabled(bool(button.category()))
        self.keywordLineEdit.setEnabled(bool(button.keywords()))
        self.shortcutWidget.setEnabled(bool(button.shortcut()))
        self.button = button

    def readButton(self):
        """
        Reads data from the interface and sets it to a button object.
        :return: (CustomFeatureButton) button read from the interface.
        """
        b = CustomFeatureButton()
        b.setName(self.buttonName())
        b.setAcquisitionTool(self.acquisitionTool())
        b.setUseColor(self.useColor())
        if self.useColor():
            b.setColor(self.color())
        b.setToolTip(self.toolTip() if self.useToolTip() else "")
        b.setCategory(self.category() if self.useCategory() else "")
        b.setKeywords(self.keywords() if self.useKeywords() else set(""))
        b.setShortcut(self.shortcut() if self.useShortcut() else "")
        b.setOpenForm(self.openForm())
        b.setLayer(self.layer())
        b.setAttributeMap(self.attributeMap())
        return b

    def currentButtonName(self):
        """
        Retrieves currently selected button on button combo box.
        :return: (CustomFeatureButton) button read from the setup object.
        """
        return self.button.name()
    
    def currentButton(self):
        """
        Retrieves currently SAVED button.
        :return: (CustomFeatureButton) current button.
        """
        return self.button

    def setEnabled(self, enabled):
        """
        Defines whether all widgets should be enabled.
        :param enabled: (bool) widgets enabling status.
        """
        self.nameLineEdit.setEnabled(enabled)
        self.toolComboBox.setEnabled(enabled)
        self.colorCheckBox.setEnabled(enabled)
        self.mColorButton.setEnabled(enabled)
        self.tooltipCheckBox.setEnabled(enabled)
        self.toolTipLineEdit.setEnabled(enabled)
        self.categoryCheckBox.setEnabled(enabled)
        self.categoryLineEdit.setEnabled(enabled)
        self.keywordCheckBox.setEnabled(enabled)
        self.keywordLineEdit.setEnabled(enabled)
        self.shortcutCheckBox.setEnabled(enabled)
        # self.shortcutWidget.setEnabled(enabled)
        self.openFormCheckBox.setEnabled(enabled)
        self.mMapLayerComboBox.setEnabled(enabled)
        self.attributeTableWidget.setEnabled(enabled)

    # def validateData(self, data=None, new=True):
    #     """
    #     Validates if a given set of button properties is valid accordingly to
    #     current button setup context.
    #     :param data: (dict) map of button properties to be validated.
    #     :param new: (bool) indicates if the property map is for a button that
    #                 is already saved into current setup, or if it is supposed
    #                 to be added to it.
    #     :return: (str) invalidation reason.
    #     """
    #     b = CustomFeatureButton(data or self.readButton().properties())
    #     s = self.setup()
    #     return ""

    # def isValid(self):
    #     """
    #     Identifies whether all input data is valid.
    #     :return: (bool) input data is validity status.
    #     """
    #     return self.validateData() == ""