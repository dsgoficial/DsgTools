 SOURCES         = dsg_tools.py \
                    ComplexTools/manageComplex.py \
                    ComplexTools/complexWindow.py \
                    DbTools/PostGISTool/postgisDBTool.py \
                    DbTools/PostGISTool/createPostGISDatabase.py \
                    LayerTools/ui_create_inom_dialog.py \
                    LayerTools/load_by_class.py \
                    LayerTools/load_by_category.py \
                    QmlTools/qmlParser.py \
                    ServerTools/serverConfigurator.py

 FORMS           = ComplexTools/complexWindow_base.ui \
                   ComplexTools/ui_manageComplex.ui \
                   DbTools/PostGISTool/ui_postgisDBTool.ui \
                   DbTools/cria_spatialite_dialog_base.ui \
                   LayerTools/load_by_category_dialog.ui \
                   LayerTools/load_by_class_base.ui \
                   LayerTools/ui_create_inom_dialog_base.ui \
                   ui_about.ui \
                   ServerTools/ui_serverConfigurator.ui

 TRANSLATIONS    = i18n/DsgTools_pt.ts

RESOURCES += \
    resources.qrc
