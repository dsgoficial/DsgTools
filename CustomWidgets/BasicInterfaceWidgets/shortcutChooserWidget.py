# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-09-12
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
# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtGui import QKeySequence

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'shortcutChooserWidget.ui'))

class ShortcutChooserWidget(QtGui.QWidget, FORM_CLASS):
    keyPressed = pyqtSignal()
    def __init__(self, parent=None):
        """
        Initializates ShortcutChooserWidget
        """
        super(ShortcutChooserWidget, self).__init__(parent)
        self.resetVariables()
        self.setupUi(self)
    
    @pyqtSlot(bool)
    def on_assignShortcutPushButton_clicked(self):
        """
        After button is clicked, focus is needed to use keyPressEvent and keyReleaseEvent
        """
        self.setFocus()
    
    @pyqtSlot(bool)
    def on_assignShortcutPushButton_toggled(self, toggled):
        """
        Button toggled reset self.modifiers and self.keys and also prepairs button text
        """
        if toggled:
            self.resetVariables()
            self.assignShortcutPushButton.setText(self.tr('Enter Value'))
    
    @pyqtSlot(bool)
    def on_clearPushButton_clicked(self):
        """
        Clears push button and also resets self.modifiers and self.keys
        """
        self.assignShortcutPushButton.setChecked(False)
        self.assignShortcutPushButton.setText(self.tr('Assign Shortcut'))
        self.resetVariables()
    
    def resetVariables(self):
        """
        Resets self.modifiers, self.key and self.keySequence to 0
        """
        self.modifiers = 0
        self.key = 0
        self.keySequence = 0

    def keyPressEvent(self, event):
        """
        """
        if not self.assignShortcutPushButton.isChecked():
            super(ShortcutChooserWidget, self).keyPressEvent(event)
            return
        key = int(event.key())
        if key == Qt.Key_Meta:
            self.modifiers |= Qt.META
            self.updateShortcutText()
        elif key == Qt.Key_Alt:
            self.modifiers |= Qt.ALT
            self.updateShortcutText()
        elif key == Qt.Key_Control:
            self.modifiers |= Qt.CTRL
            self.updateShortcutText()
        elif key == Qt.Key_Shift:
            self.modifiers |= Qt.SHIFT
            self.updateShortcutText()
        elif key == Qt.Key_Escape:
            self.assignShortcutPushButton.setChecked(False)
            return
        else:
            self.key = key
            self.updateShortcutText()

    def keyReleaseEvent(self, event):
        if not self.assignShortcutPushButton.isChecked():
            super(ShortcutChooserWidget, self).keyReleaseEvent(event)
            return
        key = event.key()
        if key == Qt.Key_Meta:
            self.modifiers &= Qt.META
            self.updateShortcutText()
        elif key == Qt.Key_Alt:
            self.modifiers &= Qt.ALT
            self.updateShortcutText()
        elif key == Qt.Key_Control:
            self.modifiers &= Qt.CTRL
            self.updateShortcutText()
        elif key == Qt.Key_Shift:
            self.modifiers &= Qt.SHIFT
            self.updateShortcutText()
        elif key == Qt.Key_Escape:
            return
        else:
            # self.setShortcut(QKeySequence(sum(self.modifiers)+self.key)) #each modifier is an int and the sum of modifiers is represented by a QKeySequence
            self.assignShortcutPushButton.setChecked(False)
            self.updateShortcutText()
            self.setShortcut(self.keySequence)
    
    def setShortcut(self, shortcut):
        self.keySequence = QKeySequence(shortcut)
        self.assignShortcutPushButton.setChecked(False)
        self.assignShortcutPushButton.setText(self.keySequence.toString(format = QKeySequence.NativeText))
    
    def getShortcut(self):
        return self.keySequence

    def updateShortcutText(self):
        self.keySequence = QKeySequence(self.modifiers+self.key)
        #this uses QKeySequence.NativeText to show in the interface. To store data, no filter should be provided
        self.assignShortcutPushButton.setText(self.tr('Input: {0}').format(self.keySequence.toString(format = QKeySequence.NativeText)))