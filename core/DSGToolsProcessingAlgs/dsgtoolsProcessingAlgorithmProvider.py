# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-07-26
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
from PyQt5.QtCore import QCoreApplication

from core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.buildJoinsOnLayersAlgorithm import \
    BuildJoinsOnLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.EditingAlgs.createEditingGridAlgorithm import \
    CreateEditingGridAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.donutHoleExtractorAlgorithm import \
    DonutHoleExtractorAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.applyStylesFromDatabaseToLayersAlgorithm import \
    ApplyStylesFromDatabaseToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignAliasesToLayersAlgorithm import \
    AssignAliasesToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignBoundingBoxFilterToLayersAlgorithm import \
    AssignBoundingBoxFilterToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignFilterToLayersAlgorithm import \
    AssignFilterToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignCustomFormAndFormatRulesToLayersAlgorithm import \
    AssignCustomFormAndFormatRulesToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignMeasureColumnToLayersAlgorithm import \
    AssignMeasureColumnToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignValueMapToLayersAlgorithm import \
    AssignValueMapToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.buildJoinsOnLayersAlgorithm import \
    BuildJoinsOnLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.groupLayersAlgorithm import \
    GroupLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.loadLayersFromPostgisAlgorithm import \
    LoadLayersFromPostgisAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.loadNonSpatialLayersFromPostgreSQLAlgorithm import \
    LoadNonSpatialLayersFromPostgreSQLAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.matchAndApplyQmlStylesToLayersAlgorithm import \
    MatchAndApplyQmlStylesToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.convertLayer2LayerAlgorithm import \
    ConvertLayer2LayerAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.createFrameAlgorithm import \
    CreateFrameAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.exportToMemoryLayer import \
    ExportToMemoryLayer
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.fileInventoryAlgorithm import \
    FileInventoryAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.pecCalculatorAlgorithm import \
    PecCalculatorAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.raiseFlagsAlgorithm import \
    RaiseFlagsAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.ruleStatisticsAlgorithm import \
    RuleStatisticsAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.runRemoteFMEAlgorithm import (
    ParameterFMEManagerType, RunRemoteFMEAlgorithm)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.singleOutputUnitTestAlgorithm import \
    SingleOutputUnitTestAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.updateOriginalLayerAlgorithm import \
    UpdateOriginalLayerAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.adjustNetworkConnectivityAlgorithm import \
    AdjustNetworkConnectivityAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.cleanGeometriesAlgorithm import \
    CleanGeometriesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.createNetworkNodesAlgorithm import \
    CreateNetworkNodesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.deaggregateGeometriesAlgorithm import \
    DeaggregatorAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.dissolvePolygonsWithSameAttributesAlgorithm import \
    DissolvePolygonsWithSameAttributesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.hierarchicalSnapLayerOnLayerAndUpdateAlgorithm import (
    HierarchicalSnapLayerOnLayerAndUpdateAlgorithm, ParameterSnapHierarchyType)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyAndFixInvalidGeometriesAlgorithm import \
    IdentifyAndFixInvalidGeometriesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDanglesAlgorithm import \
    IdentifyDanglesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedFeaturesAlgorithm import \
    IdentifyDuplicatedFeaturesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedGeometriesAlgorithm import \
    IdentifyDuplicatedGeometriesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedLinesBetweenLayersAlgorithm import \
    IdentifyDuplicatedLinesBetweenLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedPointsBetweenLayersAlgorithm import \
    IdentifyDuplicatedPointsBetweenLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedPolygonsBetweenLayersAlgorithm import \
    IdentifyDuplicatedPolygonsBetweenLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyGapsAlgorithm import \
    IdentifyGapsAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyGapsAndOverlapsInCoverageAlgorithm import \
    IdentifyGapsAndOverlapsInCoverageAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyOutOfBoundsAnglesAlgorithm import \
    IdentifyOutOfBoundsAnglesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyOutOfBoundsAnglesInCoverageAlgorithm import \
    IdentifyOutOfBoundsAnglesInCoverageAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyOverlapsAlgorithm import \
    IdentifyOverlapsAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySmallLinesAlgorithm import \
    IdentifySmallLinesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySmallPolygonsAlgorithm import \
    IdentifySmallPolygonsAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.lineOnLineOverlayerAlgorithm import \
    LineOnLineOverlayerAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.mergeLinesAlgorithm import \
    MergeLinesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.overlayElementsWithAreasAlgorithm import \
    OverlayElementsWithAreasAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeDuplicatedFeaturesAlgorithm import \
    RemoveDuplicatedFeaturesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeDuplicatedGeometriesAlgorithm import \
    RemoveDuplicatedGeometriesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeEmptyAndUpdateAlgorithm import \
    RemoveEmptyAndUpdateAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeSmallLinesAlgorithm import \
    RemoveSmallLinesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeSmallPolygonsAlgorithm import \
    RemoveSmallPolygonsAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.snapLayerOnLayerAndUpdateAlgorithm import \
    SnapLayerOnLayerAndUpdateAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.snapToGridAndUpdateAlgorithm import \
    SnapToGridAndUpdateAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalCleanAlgorithm import \
    TopologicalCleanAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalCleanLinesAlgorithm import \
    TopologicalCleanLinesAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalDouglasSimplificationAlgorithm import \
    TopologicalDouglasSimplificationAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalLineConnectivityAdjustmentAlgorithm import \
    TopologicalLineConnectivityAdjustment
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.verifyNetworkDirectioningAlgorithm import \
    VerifyNetworkDirectioningAlgorithm

from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.batchRunAlgorithm import \
    BatchRunAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.stringCsvToLayerListAlgorithm import \
    StringCsvToLayerListAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.runRemoteFMEAlgorithm import \
    RunRemoteFMEAlgorithm, ParameterFMEManagerType
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.createFrameAlgorithm import \
    CreateFrameAlgorithm

from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.fileInventoryAlgorithm import \
    FileInventoryAlgorithm

from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.raiseFlagsAlgorithm import \
    RaiseFlagsAlgorithm

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyAndFixInvalidGeometriesAlgorithm import \
    IdentifyAndFixInvalidGeometriesAlgorithm

from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.pecCalculatorAlgorithm import PecCalculatorAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.matchAndApplyQmlStylesToLayersAlgorithm import \
    MatchAndApplyQmlStylesToLayersAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.applyStylesFromDatabaseToLayersAlgorithm import \
    ApplyStylesFromDatabaseToLayersAlgorithm

from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.singleOutputUnitTestAlgorithm import SingleOutputUnitTestAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyWrongBuildingAnglesAlgorithm import \
    IdentifyWrongBuildingAnglesAlgorithm

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyVertexNearEdgeOnPolygonsAlgorithm import \
    IdentifyVertexNearEdgeOnPolygonsAlgorithm

from processing.core.ProcessingConfig import ProcessingConfig, Setting
from qgis.core import QgsApplication, QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon


class DSGToolsProcessingAlgorithmProvider(QgsProcessingProvider):
    """
    Constructor
    """
    snapHierarchyParameterName = QCoreApplication.translate('Processing', 'Snap Hierarchy')
    fmeManagerParameterName = QCoreApplication.translate('Processing', 'FME Manager Parameters')
    def __init__(self):
        super(DSGToolsProcessingAlgorithmProvider, self).__init__()
    
    def getAlgList(self):
        algList = [
                    DeaggregatorAlgorithm(), 
                    IdentifySmallPolygonsAlgorithm(), 
                    IdentifySmallLinesAlgorithm(), 
                    IdentifyDuplicatedGeometriesAlgorithm(),
                    IdentifyOutOfBoundsAnglesAlgorithm(),
                    IdentifyOutOfBoundsAnglesInCoverageAlgorithm(),
                    IdentifyOverlapsAlgorithm(),
                    IdentifyGapsAndOverlapsInCoverageAlgorithm(),
                    IdentifyDanglesAlgorithm(),
                    IdentifyGapsAlgorithm(),
                    DonutHoleExtractorAlgorithm(),
                    UpdateOriginalLayerAlgorithm(),
                    TopologicalCleanAlgorithm(),
                    TopologicalDouglasSimplificationAlgorithm(),
                    RemoveDuplicatedGeometriesAlgorithm(),
                    RemoveSmallLinesAlgorithm(),
                    RemoveSmallPolygonsAlgorithm(),
                    CleanGeometriesAlgorithm(),
                    MergeLinesAlgorithm(),
                    TopologicalCleanLinesAlgorithm(),
                    SnapLayerOnLayerAndUpdateAlgorithm(),
                    LineOnLineOverlayerAlgorithm(),
                    DissolvePolygonsWithSameAttributesAlgorithm(),
                    SnapToGridAndUpdateAlgorithm(),
                    RemoveEmptyAndUpdateAlgorithm(),
                    ConvertLayer2LayerAlgorithm(),
                    OverlayElementsWithAreasAlgorithm(),
                    CreateNetworkNodesAlgorithm(),
                    VerifyNetworkDirectioningAlgorithm(),
                    IdentifyDuplicatedFeaturesAlgorithm(),
                    AdjustNetworkConnectivityAlgorithm(),
                    RemoveDuplicatedFeaturesAlgorithm(),
                    HierarchicalSnapLayerOnLayerAndUpdateAlgorithm(),
                    IdentifyDuplicatedPolygonsBetweenLayersAlgorithm(),
                    IdentifyDuplicatedLinesBetweenLayersAlgorithm(),
                    IdentifyDuplicatedPointsBetweenLayersAlgorithm(),
                    RunRemoteFMEAlgorithm(),
                    CreateFrameAlgorithm(),
                    FileInventoryAlgorithm(),
                    RaiseFlagsAlgorithm(),
                    IdentifyAndFixInvalidGeometriesAlgorithm(),
                    CreateEditingGridAlgorithm(),
                    AssignFilterToLayersAlgorithm(),
                    AssignBoundingBoxFilterToLayersAlgorithm(),
                    AssignMeasureColumnToLayersAlgorithm(),
                    GroupLayersAlgorithm(),
                    TopologicalLineConnectivityAdjustment(),
                    PecCalculatorAlgorithm(),
                    RuleStatisticsAlgorithm(),
                    MatchAndApplyQmlStylesToLayersAlgorithm(),
                    ApplyStylesFromDatabaseToLayersAlgorithm(),
                    SingleOutputUnitTestAlgorithm(),
                    ExportToMemoryLayer(),
                    AssignCustomFormAndFormatRulesToLayersAlgorithm(),
                    AssignValueMapToLayersAlgorithm(),
                    LoadLayersFromPostgisAlgorithm(),
                    LoadNonSpatialLayersFromPostgreSQLAlgorithm(),
                    AssignAliasesToLayersAlgorithm(),
                    BuildJoinsOnLayersAlgorithm(),
                    BatchRunAlgorithm(),
                    StringCsvToLayerListAlgorithm(),
                    IdentifyWrongBuildingAnglesAlgorithm(),
                    IdentifyVertexNearEdgeOnPolygonsAlgorithm()
                ]
        return algList


    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        # Activate provider by default
        ProcessingConfig.addSetting(Setting(self.name(), 'ACTIVATE_DSGTools',
                                            'Activate', True))
        ProcessingConfig.readSettings()
        self.parameterTypeSnapHierarchy = ParameterSnapHierarchyType()
        QgsApplication.instance().processingRegistry().addParameterType(self.parameterTypeSnapHierarchy)
        self.parameterTypeFMEManager = ParameterFMEManagerType()
        QgsApplication.instance().processingRegistry().addParameterType(self.parameterTypeFMEManager)
        self.refreshAlgorithms()
        return True

    def unload(self):
        """
        Removes setting when the plugin is unloaded.
        """
        ProcessingConfig.removeSetting('ACTIVATE_DSGTools')
        QgsApplication.instance().processingRegistry().removeParameterType(self.parameterTypeSnapHierarchy)
        QgsApplication.instance().processingRegistry().removeParameterType(self.parameterTypeFMEManager)

    def isActive(self):
        """
        Returns True if the provider is activated.
        """
        return ProcessingConfig.getSetting('ACTIVATE_DSGTools')

    def setActive(self, active):
        ProcessingConfig.setSettingValue('ACTIVATE_DSGTools', active)

    def id(self):
        """
        This is the name that will appear on the toolbox group.
        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return 'dsgtools'

    def name(self):
        """
        This is the localised full name.
        """
        return 'DSGTools'

    def icon(self):
        """
        We return the default icon.
        """
        return QIcon(':/plugins/DsgTools/icons/dsg.png')

    def loadAlgorithms(self):
        """
        Here we fill the list of algorithms in self.algs.
        This method is called whenever the list of algorithms should
        be updated. If the list of algorithms can change (for instance,
        if it contains algorithms from user-defined scripts and a new
        script might have been added), you should create the list again
        here.
        In this case, since the list is always the same, we assign from
        the pre-made list. This assignment has to be done in this method
        even if the list does not change, since the self.algs list is
        cleared before calling this method.
        """
        for alg in self.getAlgList():
            self.addAlgorithm(alg)
