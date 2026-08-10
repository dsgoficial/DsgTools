from qgis.utils import iface


class AddPointFeature:
    def execute(self):
        iface.activeLayer().startEditing()
        iface.actionAddFeature().trigger()
