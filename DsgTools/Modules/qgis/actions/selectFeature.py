from qgis.utils import iface


class SelectFeature:
    def execute(self):
        iface.actionSelectRectangle().trigger()
