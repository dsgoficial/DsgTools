# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-02-10
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

import os, json

from qgis.core import Qgis, QgsMessageLog, QgsApplication
from qgis.gui import QgsMessageBar
from qgis.PyQt import uic
from qgis.PyQt.QtCore import (Qt,
                              QSize,
                              pyqtSlot,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import (QDialog,
                                 QFileDialog,
                                 QMessageBox,
                                 QHeaderView,
                                 QRadioButton,
                                 QAbstractItemView)

from DsgTools.gui.ProductionTools.Toolboxes.CustomFeatureToolBox.customButtonSetup import CustomButtonSetup, CustomFeatureButton

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'buttonSetupWidget.ui'))
app = QgsApplication.instance()

class ButtonSetupWidget(QDialog, FORM_CLASS):
    def __init__(self, parent=None, buttonSetup=None):
        """
        Class constructor.
        :param parent: (QtWidgets.*) any widget that 'contains' this tool.
        :param buttonSetup: (CustomButtonSetup) object that handles all
                            buttons displayed and configured through this GUI.
        """
        super(ButtonSetupWidget, self).__init__(parent)
        self.setupUi(self)
        self.messageBar = QgsMessageBar(self)
        self.setup = CustomButtonSetup()
        if buttonSetup:
            self.setSetup(buttonSetup)
        self.buttonComboBox.addItem(self.tr("No button selected"))
        self.tableWidget.verticalHeader().sectionDoubleClicked.connect(
            self.setButtonFromRow)
        bEnabled = self.buttonComboBox.currentIndex() > 0
        for w in ("savePushButton", "undoPushButton", "removePushButton",
                  "buttonPropWidget"):
            getattr(self, w).setEnabled(bEnabled)
        
        # making the button selection to stand out a little bit
        if "Night Mapping" in app.activeThemePath():
            ss = """QHeaderView::section:checked
                { color:black; background-color:white; }"""
        else:
            ss = """QHeaderView::section:checked
                { color:gray; background-color:black; }"""
        self.tableWidget.setStyleSheet(ss)

    def raiseWarning(self, msg, title=None, lvl=None, duration=None):
        """
        Raises a warning message to the user on a message bar and logs it to
        QGIS logger.
        :param msg: (str) message to be displayed.
        :param title: (str) pre-message on the warning bar.
        :param lvl: (int) warning level enumerator as from Qgis module.
        :param duration: (int) warning message display time.
        """
        self.messageBar.pushMessage(
            title or self.tr('Invalid workflow'), msg,
            level=lvl or Qgis.Warning, duration=duration or 5
        )
        # msg = self.tr("Buttons setup definion invalid: {m}").format(m=msg)
        QgsMessageLog.logMessage(msg, 'DSGTools Plugin', Qgis.Warning)

    def resizeEvent(self, e):
        """
        Reimplementation in order to use this window's resize event.
        On this object, this method makes sure that message bar is always the
        same size as the window.
        :param e: (QResizeEvent) resize event.
        """
        self.messageBar.resize(
            QSize(
                self.geometry().size().width(),
                40 # this felt nicer than the original height (30)
            )
        )

    def clear(self):
        """
        Clears all data filled into GUI.
        """
        self.buttonComboBox.clear()
        for button in self.registeredButtonNames():
            self.removeButtonFromTable(self.getButtonByName(button))
            self.setup.removeButton(button)
            self.buttonComboBox.removeItem(self.buttonComboBox.findText(button))

    def setSetupName(self, name):
        """
        Defines setup's name on GUI.
        :param name: (str) name to be set.
        """
        self.setupNameLineEdit.setText(name)

    def setupName(self):
        """
        Retrieves button's setup name read from GUI.
        :return: (str) name for button's setup.
        """
        return self.setupNameLineEdit.text()

    def setCurrentSetupName(self, name):
        """
        Defines current button's setup name.
        :param name: (str) name for button's setup.
        """
        return self.setup.setName(name)

    def currentSetupName(self):
        """
        Retrieves current button's setup name.
        :param name: (str) name for button's setup.
        """
        return self.setup.name()

    def setDescription(self, desc):
        """
        Defines setup's description on GUI.
        :param desc: (str) description to be set.
        """
        self.textEdit.setText(desc)

    def description(self):
        """
        Reads button's setup description from GUI.
        :return: (str) description for button's setup.
        """
        return self.textEdit.toPlainText()

    def setCurrentDescription(self, name):
        """
        Defines current button's setup description.
        :param name: (str) description for button's setup.
        """
        self.setup.setDescription(name)

    def currentDescription(self):
        """
        Retrieves current button's description.
        :param name: (str) description for button's setup.
        """
        return self.setup.description()

    def setDynamicShortcut(self, ds):
        """
        Defines setup's dynamic shortcut option on GUI.
        :param ds: (bool) dynamic shortcut assignment option.
        """
        self.dsCheckBox.setChecked(ds)

    def dynamicShortcut(self):
        """
        Retrieves button's setup dynamic shortcut option read from GUI.
        :param ds: (bool) dynamic shortcut assignment option.
        """
        return self.dsCheckBox.isChecked()

    def setCurrentDynamicShortcut(self, ds):
        """
        Defines current button's setup dynamic shortcut option.
        :param ds: (bool) dynamic shortcut assignment option.
        """
        self.setup.setDynamicShortcut(ds)

    def currentDynamicShortcut(self):
        """
        Retrieves current button's description.
        :return: (bool) dynamic shortcut assignment option.
        :param name: (str) description for button's setup.
        """
        return self.setup.dynamicShortcut()

    def readSetup(self):
        """
        Reads setup from GUI.
        :return: (CustomButtonSetup) reads all data from GUI as a setup.
        """
        s = CustomButtonSetup()
        s.setName(self.setupName())
        s.setDescription(self.description())
        for row in range(self.tableWidget.rowCount()):
            s.addButton(self.buttonFromRow(row).properties())
        s.setDynamicShortcut(self.dynamicShortcut())
        return s

    def setSetup(self, newSetup):
        """
        Imports buttons setup definitions from another buttons setup.
        :param newSetup: (CustomButtonSetup) setup to be imported. 
        """
        self.buttonComboBox.blockSignals(True)
        self.setSetupName(newSetup.name())
        self.setCurrentSetupName(newSetup.name())
        self.setDescription(newSetup.description())
        self.setCurrentDescription(newSetup.description())
        self.setDynamicShortcut(newSetup.dynamicShortcut())
        self.setCurrentDynamicShortcut(newSetup.dynamicShortcut())
        for button in newSetup.buttons():
            self.addButton(button)
        self.buttonComboBox.blockSignals(False)

    def getButtonByName(self, name):
        """
        Retrieves a registered button from its name.
        :param name: (str) name for the requested button.
        """
        return self.setup.button(name)

    def setButtonName(self, name):
        """
        Sets button name to GUI.
        :param name: (str) name to be set to GUI.
        """
        self.buttonPropWidget.setButtonName(name)

    def buttonName(self):
        """
        Reads button name from GUI.
        :return: (str) button name read from GUI.
        """
        return self.buttonPropWidget.buttonName()

    def registeredButtonNames(self):
        """
        All names for registered buttons on current profile.
        :return: (list-of-str) list of button names.
        """
        return self.setup.buttonNames()

    def setDigitizingTool(self, tool):
        """
        Sets button's digitizing tool to GUI.
        :param tool: (str) a supported digitizing tool to be set.
        """
        self.buttonPropWidget.setDigitizingTool(tool)

    def digitizingTool(self):
        """
        Reads current digitizing tool from GUI.
        :return: (str) current digitizing tool.
        """
        return self.buttonPropWidget.digitizingTool()

    def setUseColor(self, useColor):
        """
        Sets button's digitizing tool to GUI.
        :param useColor: (bool) whether button should use a custom color
                         palette.
        """
        self.buttonPropWidget.setUseColor(useColor)

    def useColor(self):
        """
        Reads whether button will have a custom color from GUI.
        :return: (bool) whether button should use a custom color
                        palette.
        """
        return self.buttonPropWidget.useColor()

    def setColor(self, color):
        """
        Sets custom color to the color widget.
        :param color: (str/tuple) color to be set.
        """
        self.buttonPropWidget.setColor(color)

    def color(self):
        """
        Reads custom color to be set to widget as read from GUI.
        :return: (tuple) color to be used.
        """
        return self.buttonPropWidget.color()

    def setUseToolTip(self, useToolTip):
        """
        Sets button's digitizing tool to GUI.
        :param useToolTip: (bool) whether button will have a tool tip assigned.
        """
        self.buttonPropWidget.setUseToolTip(useToolTip)

    def useToolTip(self):
        """
        Reads if the button will have a tool tip assigned to it from GUI.
        :return: (bool) whether the button will have a tool tip assigned.
        """
        return self.buttonPropWidget.useToolTip()

    def setToolTip(self, tooltip):
        """
        Sets a tool tip for the active button widget.
        :param tooltip: (str) tool tip to be set.
        """
        self.buttonPropWidget.setToolTip(tooltip)

    def toolTip(self):
        """
        Reads the tool tip for the button from GUI.
        :param tooltip: (str) tool tip to be used.
        """
        return self.buttonPropWidget.toolTip()

    def setUseCategory(self, useCat):
        """
        Sets whether button should be assigned a category/group on GUI.
        :param useCat: (bool) whether button will have a category assigned.
        """
        self.buttonPropWidget.setUseCategory(useCat)

    def useCategory(self):
        """
        Reads button's category/group from GUI.
        :return: (bool) whether button will have a category assigned.
        """
        return self.buttonPropWidget.useCategory()

    def setCategory(self, cat):
        """
        Assigns a group to the active button.
        :param cat: (str) category to be set.
        """
        self.buttonPropWidget.setCategory(cat)

    def category(self):
        """
        Reads the assigned category/group to the active button from GUI.
        :return: (str) category to be used.
        """
        return self.buttonPropWidget.category()

    def setUseKeywords(self, useKw):
        """
        Sets whether active button should have keywords for button searching.
        :param useKw: (bool) whether button will have keywords assigned to it.
        """
        self.buttonPropWidget.setUseKeywords(useKw)

    def useKeywords(self):
        """
        Reads whether active button should have keywords for button searching
        from GUI.
        :return: (bool) whether button will have keywords assigned to it.
        """
        return self.buttonPropWidget.useKeywords()

    def setKeywords(self, kws):
        """
        Sets button's keywords for button searching.
        :param kws: (set-of-str) set of keywords to be assigned to the button.
        """
        self.buttonPropWidget.setKeywords(kws)

    def keywords(self):
        """
        Reads button's keywords for button searching from GUI.
        :return: (set-of-str) set of keywords to be assigned to the button.
        """
        return self.buttonPropWidget.keywords()

    def setUseShortcut(self, useShortcut):
        """
        Sets whether active button should have a shortcut assigned to it.
        :param useShortcut: (bool) whether button will have a shortcut assigned.
        """
        self.buttonPropWidget.setUseShortcut(useShortcut)

    def useShortcut(self):
        """
        Reads whether active button should have a shortcut assigned to it from GUI.
        :return: (bool) whether button will have a shortcut assigned.
        """
        return self.buttonPropWidget.useShortcut()

    def setShortcurt(self, s, autoReplace):
        """
        Assigns a shortcut to trigger active button's action.
        :param s: (str) new shortcut to be set.
        :param autoReplace: (bool) whether a confirmation from the user is
                            necessary in order to replace existing shortcuts.
        """
        self.buttonPropWidget.setShortcurt(s, autoReplace)

    def shortcut(self):
        """
        Assigned shortcut read from GUI.
        :return: (str) shortcut to be used.
        """
        return self.buttonPropWidget.shorcut()

    def setOpenForm(self, openForm):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :param openForm: (bool) whether feature form should be opened.
        """
        self.buttonPropWidget.setOpenForm(openForm)

    def openForm(self):
        """
        Defines whether (re)classification tool will open feature form while
        being used.
        :return: (bool) whether feature form should be opened.
        """
        return self.buttonPropWidget.openForm()

    def setAttributeMap(self, attrMap):
        """
        Sets the attribute value map for current button to GUI.
        :param attrMap: (dict) a map from each field and its value to be set. 
        """
        self.buttonPropWidget.setAttributeMap(attrMap)

    def attributeMap(self):
        """
        Reads the field map data and set it to a button attribute map format.
        :return: (dict) read attribute map. 
        """
        return self.buttonPropWidget.attributeMap()

    def setLayer(self, layer):
        """
        Sets current layer selection on GUI.
        :param layer: (str) name for the layer to be set.
        """
        self.buttonPropWidget.setLayer(layer)

    def layer(self):
        """
        Reads current layer selection from GUI.
        :return: (str) name for the selected layer.
        """
        self.buttonPropWidget.layer() 

    def currentButton(self):
        """
        Retrives button active on GUI that has a saved state (on its last saved
        state).
        :return: (CustomFeatureButton) current button.
        """
        return self.buttonPropWidget.currentButton()

    def readButton(self):
        """
        Reads current data on GUI and gets a button with those properties.
        :return: (CustomFeatureButton) current button as from GUI.
        """
        return self.buttonPropWidget.readButton()

    def buttonIsModified(self):
        """
        Checks whether current button is modified.
        :return: (bool) whether button is modified.
        """
        return self.currentButton() != self.readButton()

    def updateButton(self, buttonName, newProps):
        """
        Updates a registered button with a new set of properties.
        :param button: (str) name for the button to be updated.
        :param newProps: (dict) new set of properties.
        """
        self.setup.updateButton(buttonName, newProps)

    def confirmAction(self, msg, title=None, showNo=True):
        """
        Raises a message box that asks for user confirmation.
        :param msg: (str) message requesting for confirmation to be shown.
        :param showNo: (bool) whether No button should be exposed.
        :return: (bool) whether action was confirmed.
        """
        return self.buttonPropWidget.confirmAction(msg, title, showNo)

    def validate(self):
        """
        Validates current input data, giving invalidation reason.
        :return: (str) invalidation reason.
        """
        if self.setupName() == "":
            return self.tr("No name provided for current setup.")
        buttons = self.readSetup().buttons()
        if not buttons:
            return self.tr("Please register at least one button.")
        # for button in buttons:
        #     # validate attribute map
        #     pass
        return ""

    def isValid(self):
        """
        Validates current input data, giving invalidation reason.
        :return: (bool) current input data validity.
        """
        if self.setupName() == "":
            return False
        buttons = self.readSetup().buttons()
        if not buttons:
            return False
        # for button in buttons:
        #     # validate attribute map
        #     pass
        return True

    @pyqtSlot(int, name="on_buttonComboBox_currentIndexChanged")
    def setCurrentButton(self, button):
        """
        Sets button properties to the GUI.
        :param button:  (CustomFeatureButton) button to be set to the GUI.
        """
        if isinstance(button, int):
            if button <= 0:
                button = CustomFeatureButton()
                button.setName("")
            else:
                # table row is less 1 due to "no button" option
                button = self.buttonFromRow(button - 1)
        if button.name() not in self.registeredButtonNames():
            # create a new one with that button?
            pass
        self.buttonComboBox.setCurrentText(button.name())
        bEnabled = self.buttonComboBox.currentIndex() > 0
        for w in ("savePushButton", "undoPushButton", "removePushButton",
                  "buttonPropWidget"):
            getattr(self, w).setEnabled(bEnabled)
        self.buttonPropWidget.setButton(button)

    @pyqtSlot(bool, name="on_savePushButton_clicked")
    def updateCurrentButton(self, props=None):
        """
        Current data will be stored as current button's properties.
        :param props: (dict) a map to button's properties to be updated.
        """
        if isinstance(props, bool) or props is None:
            # if button pressing was the triggering event, current data will be
            # store into current button
            props = self.readButton().properties()
        prevName = self.currentButton().name()
        button = self.getButtonByName(prevName)
        self.updateButton(prevName, props)
        newName = button.name()
        self.buttonPropWidget.button = button
        if prevName != newName:
            idx = self.buttonComboBox.findText(prevName)
            self.buttonComboBox.setItemText(idx, newName)
        self.setCurrentButton(button)

    @pyqtSlot(bool, name="on_undoPushButton_clicked")
    def undoButtonModifications(self):
        """
        Restores stored data from current button and sets it to GUI.
        """
        self.buttonPropWidget.setButton(self.currentButton())

    @pyqtSlot(bool, name="on_addPushButton_clicked")
    def addButton(self, button=None):
        """
        Adds a button to the setup.
        :param button: (CustomFeatureButton) a pre-existent button to be set.
        :return: (CustomFeatureButton) added button.
        """
        if button is not None and not isinstance(button, bool):
            buttonName = button.name()
            if buttonName in self.registeredButtonNames():
                msg = self.tr("Button {b} already exists. Would you like to "
                              "replace it?").format(b=buttonName)
                cnf = self.confirmAction(msg,
                    self.tr("Replace existing button"))
                if not cnf:
                    return self.getButtonByName(buttonName)
                self.updateButton(buttonName, button.properties())
            else:
                props = button.properties()
                button = self.setup.newButton()
                self.buttonComboBox.addItem(buttonName)
                self.updateButton(button.name(), props)
            # we want the button passed by reference from setup
            button = self.getButtonByName(buttonName)
        else:
            button = self.setup.newButton()
            self.buttonComboBox.addItem(button.name())
        self.setCurrentButton(button)
        self.addButtonToTable(button)
        return button

    @pyqtSlot(bool, name="on_removePushButton_clicked")
    def removeButton(self):
        """
        Removes the current button from setup.
        """
        name = self.buttonName()
        txt = self.tr("Confirm button '{b}' removal?").format(b=name)
        if name == "":
            # ignore the "Select a button..."
            return
        self.removeButtonFromTable(self.currentButton())
        self.setup.removeButton(name)
        self.buttonComboBox.removeItem(self.buttonComboBox.findText(name))

    def buttonFromRow(self, row):
        """
        Retrieves the button object from table row.
        :param row: (int) target row to get its button.
        :return: (CustomFeatureButton) retrieved button.
        """
        # combo box includes "no button", table does not -> row + 1
        return self.getButtonByName(self.buttonComboBox.itemText(row + 1))

    def setButtonFromRow(self, row):
        """
        Fills GUI with a button's properties from its row.
        :param row: (int) target row to get its button.
        """
        b = self.getButtonByName(self.buttonComboBox.itemText(row + 1))
        self.setCurrentButton(b)

    def addButtonToTable(self, button):
        """
        Adds widget to table widget.
        :param button: (CustomFeatureButton) button to have its widget added.
        """
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setCellWidget(row, 0, button.newWidget())

    def removeButtonFromTable(self, button):
        """
        Removes the button widget from buttons table.
        :param button: (CustomFeatureButton) button to be removed.
        """
        name = button.displayName()
        for row in range(self.tableWidget.rowCount()):
            bName = self.tableWidget.cellWidget(row, 0).text().replace("&", "")
            if bName == name:
                self.tableWidget.removeRow(row)
                return

    def readButtonTable(self):
        """
        Reads all registered buttons from button table and returns it, in
        order.
        :return: (list-of-CustomFeature) ordered buttons.
        """
        buttons = list()
        count = self.tableWidget.rowCount()
        if count > 0:
            for row in range(count):
                buttons.append(
                    self.tableWidget.cellWidget(row, 0).text()\
                        .rsplit(" [", 1)[0].replace("&", "")
                ) # Qt mnemonic shortcut for it widgets introduces "&"...
        return buttons

    def buttonsOrder(self):
        """
        Retrieves button order to be used for button setup.
        :return: (dict) a map from button name to its position on GUI.
        """
        buttons = dict()
        for row in range(self.tableWidget.rowCount()):
            button = self.tableWidget.cellWidget(row, 0).text()\
                         .rsplit(" [", 1)[0].replace("&", "")
            buttons[button] = row
        return buttons

    def selectedIndexes(self):
        """
        :return: (list-of-QModelIndex) table's selected indexes.
        """
        return self.tableWidget.selectedIndexes()

    def selectedRows(self, reverseOrder=False):
        """
        List of all rows that have selected items on the table.
        :param reverOrder: (bool) indicates if the row order is reversed.
        :return: (list-of-int) ordered list of selected rows' indexes.
        """
        rows = self.tableWidget.selectionModel().selectedRows()
        return sorted(set(i.row() for i in rows), reverse=reverseOrder)

    def selectedColumns(self, reverseOrder=False):
        """
        List of all columns that have selected items on the table.
        :param reverOrder: (bool) indicates if the column order is reversed.
        :return: (list-of-int) ordered list of selected columns' indexes.
        """
        return sorted(
            set(i.column() for i in self.selectedIndexes()),
            reverse=reverseOrder
        )

    def selectRow(self, row):
        """
        Clears all selected rows and selects row.
        :param row: (int) index for the row to be select.
        """
        self.clearRowSelection()
        self.addRowToSelection(row)

    def addRowToSelection(self, row):
        """
        Adds a row to selection.
        :param row: (int) index for the row to be added to selection.
        """
        if row not in self.selectedRows():
            self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
            self.tableWidget.selectRow(row)
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def removeRowFromSelection(self, row):
        """
        Removes a row from selection.
        :param row: (int) index for the row to be removed from selection.
        """
        if row in self.selectedRows():
            self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
            self.tableWidget.selectRow(row)
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def clearRowSelection(self):
        """
        Removes all selected rows from selection.
        """
        for row in self.selectedRows():
            self.removeRowFromSelection(row)

    def moveRowUp(self, row):
        """
        Moves a row one position up, if possible.
        :param row: (int) row be moved.
        """
        if row <= 0:
            return
        button = self.buttonFromRow(row)
        upperButton = self.buttonFromRow(row - 1)
        self.tableWidget.setCellWidget(row - 1, 0, button.newWidget())
        self.buttonComboBox.setItemText(row, button.name())
        self.tableWidget.setCellWidget(row, 0, upperButton.newWidget())
        self.buttonComboBox.setItemText(row + 1, upperButton.name())
        self.addRowToSelection(row - 1)
        self.removeRowFromSelection(row)

    def moveRowDown(self, row):
        """
        Moves a row one position up, if possible.
        :param row: (int) row be moved.
        """
        if row >= self.tableWidget.rowCount() - 1:
            return
        button = self.buttonFromRow(row)
        lowerButton = self.buttonFromRow(row + 1)
        self.tableWidget.setCellWidget(row + 1, 0, button.newWidget())
        self.buttonComboBox.setItemText(row + 1 + 1, button.name())
        self.tableWidget.setCellWidget(row, 0, lowerButton.newWidget())
        self.buttonComboBox.setItemText(row + 1, lowerButton.name())
        self.addRowToSelection(row + 1)
        self.removeRowFromSelection(row)

    @pyqtSlot()
    def on_moveUpPushButton_clicked(self):
        """
        Method triggered when move row up button is clicked.
        """
        rows = self.selectedRows()
        if not rows:
            return
        for row in self.selectedRows():
            if row - 1 in rows:
                # rows is a copy of selected rows that is updated after the
                # item is moved
                continue
            self.moveRowUp(row)
            if row != 0:
                # this row is never aftected, hence it is "fixed"
                rows.remove(row)
        row = max(self.selectedRows())
        self.setCurrentButton(self.buttonFromRow(row))

    @pyqtSlot()
    def on_moveDownPushButton_clicked(self):
        """
        Method triggered when move row down button is clicked.
        """
        rows = self.selectedRows(True)
        if not rows:
            return
        lastRow = self.tableWidget.rowCount() - 1
        for row in self.selectedRows(True):
            if row + 1 in rows:
                continue
            self.moveRowDown(row)
            if row != lastRow:
                rows.remove(row)
        row = max(self.selectedRows())
        self.setCurrentButton(self.buttonFromRow(row))

    @pyqtSlot()
    def on_okPushButton_clicked(self):
        """
        Closes setup dialog and returns a confirmation code.
        :return: (int) confirmation code.
        """
        if not self.isValid():
            msg = self.tr("Invalid input data: {r}").format(r=self.validate())
            self.raiseWarning(msg)
            return
        msg = self.tr("Current button has been modified and not saved. Would "
                        "you like to save it?")
        title = self.tr("Unsaved modifications")
        if self.buttonIsModified() and self.confirmAction(msg, title):
            self.updateCurrentButton()
        self.setCurrentSetupName(self.setupName())
        self.setCurrentDescription(self.description())
        self.setCurrentDynamicShortcut(self.dynamicShortcut())
        self.done(1)

    @pyqtSlot()
    def on_cancelPushButton_clicked(self):
        """
        Closes setup dialog and returns a refusal code.
        :return: (int) confirmation code.
        """
        self.done(0)

    def state(self):
        """
        Exports current setup's state as read from the GUI.
        :return: (dict) a map to tool's current state.
        """
        state = self.readSetup().state()
        # buttons' keywords are stored as sets, which are not seriallizable
        for idx, props in enumerate(state["buttons"]):
            kws = props["keywords"]
            state["buttons"][idx]["keywords"] = tuple(kws)
        return {
            "state": state,
            "order": self.buttonsOrder()
        }

    def setState(self, state):
        """
        Restores the GUI to a given state.
        :param state: (dict) a map to tool's state.
        """
        self.setup.setState(state)

    @pyqtSlot(bool, name="on_importPushButton_clicked")
    def importSetup(self):
        """
        Imports a setup from a file.
        """
        fd = QFileDialog()
        filename = fd.getOpenFileName(
            caption=self.tr("Import a DSGTools Button Setup (set of buttons)"),
            filter=self.tr("DSGTools Buttons Setup (*.setup)")
        )
        filename = filename[0] if isinstance(filename, tuple) else filename
        if not filename:
            return
        with open(filename, "r", encoding="utf-8") as fp:
            state = json.load(fp)
            order = [b[0] for b in \
                        sorted(state["order"].items(), key=lambda i: i[1])]
            state = state["state"]
        # buttons' keywords are stored as tuple in order to be seriallizable
        for idx, props in enumerate(state["buttons"]):
            kws = props["keywords"]
            state["buttons"][idx]["keywords"] = set(kws)
            # tuples and list are misinterpreted when exported
            col = props["color"]
            state["buttons"][idx]["color"] = tuple(col)
        self.clear()
        self.setState(state)
        self.buttonComboBox.blockSignals(True)
        self.buttonComboBox.addItem(self.tr("No button selected"))
        self.buttonComboBox.addItems(order)
        for btn in order:
            self.addButtonToTable(self.setup.button(btn))
        self.buttonComboBox.blockSignals(False)
        if order:
            self.setCurrentButton(self.setup.button(order[0]))
        else:
            self.buttonComboBox.setCurrentIndex(0)
            self.setCurrentButton(None)
        self.setSetupName(self.setup.name())
        self.setDescription(self.setup.description())
        self.setDynamicShortcut(self.setup.dynamicShortcut())
        msg = self.tr('Setup "{0}" imported from "{1}"')\
                  .format(self.setup.name(), filename)
        self.raiseWarning(
            msg, title=self.tr("Imported workflow"), lvl=Qgis.Success)

    @pyqtSlot(bool, name="on_exportPushButton_clicked")
    def exportSetup(self):
        """
        Exports current setup's saved state to a file.
        :return: (bool) whether setup was exported.
        """
        if not self.isValid():
            msg = self.tr("Invalid input data: {r}").format(r=self.validate())
            self.raiseWarning(msg)
            return False
        # add check of modified button in here
        s = self.readSetup()
        fd = QFileDialog()
        filename = fd.getSaveFileName(
            caption=self.tr("Export setup - {0}").format(s.name()),
            filter=self.tr("DSGTools Buttons Setup (*.setup)")
        )
        filename = filename[0] if isinstance(filename, tuple) else filename
        if not filename:
            return False
        with open(filename, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(self.state(), sort_keys=True, indent=4))
        res = os.path.exists(filename)
        if res:
            msg = self.tr('Setup "{0}" exported to "{1}"')\
                      .format(s.name(), filename)
            self.raiseWarning(
                msg, title=self.tr("Exported workflow"), lvl=Qgis.Success)
        return res
