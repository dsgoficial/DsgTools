from qgis.utils import iface


class OpenAttributeTable:
    def execute(self):
        iface.actionOpenTable().trigger()
