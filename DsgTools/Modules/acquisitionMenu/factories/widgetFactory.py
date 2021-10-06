from DsgTools.Modules.acquisitionMenu.widgets.menuWidget import MenuWidget
from DsgTools.Modules.acquisitionMenu.widgets.tabEditorWidget import TabEditorWidget
from DsgTools.Modules.acquisitionMenu.widgets.buttonEditorWidget import ButtonEditorWidget
from DsgTools.Modules.acquisitionMenu.factories.menuEditorDialogSingleton import MenuEditorDialogSingleton
from DsgTools.Modules.acquisitionMenu.widgets.addTabDialog import AddTabDialog
from DsgTools.Modules.acquisitionMenu.widgets.addButtonDialog import AddButtonDialog
from DsgTools.Modules.acquisitionMenu.widgets.customComboBox import CustomComboBox
from DsgTools.Modules.acquisitionMenu.widgets.attributeTableWidget import AttributeTableWidget
from DsgTools.Modules.acquisitionMenu.widgets.menuDock import MenuDock
from DsgTools.Modules.acquisitionMenu.widgets.reclassifyDialog import ReclassifyDialog

class WidgetFactory:

    def createWidget(self, widgetName, controller):
        widgetNames = {
            'MenuEditorDialog': lambda controller: MenuEditorDialogSingleton.getInstance( controller ),
            'MenuWidget': lambda controller: MenuWidget(controller=controller),
            'TabEditorWidget': lambda controller: TabEditorWidget(controller=controller),
            'ButtonEditorWidget': lambda controller: ButtonEditorWidget(controller=controller),
            'AddTabDialog': lambda controller: AddTabDialog(controller=controller),
            'AddButtonDialog': lambda controller: AddButtonDialog(controller=controller),
            'FilterComboBox': lambda controller: CustomComboBox(),
            'AttributeTableWidget': lambda controller: AttributeTableWidget(controller=controller),
            'MenuDock': lambda controller: MenuDock(controller=controller),
            'ReclassifyDialog': lambda controller: ReclassifyDialog(controller=controller)
        }
        return widgetNames[ widgetName ]( controller )