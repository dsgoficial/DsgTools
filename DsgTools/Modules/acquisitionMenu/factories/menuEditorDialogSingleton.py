from DsgTools.Modules.acquisitionMenu.widgets.menuEditorDialog import MenuEditorDialog


class MenuEditorDialogSingleton:

    instance = None

    @staticmethod
    def getInstance(controller):
        if not MenuEditorDialogSingleton.instance:
            MenuEditorDialogSingleton.instance = MenuEditorDialog(controller)
        return MenuEditorDialogSingleton.instance
