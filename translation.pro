 SOURCES         =	BDGExTools/BDGExTools.py \
 					ComplexTools/complexWindow.py \
 					ComplexTools/manageComplex.py \
 					DbTools/PostGISTool/postgisDBTool.py \
 					DbTools/SpatialiteTool/cria_spatialite_dialog.py \
 					Factories/ThreadFactory/dpiThread.py \
 					Factories/ThreadFactory/postgisDbThread.py \
 					ImageTools/processingTools.py \
 					LayerTools/load_by_category.py \
 					LayerTools/load_by_class.py \
 					LayerTools/ui_create_inom_dialog.py \
 					ProcessingTools/processManager.py \
 					QmlTools/qmlParser.py \
 					ServerTools/serverConfigurator.py \
 					ServerTools/viewServers.py \
 					dsg_tools.py \
					InventoryTools/inventoryTools.py \
					Factories/ThreadFactory/inventoryThread.py \
					ToolboxTools/models_and_scripts_installer.py \
					ServerTools/serverDBExplorer.py \
					CustomWidgets/connectionWidget.py \
					UserTools/assign_profiles.py \
					UserTools/create_profile.py \
					UserTools/profile_editor.py \
					UserTools/user_profiles.py \
					UserTools/alter_user_password.py \
					UserTools/create_user.py \
					VectorTools/calc_contour.py \
					VectorTools/contour_tool.py \
					VectorTools/dsg_line_tool.py \
					ConversionTools/convert_database.py \
					AttributeTools/attributes_viewer.py \
					AttributeTools/code_list.py \
					Factories/DbFactory/abstractDb.py \
					Factories/DbFactory/postgisDb.py \
					Factories/DbFactory/spatialiteDb.py

 FORMS           =	ComplexTools/complexWindow_base.ui \
 					ComplexTools/ui_manageComplex.ui \
 					DbTools/PostGISTool/ui_postgisDBTool.ui \
 					DbTools/SpatialiteTool/cria_spatialite_dialog_base.ui \
 					ImageTools/ui_processingTools.ui \
 					LayerTools/load_by_category_dialog.ui \
 					LayerTools/load_by_class_base.ui \
 					LayerTools/ui_create_inom_dialog_base.ui \
 					ServerTools/ui_serverConfigurator.ui \
 					ServerTools/ui_viewServers.ui \
 					ui_about.ui \
					InventoryTools/ui_inventoryTools.ui \
					ToolboxTools/models_and_scripts_installer.ui \
					ServerTools/ui_serverDBExplorer.ui \
					CustomWidgets/connectionWidget.ui \
					UserTools/assign_profiles.ui \
					UserTools/create_profile.ui \
					UserTools/profile_editor.ui \
					UserTools/user_profiles.ui \
					UserTools/alter_user_password.ui \
					UserTools/create_user.ui \
					VectorTools/calc_contour.ui \
					ConversionTools/convert_database.ui \
					AttributeTools/attributes_viewer.ui \
					AttributeTools/code_list.ui

 TRANSLATIONS    = i18n/DsgTools_pt.ts

RESOURCES += \
    resources.qrc
