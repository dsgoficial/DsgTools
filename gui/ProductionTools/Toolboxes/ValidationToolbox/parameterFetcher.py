# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-07-16
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from __future__ import print_function
import os
from collections import deque, OrderedDict
from qgis.core import QgsMessageLog, Qgis, QgsTask, QgsApplication
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.processParametersDialog import ProcessParametersDialog
from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedRecursiveSnapWidget import OrderedRecursiveSnapWidget
from DsgTools.core.ValidationTools.ValidationProcesses.hierarchicalSnapLayerOnLayerProcess import HierarchicalSnapParameters

from qgis.PyQt.QtCore import Qt
from qgis.PyQt import QtGui
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QMenu
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.Qt import QObject

class ParameterFetcher(QObject):
    def __init__(self):
        """
        Constructor
        """
        super(ParameterFetcher, self).__init__()
        self.processAliasDict = {
            'Rules Setting' : {
                'alias': self.tr('Rules Setting'), 
                'type': deque
                },
            'Snap' : {
                'alias': self.tr('Snap'), 
                'type': float
                },
            'MinArea' : {
                'alias': self.tr('Minimum area'), 
                'type': float
                },
            'Layers' : {
                'alias': self.tr('Layers'), 
                'type': list
                },
            'Only Selected' : {
                'alias': self.tr('Only Selected'), 
                'type': bool
                },
            'MaxDissolveArea' : {
                'alias': self.tr('Maximum dissolved area'), 
                'type': float
                },
            'Ordered Layers' : {
                'alias': self.tr('Ordered Layers'), 
                'type': HierarchicalSnapParameters
                },
            'Ignore search radius on inner layer search' : {
                'alias': self.tr('Ignore search radius on inner layer search'), 
                'type': bool
                }
            'Layer and Filter Layers' : {
                'alias': self.tr('Ordered Layers'), 
                'type': OrderedDict
                },
            'Identification Type' : {
                'alias': self.tr('Identification Type'), 
                'type': deque
            },
            'Reference and Layers' : {
                'alias': self.tr('Reference and Layers'),
                'type' : OrderedDict
            },
            'Angle' : {
                'alias': self.tr('Reference and Layers'),
                'type' : float
            },
            'Only First Order Lines' : {
                'alias': self.tr('Only First Order Lines'),
                'type' : float
            }
            'Tolerance' : {
                'alias': self.tr('Tolerance'),
                'type' : float
            },
            'AttributeBlackList' : {
                'alias': self.tr('Attribute Black List (comma separated)'),
                'type' : str
            },
            'Overlayer and Layers' : {
                'alias': self.tr('Overlay layer and layers to be overlayed'),
                'type' : OrderedDict
            },
            'Overlay Type' : {
                'alias' : self.tr('Overlay type'),
                'type' : deque
            },
            'Coordinate Precision' : {
                'alias' : self.tr('Coordinate Precision'),
                'type' : float
            }
        }
    
    def fetch(self, processChain, parameterDict, restoreOverride = True):
        """
        Builds interface
        """
        processText = ', '.join([process.processAlias for process in processChain])
        dlgTitle = self.tr('Process parameters setter for process(es) {0}').format(processText)
        dlg = ProcessParametersDialog(None, parameterDict, title=dlgTitle, restoreOverride = restoreOverride)
        if dlg.exec_() == 0:
            return -1
        # get parameters
        params = dlg.values
        return params
    
