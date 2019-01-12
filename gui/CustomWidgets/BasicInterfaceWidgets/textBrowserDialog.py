# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-01-09
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog, QFileDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'textBrowserDialog.ui'))

class TextBrowserDialog(QDialog, FORM_CLASS):
    def __init__(self, html="", parent=None):
        """
        Class constructor.
        :param html:
        """
        super(TextBrowserDialog, self).__init__(parent=parent)
        self.parent = parent
        self.setupUi(self)
        self.setHtml(html)

    def setHtml(self, html):
        """
        Sets HTML text to GUI.
        :param html: (str) html text to be added.
        """
        self.textBrowser.setHtml(html)

    def addToHtml(self, textToAdd):
        """
        Appends text to existing one.
        :param textToAdd: (str) text to be added to GUI.
        """
        html = self.textBrowser.toHtml()
        self.textBrowser.setHtml(html + textToAdd)

    def clearHtml(self):
        """
        Clears text from GUI.
        """
        self.textBrowser.setHtml("")

    @pyqtSlot(bool, name='on_savePushButton_clicked')
    def saveHtml(self):
        """
        Exports text.
        :return: (str) output path.
        """
        html = self.textBrowser.toHtml()
        fd = QFileDialog()
        filename = fd.getSaveFileName(caption=self.tr('Select a Path to Log'),filter=self.tr('HTML Files (*.html)'))
        filename = filename[0] if isinstance(filename, tuple) else filename
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
        return filename

    @pyqtSlot(bool, name='on_closePushButton_clicked')
    def exit(self):
        """
        Closes dialog.
        """
        self.close()