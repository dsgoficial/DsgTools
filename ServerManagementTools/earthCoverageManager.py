# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
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
#General imports
from osgeo import ogr
from uuid import uuid4
import codecs, os, json, binascii

#DSG Tools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory 
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
from DsgTools.ServerManagementTools.genericDbManager import GenericDbManager
from DsgTools.Utils.utils import Utils

#PyQt4 imports
from PyQt4.Qt import QObject

class EarthCoverageManager(GenericDbManager):
    """
    This class manages the customizations on dsgtools databases.
    """
    def __init__(self, serverAbstractDb, dbDict, edgvVersion, parentWidget = None):
        super(self.__class__,self).__init__(serverAbstractDb, dbDict, edgvVersion, parentWidget = None)

    def materializeIntoDatabase(self, abstractDb):
        """
        Method that is reimplemented in each child when installing a property involves changing any sort of database structure
        """
        pass
    
    def undoMaterializationFromDatabase(self, abstractDb):
        """
        Method that is reimplemented in each child when uninstalling a property involves changing any sort of database structure
        """
        pass