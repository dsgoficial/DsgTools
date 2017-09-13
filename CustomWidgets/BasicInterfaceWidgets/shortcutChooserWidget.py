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

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'shortcutChooserWidget.ui'))

class ShortcutChooserWidget(QtGui.QWidget, FORM_CLASS):
    keyPressed = pyqtSignal()
    def __init__(self, parent=None):
        super(ShortcutChooserWidget, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(bool)
    def on_clearPushButton_clicked(self):
        self.assignShortcutPushButton.setChecked(False)

    def keyPressEvent(self, event):
        super(self.assignShortcutPushButton, self).keyReleaseEvent(event)
        if self.assignShortcutPushButton.isChecked():
            print 'pegou', event
            self.keyReleased.emit()
    
    def getShortcut(self):
        return ''