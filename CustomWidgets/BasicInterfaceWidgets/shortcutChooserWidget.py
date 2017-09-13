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
        super(ShortcutChooserWidget, self).__init__(parent)
        self.modifiers = []
        self.key = 0
        self.setupUi(self)
    
    @pyqtSlot(bool)
    def on_assignShortcutPushButton_clicked(self):
        self.setFocus()
    
    @pyqtSlot(bool)
    def on_assignShortcutPushButton_toggled(self, toggled):
        self.modifiers = []
        self.key = 0
        if toggled:
            self.assignShortcutPushButton.setText(self.tr('Enter Value'))
    
    @pyqtSlot(bool)
    def on_clearPushButton_clicked(self):
        self.assignShortcutPushButton.setChecked(False)
        self.assignShortcutPushButton.setText(self.tr('Assign Shortcut'))

    def keyPressEvent(self, event):
        if not self.assignShortcutPushButton.isChecked():
            super(ShortcutChooserWidget, self).keyPressEvent(event)
            return
        key = event.key()
        modifier = event.modifiers()
        if modifier in [Qt.ControlModifier, Qt.ShiftModifier, Qt.AltModifier, Qt.Key_Meta]:
            if modifier not in self.modifiers:
                self.modifiers.append(modifier)
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
        modifiers = event.modifiers()
        if modifiers in [Qt.ControlModifier, Qt.ShiftModifier, Qt.AltModifier, Qt.Key_Meta]:
            if modifiers not in self.modifiers:
                self.modifiers.append(modifiers)
                self.updateShortcutText()
        elif key == Qt.Key_Escape:
            return
        else:
            self.setShortcut(QKeySequence(sum(self.modifiers)+self.key)) #each modifier is an int and the sum of modifiers is represented by a QKeySequence
            self.assignShortcutPushButton.setChecked(False)
    
    def setShortcut(self, shortcut):
        pass

    def updateShortcutText(self):
        keySequence = QKeySequence(sum(map(int,self.modifiers))+self.key)
        self.assignShortcutPushButton.setText(self.tr('Input: {0}').format(keySequence.toString()))