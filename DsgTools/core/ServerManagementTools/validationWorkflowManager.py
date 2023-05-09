# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-24
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
# General imports
from osgeo import ogr
from uuid import uuid4
import codecs, os, json, binascii

# DSG Tools imports
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.ServerManagementTools.genericDbManager import GenericDbManager
from DsgTools.core.Utils.utils import Utils

# qgis.PyQt imports
from qgis.PyQt.Qt import QObject


class ValidationWorkflowManager(GenericDbManager):
    """
    This class manages the customizations on dsgtools databases.
    """

    def __init__(self, serverAbstractDb, dbDict, edgvVersion, parentWidget=None):
        super(ValidationWorkflowManager, self).__init__(
            serverAbstractDb, dbDict, edgvVersion, parentWidget=None
        )

    def validateJsonProfile(self, inputJsonDict):
        """
        1. Validates each key and value in inputJsonDict;
        2. If input is ok, returns True;
        3. If one piece of json is not valid, returns False.
        This validator does not validate the name of classes or names of categories. It only checks the format of dsgtools json profile.
        """
        # TODO
        return True
