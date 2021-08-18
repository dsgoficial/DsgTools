# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-31
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
#DsgTools imports
from builtins import object
from DsgTools.core.Factories.DbCustomizationFactory.attributeCustomization import AttributeCustomization
from DsgTools.core.Factories.DbCustomizationFactory.classCustomization import ClassCustomization
from DsgTools.core.Factories.DbCustomizationFactory.codeNameCustomization import CodeNameCustomization
from DsgTools.core.Factories.DbCustomizationFactory.defaultCustomization import DefaultCustomization
from DsgTools.core.Factories.DbCustomizationFactory.newDomainTableCustomization import NewDomainTableCustomization
from DsgTools.core.Factories.DbCustomizationFactory.domainValueCustomization import DomainValueCustomization
from DsgTools.core.Factories.DbCustomizationFactory.nullityCustomization import NullityCustomization
from DsgTools.core.Factories.DbCustomizationFactory.filterCustomization import FilterCustomization


class DbCustomizationFactory(object):
    def createCustomization(self, type, validatedJSONDict):
        if type == 'attribute':
            return AttributeCustomization(validatedJSONDict)
        elif type == 'class':
            return ClassCustomization(validatedJSONDict)
        elif type == 'codeName':
            return CodeNameCustomization(validatedJSONDict)
        elif type == 'default':
            return DefaultCustomization(validatedJSONDict)        
        elif type == 'domain':
            return NewDomainTableCustomization(validatedJSONDict)
        elif type == 'domainValue':
            return DomainValueCustomization(validatedJSONDict)
        elif type == 'nullity':
            return NullityCustomization(validatedJSONDict)
        elif type == 'filter':
            return FilterCustomization(validatedJSONDict)
        else:
            raise Exception(self.tr('Customization type not defined.'))
