# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-05-31
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from typing import List, Optional, Union
from qgis.gui import QgsCheckableComboBox


class CustomCheckableComboBox(QgsCheckableComboBox):
    def __init__(self):
        super(CustomCheckableComboBox, self).__init__()

    def setData(
        self,
        items: Union[List[str], str],
        checkedItems: Optional[Union[List[str], str]] = None,
    ):
        itemList = items.split(",") if isinstance(items, str) else items
        self.addItems(itemList)
        if checkedItems is None:
            return
        checkedItemList = (
            checkedItems.split(",") if isinstance(checkedItems, str) else checkedItems
        )
        self.setCheckedItems(checkedItemList)
