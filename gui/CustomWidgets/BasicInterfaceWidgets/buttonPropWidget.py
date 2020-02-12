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

from qgis.core import QgsMessageLog

from qgis.PyQt import uic
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

    def fillToolComboBox(self):
        """
        Sets a up available feature extraction tool to GUI.
        """
        self.toolComboBox.clear()
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
        Sets button's acquisition tool to GUI.
        :param useColor: (bool) whether button should use a custom color
                         palette.
        """
        self.colorCheckBox.setChecked(useColor)

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

    def setUseToolTip(self, useToolTip):
        """
        Sets button's acquisition tool to GUI.
        :param useToolTip: (bool) whether button will have a tool tip assigned.
        """
        self.tooltipCheckBox.setChecked(useToolTip)

    def setToolTip(self, tooltip):
        """
        Sets a tool tip for the active button widget.
        :param tooltip: (str) tool tip to be set.
        """
        self.toolTipLineEdit.setText(tooltip)

    def setUseCategory(self, useCat):
        """
        Sets button's acquisition tool to GUI.
        :param useCat: (bool) whether button will have a category assigned.
        """
        self.categoryCheckBox.setChecked(useCat)

    def setCategory(self, cat):
        """
        Assigns a group to the active button.
        :param cat: (str) category to be set.
        """
        self.categoryLineEdit.setText(cat)

    def setUseKeywords(self, useKw):
        """
        Sets whether active button should have keywords for button searching.
        :param useKw: (bool) whether button will have keywords assigned to it.
        """
        self.keywordCheckBox.setChecked(useKw)

    def setKeywords(self, kws):
        """
        Sets button's keywords for button searching.
        :param kws: (set-of-str) set of keywords to be assigned to the button.
        """
        self.keywordLineEdit.setText(" ".join(kws))

    def setUseShortcut(self, useShortcut):
        """
        Sets whether active button should have a shortcut assigned to it.
        :param useShortcut: (bool) whether button will have a shortcut assigned.
        """
        self.shortcutCheckBox.setChecked(useShortcut)

    def setShortcurt(self, s):
        """
        Assigns a shortcut to trigger active button's action.
        :param s: (str) new shortcut to be set.
        """
        # check if shortcut is already assigned to some other action on QGIS
        self.shortcutWidget.setShortcut(QKeySequence.fromString(s))

    def setOpenForm(self, openForm):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :param openForm: (bool) whether feature form should be opened.
        """
        self.openFormCheckBox.setChecked(openForm)

    def setAttributeMap(self, attrMap):
        """
        Sets the attribute value map for current button to GUI.
        :param attrMap: (dict) a map from each field and its value to be set. 
        """
        pass

    def readAttributeMap(self):
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
        pass

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
        self.setAttributeMap(button.attributeMap())
        self.button.update(self.readButton().properties())

    def readButton(self):
        """
        Reads data from the interface and sets it to a button object.
        :return: (CustomFeatureButton) button read from the interface.
        """
        b = CustomFeatureButton()
        b.setName(self.nameLineEdit.text().strip())
        b.setAcquisitionTool(self.acquisitionTool())
        b.setUseColor(self.colorCheckBox.isChecked())
        if self.colorCheckBox.isChecked():
            b.setColor(self.mColorButton.color().getRgb())
        if self.tooltipCheckBox.isChecked():
            b.setToolTip(self.toolTipLineEdit.text().strip())
        if self.categoryCheckBox.isChecked():
            b.setCategory(self.categoryLineEdit.text().strip())
        if self.shortcutCheckBox.isChecked():
            b.setShortcut(self.shortcutWidget.getShortcut().strip())
        b.setOpenForm(self.openFormCheckBox.isChecked())
        b.setLayer(self.mMapLayerComboBox.currentText())
        b.setAttributeMap(self.readAttributeMap())
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

    # @pyqtSlot(int, name="on_buttonComboBox_currentIndexChanged")
    # def setActiveButton(self, button):
    #     """
    #     Changes current active button.
    #     :button: (CustomFeatureButton) button to be set as active.
    #     """
    #     isButton = bool(self.currentButtonName())
    #     self.savePushButton.setEnabled(isButton)
    #     self.undoPushButton.setEnabled(isButton)
    #     self.removePushButton.setEnabled(isButton)
    #     if isinstance(button, int):
    #         # then this came from the signal input
    #         button = self.currentButton()
    #     self.buttonComboBox.setCurrentText(button.name())
    #     self.nameLineEdit.setText(button.name())
    #     self.colorCheckBox.setChecked(button.useColor())
    #     if button.useColor():
    #         col = button.color()
    #         col = QColor(col) if isinstance(col, str) else QColor(*col)
    #         self.mColorButton.setColor(col)
    #     self.tooltipCheckBox.setChecked(bool(button.toolTip()))
    #     self.toolTipLineEdit.setText(button.toolTip())
    #     self.categoryCheckBox.setChecked(bool(button.category()))
    #     self.categoryLineEdit.setText(button.category())
    #     self.shortcutCheckBox.setChecked(bool(button.shortcut()))
    #     self.shortcutWidget.setShortcut(button.shortcut())
    #     self.openFormCheckBox.setChecked(button.openForm())

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

    # @pyqtSlot(bool)
    # def on_undoPushButton_clicked(self):
    #     """
    #     Restores stored data from current button and sets it to GUI.
    #     """
    #     self.setActiveButton(self.currentButton())

    # @pyqtSlot(bool, name="on_addPushButton_clicked")
    # def addButton(self):
    #     """
    #     Adds a new button to the interface.
    #     """
    #     button = CustomFeatureButton()
    #     name = button.name()
    #     names = [b.name() for b in self.setup().buttons()]
    #     if name in names:
    #         i = 1
    #         name = "{0} {1}".format(name, i)
    #         while name in names:
    #             name = "{0} {1}".format(button.name(), i)
    #             i += 1
    #         button.setName(name)
    #     self.setup().addButton(button.properties())
    #     self.buttonComboBox.addItem(name)
    #     self.setActiveButton(button)

    # @pyqtSlot(bool)
    # def on_removePushButton_clicked(self):
    #     """
    #     Removes the current button from setup.
    #     """
    #     # ADD CONFIRMATION BOX
    #     name = self.currentButton().name()
    #     if name == "":
    #         # ignore the "Select a button..."
    #         return
    #     self.setup().removeButton(name)
    #     self.buttonComboBox.removeItem(self.buttonComboBox.findText(name))

    # def state(self):
    #     """
    #     Retrieves dialog's data display state.
    #     :return: (dict) a map to object's state.
    #     """
    #     return {
    #         "item": self.buttonComboBox.currentIndex(),
    #         "buttons": [b.properties() for b in self.setup().buttons()],
    #         "activeData": {} # this may be a modified button not yet saved
    #     }

    # def setState(self, state):
    #     """
    #     Restores a saved state to current dialog's instance.
    #     :param state: (dict) a map to object's state.
    #     """
    #     msg = self.validateData(state)
    #     if msg == "":
    #         self.setup()
