from qgis import gui, core
from qgis.utils import iface
from DsgTools.Modules.qgis.actions.selectRaster import SelectRaster
from DsgTools.Modules.qgis.actions.addPointFeature import AddPointFeature
from DsgTools.Modules.qgis.actions.selectFeature import SelectFeature
from DsgTools.Modules.qgis.actions.setFeatureInspector import SetFeatureInspector
from DsgTools.Modules.qgis.actions.topologicalSnapping import TopologicalSnapping
from DsgTools.Modules.qgis.actions.openAttributeTable import OpenAttributeTable
from DsgTools.Modules.qgis.actions.restoreFields import RestoreFields
from DsgTools.Modules.qgis.actions.setDefaultFields import SetDefaultFields
from DsgTools.Modules.qgis.actions.openAttributeTableOnlySelection import (
    OpenAttributeTableOnlySelection,
)
from DsgTools.Modules.qgis.actions.moveFeature import MoveFeature
from DsgTools.Modules.qgis.actions.mergeFeatureAttributes import MergeFeatureAttributes
from DsgTools.Modules.qgis.actions.deleteSelected import DeleteSelected
from DsgTools.Modules.qgis.actions.freeHand import FreeHand
from DsgTools.Modules.qgis.actions.cutFeatures import CutFeatures
from DsgTools.Modules.qgis.actions.trimExtendFeature import TrimExtendFeature
from DsgTools.Modules.qgis.actions.addRing import AddRing
from DsgTools.Modules.qgis.actions.deleteRing import DeleteRing
from DsgTools.Modules.qgis.actions.rightDegreeAngleDigitizing import (
    RightDegreeAngleDigitizing,
)
from DsgTools.Modules.qgis.actions.freeHandReshape import FreeHandReshape


class ActionsFactory:
    def __init__(self):
        pass

    def getAction(self, actionName):
        actions = {
            "SelectRaster": SelectRaster,
            "AddPointFeature": AddPointFeature,
            "SelectFeature": SelectFeature,
            "SetFeatureInspector": SetFeatureInspector,
            "TopologicalSnapping": TopologicalSnapping,
            "OpenAttributeTable": OpenAttributeTable,
            "RestoreFields": RestoreFields,
            "SetDefaultFields": SetDefaultFields,
            "OpenAttributeTableOnlySelection": OpenAttributeTableOnlySelection,
            "MoveFeature": MoveFeature,
            "MergeFeatureAttributes": MergeFeatureAttributes,
            "DeleteSelected": DeleteSelected,
            "FreeHand": FreeHand,
            "CutFeatures": CutFeatures,
            "TrimExtendFeature": TrimExtendFeature,
            "AddRing": AddRing,
            "DeleteRing": DeleteRing,
            "RightDegreeAngleDigitizing": RightDegreeAngleDigitizing,
            "FreeHandReshape": FreeHandReshape,
        }
        return actions[actionName]() if actionName in actions else None
