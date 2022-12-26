# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-05-14
        git sha              : $Format:%H$
        copyright            : (C) 2020 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

"""
Module designed to centralize the access to DSGTools tools.
This module CANNOT be imported at the beginning of modules and must be called
from within methods that are NOT the __init__!
"""

from DsgTools import dsgTools

mapToolManager = dsgTools.guiManager.productionToolsGuiManager.mapToolsGuiManager
toolBoxManager = dsgTools.guiManager.productionToolsGuiManager.toolBoxesGuiManager
toolBarManager = dsgTools.guiManager.productionToolsGuiManager.toolbarsGuiManager


def mapToolsNames():
    """
    Lists all non-i18n names for DSGTools map tools.
    :return: (list-of-str) list of non-i18n of all available map tools.
    """
    return [
        "genericTool",
        "flipLineTool",
        "acquisition",
        "freeHandAcquisiton",
        "freeHandReshape",
        "labelTool",
        "shortcutsTool",
    ]


def mapTools():
    """
    Lists all available map tools provided by DSGTools plugin.
    :return: (list-of-QgsMapTools) DSGTools map tools.
    """
    return [getattr(mapToolManager, tn) for tn in mapToolsNames()]


def mapTool(name):
    """
    Provides the map tool from DSGTools plugin through its non-i18n name.
    :param name: (str) non-i18n tool name.
    :return: (*QgsMapTools) target DSGTools map tool.
    """
    return getattr(mapToolManager, name)


def toolBarsNames():
    """
    Lists all non-i18n names for DSGTools tool bars.
    :return: (list-of-str) list of non-i18n of all available tool bars.
    """
    return [
        "minimumAreaTool",
        "inspectFeaturesTool",
        "styleManagerTool",
        "rasterInfoTool",
        "dataValidationTool",
    ]


def toolBars():
    """
    Lists all available tool bars provided by DSGTools plugin.
    :return: (list-of-QgsMapTools) DSGTools tool bars.
    """
    return [getattr(toolBarManager, tn) for tn in toolBarsNames()]


def toolBar(name):
    """
    Provides the tool bar from DSGTools plugin through its non-i18n name.
    :param name: (str) non-i18n tool name.
    :return: (list-of-*QToolBar) target DSGTools tool bar.
    """
    return getattr(toolBarManager, name)


def toolBoxesNames():
    """
    Lists all non-i18n names for DSGTools tool boxes.
    :return: (list-of-str) list of non-i18n of all available tool boxes.
    """
    return ["qaToolBox", "cfToolbox", "calcContour", "codeList", "complexWindow"]


def toolBoxes():
    """
    Lists all available tool boxes provided by DSGTools plugin.
    :return: (list-of-QgsMapTools) DSGTools tool boxes.
    """
    return [getattr(toolBoxManager, tn) for tn in toolBoxesNames()]


def toolBox(name):
    """
    Provides the tool bar from DSGTools plugin through its non-i18n name.
    :param name: (str) non-i18n tool name.
    :return: (list-of-*QToolBar) target DSGTools tool bar.
    """
    return getattr(toolBoxManager, name)


def toolsNames():
    """
    Lists all non-i18n names for DSGTools tools.
    :return: (list-of-str) list of non-i18n of all available tools.
    """
    return mapToolsNames() + toolBarsNames() + toolBoxesNames()


def tools():
    """
    List of all available DSGTools tools.
    :return: (list-of-*) all DSGTools map tools, tool boxes and tool bars.
    """
    return mapTools() + toolBars() + toolBoxes()


def toolByName(name):
    """
    Retrieve any of DSGTools its name.
    :param name: (str) non-i18n tool name.
    :return: (QgsMapTool/QgsToolBar/QgsToolBox?) target DSGTools tool.
    """
    if name in mapToolsNames():
        return mapTool(name)
    elif name in toolBarsNames():
        return toolBar(name)
    else:
        return toolBox(name)


def actions():
    """
    Retrieves all registered action on GuiManager.
    :return: (list-of-QAction) all registered actions related to DSGTools tools
    """
    return dsgTools.guiManager.actions
