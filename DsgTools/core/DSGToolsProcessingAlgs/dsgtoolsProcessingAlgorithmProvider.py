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
from .Algs.EditingAlgs.createEditingGridAlgorithm import (
    CreateEditingGridAlgorithm,
)
from .Algs.EnvironmentSetterAlgs.setFreeHandToolParametersAlgorithm import (
    SetFreeHandToolParametersAlgorithm,
)
from .Algs.GeometricAlgs.buildTerrainSlicingFromContoursAlgorihtm import (
    BuildTerrainSlicingFromContoursAlgorihtm,
)
from .Algs.GeometricAlgs.donutHoleExtractorAlgorithm import (
    DonutHoleExtractorAlgorithm,
)
from .Algs.GeometricAlgs.reclassifyAdjecentPolygonsAlgorithm import (
    ReclassifyAdjacentPolygonsAlgorithm,
)
from .Algs.GeometricAlgs.smallHoleRemoverAlgorithm import (
    SmallHoleRemoverAlgorithm,
)
from .Algs.LayerManagementAlgs.applyStylesFromDatabaseToLayersAlgorithm import (
    ApplyStylesFromDatabaseToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignActionsToLayersAlgorithm import (
    AssignActionsToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignAliasesToLayersAlgorithm import (
    AssignAliasesToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignBoundingBoxFilterToLayersAlgorithm import (
    AssignBoundingBoxFilterToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignConditionalStyleToLayersAlgorithm import (
    AssignConditionalStyleToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignCustomFormAndFormatRulesToLayersAlgorithm import (
    AssignCustomFormAndFormatRulesToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignDefaultFieldValueToLayersAlgorithm import (
    AssignDefaultFieldValueToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignExpressionFieldToLayersAlgorithm import (
    AssignExpressionFieldToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignFilterToLayersAlgorithm import (
    AssignFilterToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.assignFormatRulesToLayersAlgorithm import (
    AssignFormatRulesToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.detectNullGeometriesAlgorithm import (
    DetectNullGeometriesAlgorithm,
)
from .Algs.LayerManagementAlgs.assignMeasureColumnToLayersAlgorithm import (
    AssignMeasureColumnToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.lockAttributeEditingAlgorithm import (
    LockAttributeEditingAlgorithm,
)
from .Algs.LayerManagementAlgs.assignValueMapToLayersAlgorithm import (
    AssignValueMapToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.buildJoinsOnLayersAlgorithm import (
    BuildJoinsOnLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.groupLayersAlgorithm import (
    GroupLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.loadLayersFromPostgisAlgorithm import (
    LoadLayersFromPostgisAlgorithm,
)
from .Algs.LayerManagementAlgs.loadNonSpatialLayersFromPostgreSQLAlgorithm import (
    LoadNonSpatialLayersFromPostgreSQLAlgorithm,
)
from .Algs.LayerManagementAlgs.loadShapefileAlgorithm import (
    LoadShapefileAlgorithm,
)
from .Algs.LayerManagementAlgs.matchAndApplyQmlStylesToLayersAlgorithm import (
    MatchAndApplyQmlStylesToLayersAlgorithm,
)
from .Algs.LayerManagementAlgs.removeEmptyLayers import (
    RemoveEmptyLayers,
)
from .Algs.LayerManagementAlgs.spellCheckerAlgorithm import (
    SpellCheckerAlgorithm,
)
from .Algs.OtherAlgs.batchRunAlgorithm import (
    BatchRunAlgorithm,
)
from .Algs.OtherAlgs.convertLayer2LayerAlgorithm import (
    ConvertLayer2LayerAlgorithm,
)
from .Algs.OtherAlgs.createFrameAlgorithm import (
    CreateFrameAlgorithm,
)
from .Algs.OtherAlgs.createFramesWithConstraintAlgorithm import (
    CreateFramesWithConstraintAlgorithm,
)
from .Algs.OtherAlgs.filterLayerListByGeometryType import (
    FilterLayerListByGeometryType,
)
from .Algs.OtherAlgs.selectFeaturesOnCurrentCanvas import (
    SelectFeaturesOnCurrentCanvas,
)
from .Algs.ValidationAlgs.addUnsharedVertexOnIntersectionsAlgorithm import (
    AddUnsharedVertexOnIntersectionsAlgorithm,
)
from .Algs.ValidationAlgs.addUnsharedVertexOnSharedEdgesAlgorithm import (
    AddUnsharedVertexOnSharedEdgesAlgorithm,
)
from .Algs.ValidationAlgs.extendLinesToGeographicBoundsAlgorithm import (
    ExtendLinesToGeographicBoundsAlgorithm,
)
from .Algs.ValidationAlgs.streamOrder import StreamOrder
from .Algs.OtherAlgs.createReviewGridAlgorithm import CreateReviewGridAlgorithm
from .Algs.OtherAlgs.exportToMemoryLayer import (
    ExportToMemoryLayer,
)
from .Algs.OtherAlgs.fileInventoryAlgorithm import (
    FileInventoryAlgorithm,
)
from .Algs.OtherAlgs.pecCalculatorAlgorithm import (
    PecCalculatorAlgorithm,
)
from .Algs.OtherAlgs.raiseFlagsAlgorithm import (
    RaiseFlagsAlgorithm,
)
from .Algs.OtherAlgs.ruleStatisticsAlgorithm import (
    RuleStatisticsAlgorithm,
)
from .Algs.OtherAlgs.runFMESAPAlgorithm import (
    RunFMESAPAlgorithm,
)
from .Algs.OtherAlgs.runRemoteFMEAlgorithm import (
    ParameterFMEManagerType,
    RunRemoteFMEAlgorithm,
)
from .Algs.OtherAlgs.stringCsvToFirstLayerWithElementsAlgorithm import (
    StringCsvToFirstLayerWithElementsAlgorithm,
)
from .Algs.OtherAlgs.stringCsvToLayerListAlgorithm import (
    StringCsvToLayerListAlgorithm,
)
from .Algs.OtherAlgs.unicodeFilterAlgorithm import (
    UnicodeFilterAlgorithm,
)
from .Algs.OtherAlgs.updateOriginalLayerAlgorithm import (
    UpdateOriginalLayerAlgorithm,
)
from .Algs.ValidationAlgs.adjustNetworkConnectivityAlgorithm import (
    AdjustNetworkConnectivityAlgorithm,
)
from .Algs.ValidationAlgs.buildPolygonsFromCenterPointsAndBoundariesAlgorithm import (
    BuildPolygonsFromCenterPointsAndBoundariesAlgorithm,
)
from .Algs.ValidationAlgs.cleanGeometriesAlgorithm import (
    CleanGeometriesAlgorithm,
)
from .Algs.ValidationAlgs.createNetworkNodesAlgorithm import (
    CreateNetworkNodesAlgorithm,
)
from .Algs.ValidationAlgs.deaggregateGeometriesAlgorithm import (
    DeaggregatorAlgorithm,
)
from .Algs.ValidationAlgs.dissolvePolygonsWithSameAttributesAlgorithm import (
    DissolvePolygonsWithSameAttributesAlgorithm,
)
from .Algs.ValidationAlgs.enforceAttributeRulesAlgorithm import (
    EnforceAttributeRulesAlgorithm,
)
from .Algs.ValidationAlgs.enforceSpatialRulesAlgorithm import (
    EnforceSpatialRulesAlgorithm,
    ParameterSpatialRulesSetType,
)
from .Algs.ValidationAlgs.hierarchicalSnapLayerOnLayerAndUpdateAlgorithm import (
    HierarchicalSnapLayerOnLayerAndUpdateAlgorithm,
    ParameterSnapHierarchyType,
)
from .Algs.ValidationAlgs.identifyAndFixInvalidGeometriesAlgorithm import (
    IdentifyAndFixInvalidGeometriesAlgorithm,
)
from .Algs.ValidationAlgs.identifyAnglesInInvalidRangeAlgorithm import (
    IdentifyAnglesInInvalidRangeAlgorithm,
)
from .Algs.ValidationAlgs.identifyCountourStreamIntersectionAlgorithm import (
    IdentifyCountourStreamIntersectionAlgorithm,
)
from .Algs.ValidationAlgs.identifyDanglesAlgorithm import (
    IdentifyDanglesAlgorithm,
)
from .Algs.ValidationAlgs.identifyDrainageFlowIssuesWithOtherHydrographicClassesAlgorithm import (
    IdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm,
)
from .Algs.ValidationAlgs.identifyDrainageLoops import (
    IdentifyDrainageLoops,
)
from .Algs.ValidationAlgs.identifyNetworkConstructionIssuesAlgorithm import (
    IdentifyNetworkConstructionIssuesAlgorithm,
)
from .Algs.ValidationAlgs.identifyDuplicatedFeaturesAlgorithm import (
    IdentifyDuplicatedFeaturesAlgorithm,
)
from .Algs.ValidationAlgs.identifyDuplicatedGeometriesAlgorithm import (
    IdentifyDuplicatedGeometriesAlgorithm,
)
from .Algs.ValidationAlgs.identifyDuplicatedLinesBetweenLayersAlgorithm import (
    IdentifyDuplicatedLinesBetweenLayersAlgorithm,
)
from .Algs.ValidationAlgs.identifyDuplicatedPointsBetweenLayersAlgorithm import (
    IdentifyDuplicatedPointsBetweenLayersAlgorithm,
)
from .Algs.ValidationAlgs.identifyDuplicatedPolygonsBetweenLayersAlgorithm import (
    IdentifyDuplicatedPolygonsBetweenLayersAlgorithm,
)
from .Algs.ValidationAlgs.identifyDuplicatedVertexesAlgorithm import (
    IdentifyDuplicatedVertexesAlgorithm,
)
from .Algs.ValidationAlgs.identifyGapsAlgorithm import (
    IdentifyGapsAlgorithm,
)
from .Algs.ValidationAlgs.identifyGapsAndOverlapsInCoverageAlgorithm import (
    IdentifyGapsAndOverlapsInCoverageAlgorithm,
)
from .Algs.ValidationAlgs.identifyGeometriesWithLargeVertexDensityAlgorithm import (
    IdentifyGeometriesWithLargeVertexDensityAlgorithm,
)
from .Algs.ValidationAlgs.identifyInvalidUUIDsAlgorithm import (
    IdentifyInvalidUUIDsAlgorithm,
)
from .Algs.ValidationAlgs.identifyMultiPartGeometriesAlgorithm import (
    IdentifyMultiPartGeometriesAlgorithm,
)
from .Algs.ValidationAlgs.identifyUnmergedLinesWithSameAttributeSetAlgorithm import (
    IdentifyUnmergedLinesWithSameAttributeSetAlgorithm,
)
from .Algs.ValidationAlgs.identifyOutOfBoundsAnglesAlgorithm import (
    IdentifyOutOfBoundsAnglesAlgorithm,
)
from .Algs.ValidationAlgs.identifyOutOfBoundsAnglesInCoverageAlgorithm import (
    IdentifyOutOfBoundsAnglesInCoverageAlgorithm,
)
from .Algs.ValidationAlgs.identifyOverlapsAlgorithm import (
    IdentifyOverlapsAlgorithm,
)
from .Algs.ValidationAlgs.identifyPolygonSliverAlgorithm import (
    IdentifyPolygonSliverAlgorithm,
)
from .Algs.ValidationAlgs.identifyPolygonUndershoots import (
    IdentifyPolygonUndershootsAlgorithm,
)
from .Algs.ValidationAlgs.identifySmallFirstOrderDangle import (
    IdentifySmallFirstOrderDanglesAlgorithm,
)
from .Algs.ValidationAlgs.identifySmallHolesAlgorithm import (
    IdentifySmallHolesAlgorithm,
)
from .Algs.ValidationAlgs.identifySmallLinesAlgorithm import (
    IdentifySmallLinesAlgorithm,
)
from .Algs.ValidationAlgs.identifySmallPolygonsAlgorithm import (
    IdentifySmallPolygonsAlgorithm,
)

# from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.multipleOutputUnitTestAlgorithm import \
#     MultipleOutputUnitTestAlgorithm
from .Algs.ValidationAlgs.identifyTerrainModelErrorsAlgorithm import (
    IdentifyTerrainModelErrorsAlgorithm,
)
from .Algs.ValidationAlgs.identifyUnsharedVertexOnIntersectionsAlgorithm import (
    IdentifyUnsharedVertexOnIntersectionsAlgorithm,
)
from .Algs.ValidationAlgs.identifyUnsharedVertexOnSharedEdgesAlgorithm import (
    IdentifyUnsharedVertexOnSharedEdgesAlgorithm,
)
from .Algs.ValidationAlgs.identifyVertexNearEdgesAlgorithm import (
    IdentifyVertexNearEdgesAlgorithm,
)

# from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.singleOutputUnitTestAlgorithm import SingleOutputUnitTestAlgorithm
from .Algs.ValidationAlgs.identifyWrongBuildingAnglesAlgorithm import (
    IdentifyWrongBuildingAnglesAlgorithm,
)
from .Algs.ValidationAlgs.identifyZAnglesBetweenFeaturesAlgorithm import (
    identifyZAnglesBetweenFeaturesAlgorithm,
)
from .Algs.ValidationAlgs.lineOnLineOverlayerAlgorithm import (
    LineOnLineOverlayerAlgorithm,
)
from .Algs.ValidationAlgs.mergeLinesAlgorithm import (
    MergeLinesAlgorithm,
)
from .Algs.ValidationAlgs.overlayElementsWithAreasAlgorithm import (
    OverlayElementsWithAreasAlgorithm,
)
from .Algs.ValidationAlgs.removeDuplicatedFeaturesAlgorithm import (
    RemoveDuplicatedFeaturesAlgorithm,
)
from .Algs.ValidationAlgs.removeDuplicatedGeometriesAlgorithm import (
    RemoveDuplicatedGeometriesAlgorithm,
)
from .Algs.ValidationAlgs.removeEmptyAndUpdateAlgorithm import (
    RemoveEmptyAndUpdateAlgorithm,
)
from .Algs.ValidationAlgs.removeSmallLinesAlgorithm import (
    RemoveSmallLinesAlgorithm,
)
from .Algs.ValidationAlgs.removeSmallPolygonsAlgorithm import (
    RemoveSmallPolygonsAlgorithm,
)
from .Algs.ValidationAlgs.snapLayerOnLayerAndUpdateAlgorithm import (
    SnapLayerOnLayerAndUpdateAlgorithm,
)
from .Algs.ValidationAlgs.snapToGridAndUpdateAlgorithm import (
    SnapToGridAndUpdateAlgorithm,
)
from .Algs.ValidationAlgs.topologicalCleanAlgorithm import (
    TopologicalCleanAlgorithm,
)
from .Algs.ValidationAlgs.topologicalCleanLinesAlgorithm import (
    TopologicalCleanLinesAlgorithm,
)
from .Algs.ValidationAlgs.topologicalDouglasAreaSimplificationAlgorithm import (
    TopologicalDouglasPeuckerAreaSimplificationAlgorithm,
)
from .Algs.ValidationAlgs.topologicalDouglasLineSimplificationAlgorithm import (
    TopologicalDouglasPeuckerLineSimplificationAlgorithm,
)
from .Algs.ValidationAlgs.topologicalLineConnectivityAdjustmentAlgorithm import (
    TopologicalLineConnectivityAdjustment,
)
from .Algs.ValidationAlgs.unbuildPolygonsAlgorithm import (
    UnbuildPolygonsAlgorithm,
)
from .Algs.ValidationAlgs.verifyCountourStackingAlgorithm import (
    VerifyCountourStackingAlgorihtm,
)
from .Algs.ValidationAlgs.verifyNetworkDirectioningAlgorithm import (
    VerifyNetworkDirectioningAlgorithm,
)
from .Algs.ValidationAlgs.identifyDrainageFlowIssues import (
    IdentifyDrainageFlowIssues,
)
from .Algs.ValidationAlgs.identifyDrainageAngleIssues import (
    IdentifyDrainageAngleIssues,
)
from .Algs.LayerManagementAlgs.setRemoveDuplicateNodePropertyOnLayers import (
    SetRemoveDuplicateNodePropertyOnLayers,
)
from processing.core.ProcessingConfig import ProcessingConfig, Setting
from PyQt5.QtCore import QCoreApplication
from qgis.core import QgsApplication, QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon


class DSGToolsProcessingAlgorithmProvider(QgsProcessingProvider):
    """
    Constructor
    """

    snapHierarchyParameterName = QCoreApplication.translate(
        "Processing", "Snap Hierarchy"
    )
    fmeManagerParameterName = QCoreApplication.translate(
        "Processing", "FME Manager Parameters"
    )

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
            TopologicalDouglasPeuckerAreaSimplificationAlgorithm(),
            TopologicalDouglasPeuckerLineSimplificationAlgorithm(),
            RemoveDuplicatedGeometriesAlgorithm(),
            RemoveSmallLinesAlgorithm(),
            RemoveSmallPolygonsAlgorithm(),
            CleanGeometriesAlgorithm(),
            MergeLinesAlgorithm(),
            AssignExpressionFieldToLayersAlgorithm(),
            TopologicalCleanLinesAlgorithm(),
            SnapLayerOnLayerAndUpdateAlgorithm(),
            LineOnLineOverlayerAlgorithm(),
            DissolvePolygonsWithSameAttributesAlgorithm(),
            SnapToGridAndUpdateAlgorithm(),
            RemoveEmptyAndUpdateAlgorithm(),
            ConvertLayer2LayerAlgorithm(),
            OverlayElementsWithAreasAlgorithm(),
            CreateNetworkNodesAlgorithm(),
            AssignDefaultFieldValueToLayersAlgorithm(),
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
            AssignConditionalStyleToLayersAlgorithm(),
            AssignBoundingBoxFilterToLayersAlgorithm(),
            AssignMeasureColumnToLayersAlgorithm(),
            LockAttributeEditingAlgorithm(),
            GroupLayersAlgorithm(),
            TopologicalLineConnectivityAdjustment(),
            PecCalculatorAlgorithm(),
            RuleStatisticsAlgorithm(),
            MatchAndApplyQmlStylesToLayersAlgorithm(),
            ApplyStylesFromDatabaseToLayersAlgorithm(),
            # SingleOutputUnitTestAlgorithm(),
            ExportToMemoryLayer(),
            AssignCustomFormAndFormatRulesToLayersAlgorithm(),
            AssignValueMapToLayersAlgorithm(),
            LoadLayersFromPostgisAlgorithm(),
            LoadNonSpatialLayersFromPostgreSQLAlgorithm(),
            AssignAliasesToLayersAlgorithm(),
            AssignActionsToLayersAlgorithm(),
            BuildJoinsOnLayersAlgorithm(),
            BatchRunAlgorithm(),
            StringCsvToLayerListAlgorithm(),
            IdentifyWrongBuildingAnglesAlgorithm(),
            IdentifyVertexNearEdgesAlgorithm(),
            IdentifyUnsharedVertexOnSharedEdgesAlgorithm(),
            EnforceSpatialRulesAlgorithm(),
            UnbuildPolygonsAlgorithm(),
            IdentifyUnsharedVertexOnIntersectionsAlgorithm(),
            SetFreeHandToolParametersAlgorithm(),
            BuildPolygonsFromCenterPointsAndBoundariesAlgorithm(),
            # MultipleOutputUnitTestAlgorithm(),
            IdentifyTerrainModelErrorsAlgorithm(),
            CreateFramesWithConstraintAlgorithm(),
            IdentifyAnglesInInvalidRangeAlgorithm(),
            RunFMESAPAlgorithm(),
            EnforceAttributeRulesAlgorithm(),
            IdentifyPolygonSliverAlgorithm(),
            identifyZAnglesBetweenFeaturesAlgorithm(),
            IdentifySmallHolesAlgorithm(),
            IdentifyInvalidUUIDsAlgorithm(),
            VerifyCountourStackingAlgorihtm(),
            LoadShapefileAlgorithm(),
            IdentifyCountourStreamIntersectionAlgorithm(),
            SpellCheckerAlgorithm(),
            UnicodeFilterAlgorithm(),
            IdentifyNetworkConstructionIssuesAlgorithm(),
            IdentifySmallFirstOrderDanglesAlgorithm(),
            RemoveEmptyLayers(),
            IdentifyGeometriesWithLargeVertexDensityAlgorithm(),
            AssignFormatRulesToLayersAlgorithm(),
            DetectNullGeometriesAlgorithm(),
            IdentifyDuplicatedVertexesAlgorithm(),
            IdentifyMultiPartGeometriesAlgorithm(),
            IdentifyPolygonUndershootsAlgorithm(),
            IdentifyUnmergedLinesWithSameAttributeSetAlgorithm(),
            StringCsvToFirstLayerWithElementsAlgorithm(),
            IdentifyDrainageFlowIssues(),
            IdentifyDrainageAngleIssues(),
            BuildTerrainSlicingFromContoursAlgorihtm(),
            SetRemoveDuplicateNodePropertyOnLayers(),
            IdentifyDrainageLoops(),
            IdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm(),
            CreateReviewGridAlgorithm(),
            ExtendLinesToGeographicBoundsAlgorithm(),
            AddUnsharedVertexOnIntersectionsAlgorithm(),
            AddUnsharedVertexOnSharedEdgesAlgorithm(),
            SelectFeaturesOnCurrentCanvas(),
            FilterLayerListByGeometryType(),
            SmallHoleRemoverAlgorithm(),
            ReclassifyAdjacentPolygonsAlgorithm(),
            StreamOrder(),
        ]
        return algList

    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        # Activate provider by default
        ProcessingConfig.addSetting(
            Setting(self.name(), "ACTIVATE_DSGTools", "Activate", True)
        )
        ProcessingConfig.readSettings()
        self.parameterTypeSnapHierarchy = ParameterSnapHierarchyType()
        QgsApplication.instance().processingRegistry().addParameterType(
            self.parameterTypeSnapHierarchy
        )
        self.parameterTypeFMEManager = ParameterFMEManagerType()
        QgsApplication.instance().processingRegistry().addParameterType(
            self.parameterTypeFMEManager
        )
        self.parameterSpatialRulesSetType = ParameterSpatialRulesSetType()
        QgsApplication.instance().processingRegistry().addParameterType(
            self.parameterSpatialRulesSetType
        )
        self.refreshAlgorithms()
        return True

    def unload(self):
        """
        Removes setting when the plugin is unloaded.
        """
        ProcessingConfig.removeSetting("ACTIVATE_DSGTools")
        QgsApplication.instance().processingRegistry().removeParameterType(
            self.parameterTypeSnapHierarchy
        )
        QgsApplication.instance().processingRegistry().removeParameterType(
            self.parameterTypeFMEManager
        )
        QgsApplication.instance().processingRegistry().removeParameterType(
            self.parameterSpatialRulesSetType
        )

    def isActive(self):
        """
        Returns True if the provider is activated.
        """
        return ProcessingConfig.getSetting("ACTIVATE_DSGTools")

    def setActive(self, active):
        ProcessingConfig.setSettingValue("ACTIVATE_DSGTools", active)

    def id(self):
        """
        This is the name that will appear on the toolbox group.
        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return "dsgtools"

    def name(self):
        """
        This is the localised full name.
        """
        return "DSGTools"

    def icon(self):
        """
        We return the default icon.
        """
        return QIcon(":/plugins/DsgTools/icons/dsg.png")

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
