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

from DsgTools.core.DSGToolsProcessingAlgs.Algs.DataManagementAlgs.clipAndCopyFeaturesBetweenDatabasesAlgorithm import (
    ClipAndCopyFeaturesBetweenDatabasesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.EnvironmentSetterAlgs.genericSelectionToolParametersAlgorithm import (
    GenericSelectionToolParametersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.EnvironmentSetterAlgs.rightAngleToolParametersAlgorithm import (
    RightAngleToolParametersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.DataManagementAlgs.appendFeaturesToLayerAlgorithm import (
    AppendFeaturesToLayerAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.findSmallClosedLinesAlgorithm import (
    FindSmallClosedLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeNetworkEdgesFromLengthAlgorithm import (
    GeneralizeNetworkEdgesWithLengthAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeWaterBodyAlgorithm import (
    GeneralizeWaterBodyAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.reclassifyGroupsOfPixelsToNearestNeighborAlgorithm import (
    ReclassifyGroupsOfPixelsToNearestNeighborAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.reclassifyPixelsToNearestNeighborAlgorithm import (
    ReclassifyAdjacentPixelsToNearestNeighborAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.runReclassifyPixelsWithSlidingWindow import (
    ReclassifyGroupsOfPixelsToNearestNeighborWithSlidingWindowAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.setLineOrientation import (
    SetLineOrientation,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.buildZipPackagesAlgorithm import (
    BuildZipPackageAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.batchRunAlgorithmWithGeographicBoundsConstraint import (
    BatchRunAlgorithmWithGeographicBoundsConstraint,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.createGridFromCoordinatesAlgorithm import (
    CreateGridFromCoordinatesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.RasterAlgs.batchRasterPackagingForBDGEx import (
    BatchRasterPackagingForBDGEx,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.fixSegmentErrorsBetweenLinesAlgorithm import (
    FixSegmentErrorsBetweenLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySmallObjectsOnLayersAlgorithm import (
    IdentifySmallObjectsOnLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyUncoveredStartAndEndPointsAlgorithm import (
    IdentifyUncoveredStartAndEndPointsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyWaterBodyAndContourInconsistencies import (
    IdentifyWaterBodyAndContourInconsistencies,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeDuplicateNodesAlgorithm import (
    RemoveDuplicateVertexesAlgorithm,
)
from processing.core.ProcessingConfig import ProcessingConfig, Setting
from PyQt5.QtCore import QCoreApplication
from qgis.core import QgsApplication, QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from DsgTools.core.DSGToolsProcessingAlgs.Algs.EditingAlgs.createEditingGridAlgorithm import (
    CreateEditingGridAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.EnvironmentSetterAlgs.setFreeHandToolParametersAlgorithm import (
    SetFreeHandToolParametersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.donutHoleExtractorAlgorithm import (
    DonutHoleExtractorAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.extractByDE9IM import (
    ExtractByDE9IMAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.extractElevationPoints import (
    ExtractElevationPoints,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeEdificationsAlgorithm import (
    GeneralizeEdificationsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeEdificationsAreaAlgorithm import (
    GeneralizeEdificationsAreaAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeLandingStrip import (
    GeneralizeLandingStripAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeRoundaboutsAlgorithm import (
    GeneralizeRoundaboutsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.generalizeHighwaysAlgorithm import (
    GeneralizeHighwaysAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.line2Multiline import (
    Line2Multiline,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.reclassifyAdjecentPolygonsAlgorithm import (
    ReclassifyAdjacentPolygonsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.selectByDE9IM import (
    SelectByDE9IMAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeometricAlgs.smallHoleRemoverAlgorithm import (
    SmallHoleRemoverAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.splitPolygonsAlgorithm import (
    SplitPolygons,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.GeneralizationAlgs.splitPolygonsByGrid import (
    SplitPolygonsByGrid,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.applyStylesFromDatabaseToLayersAlgorithm import (
    ApplyStylesFromDatabaseToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignActionsToLayersAlgorithm import (
    AssignActionsToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignAliasesToLayersAlgorithm import (
    AssignAliasesToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignBoundingBoxFilterToLayersAlgorithm import (
    AssignBoundingBoxFilterToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignConditionalStyleToLayersAlgorithm import (
    AssignConditionalStyleToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignCustomFormAndFormatRulesToLayersAlgorithm import (
    AssignCustomFormAndFormatRulesToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignDefaultFieldValueToLayersAlgorithm import (
    AssignDefaultFieldValueToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignExpressionFieldToLayersAlgorithm import (
    AssignExpressionFieldToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignFilterToLayersAlgorithm import (
    AssignFilterToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignFormatRulesToLayersAlgorithm import (
    AssignFormatRulesToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignMeasureColumnToLayersAlgorithm import (
    AssignMeasureColumnToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.assignValueMapToLayersAlgorithm import (
    AssignValueMapToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.buildJoinsOnLayersAlgorithm import (
    BuildJoinsOnLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.groupLayersAlgorithm import (
    GroupLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.loadLayersFromPostgisAlgorithm import (
    LoadLayersFromPostgisAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.loadNonSpatialLayersFromPostgreSQLAlgorithm import (
    LoadNonSpatialLayersFromPostgreSQLAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.loadRasterLayerFromServerAlgorithm import (
    LoadRasterLayerFromServerAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.loadShapefileAlgorithm import (
    LoadShapefileAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.lockAttributeEditingAlgorithm import (
    LockAttributeEditingAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.matchAndApplyQmlStylesToLayersAlgorithm import (
    MatchAndApplyQmlStylesToLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.removeEmptyLayers import (
    RemoveEmptyLayers,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.setRemoveDuplicateNodePropertyOnLayers import (
    SetRemoveDuplicateNodePropertyOnLayers,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.batchRunAlgorithm import (
    BatchRunAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.convertLayer2LayerAlgorithm import (
    ConvertLayer2LayerAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.createFrameAlgorithm import (
    CreateFrameAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.createFramesWithConstraintAlgorithm import (
    CreateFramesWithConstraintAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.createReviewGridAlgorithm import (
    CreateReviewGridAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.filterLayerListByGeometryType import (
    FilterLayerListByGeometryType,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.selectFeaturesOnCurrentCanvas import (
    SelectFeaturesOnCurrentCanvas,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.azimuthCalculationAlgorithm import (
    AzimuthCalculationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.exportFeaturesByAttributeAlgorithm import (
    ExportFeaturesByAttributeAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.addUnsharedVertexOnIntersectionsAlgorithm import (
    AddUnsharedVertexOnIntersectionsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.addUnsharedVertexOnSharedEdgesAlgorithm import (
    AddUnsharedVertexOnSharedEdgesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.extendLinesToGeographicBoundsAlgorithm import (
    ExtendLinesToGeographicBoundsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.fixDrainageFlowAlgorithm import (
    FixDrainageFlowAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.exportToMemoryLayer import (
    ExportToMemoryLayer,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.fileInventoryAlgorithm import (
    FileInventoryAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.filterLayerListByGeometryType import (
    FilterLayerListByGeometryType,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.loadTrackerAlgorithm import (
    LoadTrackerAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.pecCalculatorAlgorithm import (
    PecCalculatorAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.raiseFlagsAlgorithm import (
    RaiseFlagsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.ruleStatisticsAlgorithm import (
    RuleStatisticsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.runFMESAPAlgorithm import (
    RunFMESAPAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.runRemoteFMEAlgorithm import (
    ParameterFMEManagerType,
    RunRemoteFMEAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.selectFeaturesOnCurrentCanvas import (
    SelectFeaturesOnCurrentCanvas,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.stringCsvToFirstLayerWithElementsAlgorithm import (
    StringCsvToFirstLayerWithElementsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.stringCsvToLayerListAlgorithm import (
    StringCsvToLayerListAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.updateRunwayAltitudeAlgorithm import (
    UpdateRunwayAltitudeAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.validateTrackerAlgorithm import (
    ValidateTrackerAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.identifyDifferencesBetweenDatabaseModelsAlgorithm import (
    IdentifyDifferencesBetweenDatabaseModelsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.addUnsharedVertexOnIntersectionsAlgorithm import (
    AddUnsharedVertexOnIntersectionsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.addUnsharedVertexOnSharedEdgesAlgorithm import (
    AddUnsharedVertexOnSharedEdgesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.adjustNetworkConnectivityAlgorithm import (
    AdjustNetworkConnectivityAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.buildPolygonsFromCenterPointsAndBoundariesAlgorithm import (
    BuildPolygonsFromCenterPointsAndBoundariesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.cleanGeometriesAlgorithm import (
    CleanGeometriesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.deaggregateGeometriesAlgorithm import (
    DeaggregatorAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.detectChangesGroupAlgorithm import (
    DetectChangesBetweenGroups,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.detectNullGeometriesAlgorithm import (
    DetectNullGeometriesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.dissolvePolygonsWithSameAttributesAlgorithm import (
    DissolvePolygonsWithSameAttributesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.enforceAttributeRulesAlgorithm import (
    EnforceAttributeRulesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.enforceSpatialRulesAlgorithm import (
    EnforceSpatialRulesAlgorithm,
    ParameterSpatialRulesSetType,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.extendLinesToGeographicBoundsAlgorithm import (
    ExtendLinesToGeographicBoundsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.hierarchicalSnapLayerOnLayerAndUpdateAlgorithm import (
    HierarchicalSnapLayerOnLayerAndUpdateAlgorithm,
    ParameterSnapHierarchyType,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyAndFixInvalidGeometriesAlgorithm import (
    IdentifyAndFixInvalidGeometriesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyAnglesInInvalidRangeAlgorithm import (
    IdentifyAnglesInInvalidRangeAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyAttributeChangesInLines import (
    IdentifyAttributeChangesInLines,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyCountourStreamIntersectionAlgorithm import (
    IdentifyCountourStreamIntersectionAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyCrossingLinesAlgorithm import (
    IdentifyCrossingLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDanglesAlgorithm import (
    IdentifyDanglesAlgorithm,
)

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyCloseFeaturesAlgorithm import (
    IdentifyCloseFeaturesAlgorithm,
    ParameterDistanceBetweenLayersType,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDrainageAndContourInconsistencies import (
    IdentifyDrainageAndContourInconsistencies,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDrainageAngleIssues import (
    IdentifyDrainageAngleIssues,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDrainageFlowIssues import (
    IdentifyDrainageFlowIssues,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDrainageFlowIssuesWithOtherHydrographicClassesAlgorithm import (
    IdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDrainageLoops import (
    IdentifyDrainageLoops,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedFeaturesAlgorithm import (
    IdentifyDuplicatedFeaturesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedGeometriesAlgorithm import (
    IdentifyDuplicatedGeometriesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedLinesBetweenLayersAlgorithm import (
    IdentifyDuplicatedLinesBetweenLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedPointsBetweenLayersAlgorithm import (
    IdentifyDuplicatedPointsBetweenLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedPolygonsBetweenLayersAlgorithm import (
    IdentifyDuplicatedPolygonsBetweenLayersAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyDuplicatedVertexesAlgorithm import (
    IdentifyDuplicatedVertexesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyIntertwinedLinesAlgorithm import (
    IdentifyIntertwinedLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySegmentErrorsBetweenLinesAlgorithm import (
    IdentifySegmentErrorsBetweenLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyGapsAlgorithm import (
    IdentifyGapsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyGapsAndOverlapsInCoverageAlgorithm import (
    IdentifyGapsAndOverlapsInCoverageAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyGeometriesWithLargeVertexDensityAlgorithm import (
    IdentifyGeometriesWithLargeVertexDensityAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyInvalidUUIDsAlgorithm import (
    IdentifyInvalidUUIDsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyMultiPartGeometriesAlgorithm import (
    IdentifyMultiPartGeometriesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyMissingLineIntersectionsOnPoints import (
    IdentifyMissingLineIntersectionsOnPoints,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyMissingLinesOnPolygonLineIntersections import (
    IdentifyMissingLinesOnPolygonLineIntersections,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyMissingPointsOnLineIntersections import (
    IdentifyMissingPointsOnLineIntersections,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyMissingPolygonLinesIntersectionsOnLines import (
    IdentifyMissingPolygonLineIntersectionsOnLines,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyNetworkConstructionIssuesAlgorithm import (
    IdentifyNetworkConstructionIssuesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyOutOfBoundsAnglesAlgorithm import (
    IdentifyOutOfBoundsAnglesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyOutOfBoundsAnglesInCoverageAlgorithm import (
    IdentifyOutOfBoundsAnglesInCoverageAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyOverlapsAlgorithm import (
    IdentifyOverlapsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyPolygonSliverAlgorithm import (
    IdentifyPolygonSliverAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyPolygonUndershoots import (
    IdentifyPolygonUndershootsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySmallFirstOrderDangle import (
    IdentifySmallFirstOrderDanglesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySmallHolesAlgorithm import (
    IdentifySmallHolesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySmallLinesAlgorithm import (
    IdentifySmallLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifySmallPolygonsAlgorithm import (
    IdentifySmallPolygonsAlgorithm,
)

# from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.multipleOutputUnitTestAlgorithm import \
#     MultipleOutputUnitTestAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyTerrainModelErrorsAlgorithm import (
    IdentifyTerrainModelErrorsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyUnmergedLinesWithSameAttributeSetAlgorithm import (
    IdentifyUnmergedLinesWithSameAttributeSetAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyUnsharedVertexOnIntersectionsAlgorithm import (
    IdentifyUnsharedVertexOnIntersectionsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyUnsharedVertexOnSharedEdgesAlgorithm import (
    IdentifyUnsharedVertexOnSharedEdgesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyVertexNearEdgesAlgorithm import (
    IdentifyVertexNearEdgesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyWrongBuildingAnglesAlgorithm import (
    IdentifyWrongBuildingAnglesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyZAnglesBetweenFeaturesAlgorithm import (
    identifyZAnglesBetweenFeaturesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.lineOnLineOverlayerAlgorithm import (
    LineOnLineOverlayerAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.mergeLinesAlgorithm import (
    MergeLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.overlayElementsWithAreasAlgorithm import (
    OverlayElementsWithAreasAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeDuplicatedFeaturesAlgorithm import (
    RemoveDuplicatedFeaturesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeDuplicatedGeometriesAlgorithm import (
    RemoveDuplicatedGeometriesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeEmptyAndUpdateAlgorithm import (
    RemoveEmptyAndUpdateAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeSmallLinesAlgorithm import (
    RemoveSmallLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.removeSmallPolygonsAlgorithm import (
    RemoveSmallPolygonsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.snapLayerOnLayerAndUpdateAlgorithm import (
    SnapLayerOnLayerAndUpdateAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.snapToGridAndUpdateAlgorithm import (
    SnapToGridAndUpdateAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.spellCheckerAlgorithm import (
    SpellCheckerAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.streamOrder import (
    StreamOrder,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalCleanAlgorithm import (
    TopologicalCleanAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalCleanLinesAlgorithm import (
    TopologicalCleanLinesAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalDouglasAreaSimplificationAlgorithm import (
    TopologicalDouglasPeuckerAreaSimplificationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalDouglasLineSimplificationAlgorithm import (
    TopologicalDouglasPeuckerLineSimplificationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.topologicalLineConnectivityAdjustmentAlgorithm import (
    TopologicalLineConnectivityAdjustment,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.unbuildPolygonsAlgorithm import (
    UnbuildPolygonsAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.unicodeFilterAlgorithm import (
    UnicodeFilterAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.verifyAdjacentGeographicBoundaryDataAlgorithm import (
    VerifyAdjacentGeographicBoundaryDataAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.loadThemesAlgorithm import (
    LoadThemesAlgorithm,
)

# from DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.singleOutputUnitTestAlgorithm import SingleOutputUnitTestAlgorithm


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
            AssignDefaultFieldValueToLayersAlgorithm(),
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
            SplitPolygons(),
            SplitPolygonsByGrid(),
            SelectByDE9IMAlgorithm(),
            ExtractByDE9IMAlgorithm(),
            Line2Multiline(),
            IdentifyDrainageAndContourInconsistencies(),
            ExtractElevationPoints(),
            LoadTrackerAlgorithm(),
            IdentifySegmentErrorsBetweenLinesAlgorithm(),
            ValidateTrackerAlgorithm(),
            UpdateRunwayAltitudeAlgorithm(),
            LoadRasterLayerFromServerAlgorithm(),
            IdentifyIntertwinedLinesAlgorithm(),
            IdentifyCrossingLinesAlgorithm(),
            FixDrainageFlowAlgorithm(),
            LoadThemesAlgorithm(),
            IdentifyCloseFeaturesAlgorithm(),
            IdentifySmallObjectsOnLayersAlgorithm(),
            AppendFeaturesToLayerAlgorithm(),
            RightAngleToolParametersAlgorithm(),
            GenericSelectionToolParametersAlgorithm(),
            ClipAndCopyFeaturesBetweenDatabasesAlgorithm(),
            VerifyAdjacentGeographicBoundaryDataAlgorithm(),
            FixSegmentErrorsBetweenLinesAlgorithm(),
            IdentifyDifferencesBetweenDatabaseModelsAlgorithm(),
            AzimuthCalculationAlgorithm(),
            ExportFeaturesByAttributeAlgorithm(),
            DetectChangesBetweenGroups(),
            IdentifyWaterBodyAndContourInconsistencies(),
            CreateGridFromCoordinatesAlgorithm(),
            BuildZipPackageAlgorithm(),
            GeneralizeNetworkEdgesWithLengthAlgorithm(),
            RemoveDuplicateVertexesAlgorithm(),
            IdentifyAttributeChangesInLines(),
            BatchRunAlgorithmWithGeographicBoundsConstraint(),
            IdentifyUncoveredStartAndEndPointsAlgorithm(),
            ReclassifyAdjacentPixelsToNearestNeighborAlgorithm(),
            ReclassifyGroupsOfPixelsToNearestNeighborAlgorithm(),
            ReclassifyGroupsOfPixelsToNearestNeighborWithSlidingWindowAlgorithm(),
            FindSmallClosedLinesAlgorithm(),
            SetLineOrientation(),
            IdentifyMissingLineIntersectionsOnPoints(),
            IdentifyMissingLinesOnPolygonLineIntersections(),
            IdentifyMissingPointsOnLineIntersections(),
            IdentifyMissingPolygonLineIntersectionsOnLines(),
            BatchRasterPackagingForBDGEx(),
            # GeneralizeWaterBodyAlgorithm(),
            # GeneralizeEdificationsAlgorithm(),
            # GeneralizeEdificationsAreaAlgorithm(),
            # GeneralizeLandingStripAlgorithm(),
            # GeneralizeRoundaboutsAlgorithm(),
            # GeneralizeHighwaysAlgorithm(),
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
        self.parameterDistanceBetweenLayersType = ParameterDistanceBetweenLayersType()
        QgsApplication.instance().processingRegistry().addParameterType(
            self.parameterDistanceBetweenLayersType
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
        QgsApplication.instance().processingRegistry().removeParameterType(
            self.parameterDistanceBetweenLayersType
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
        return QIcon(":/plugins/DsgTools/icons/DSGToolsIcon.png")

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
