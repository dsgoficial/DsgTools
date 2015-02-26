# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mosaicTools import Ui_Dialog

class MosaicTools(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor."""
        super(MosaicTools, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        print "foi"
        
    @pyqtSlot()
    def on_procuraSRButton_clicked(self):
        print "procuraSR"
        
    @pyqtSlot()
    def on_addButton_clicked(self):
        print "addButton"
        
    @pyqtSlot()
    def on_removeButton_clicked(self):
        print "removeButton"
        
    @pyqtSlot()
    def on_addFolderButton_clicked(self):
        print "addFolderButton"
    
    @pyqtSlot()
    def on_outputFolderButton_clicked(self):
        print "outputFolderButton"
    
    
