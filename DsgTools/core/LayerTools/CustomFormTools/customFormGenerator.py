# -*- coding: utf-8 -*-
"""
/***************************************************************************

                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2018-02-28
        git sha              : $Format:%H$
        copyright            : (C) 2018 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br

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
import os
from qgis import core


class CustomFormGenerator(object):
    def __init__(self):
        super(CustomFormGenerator, self).__init__()
        self.lenColumnDict = {1: "length_otf", 2: "area_otf"}

    def get_form_template(self):
        return """<?xml version="1.0" encoding="UTF-8"?>
            <ui version="4.0">
            <class>Dialog</class>
            <widget class="QDialog" name="Dialog">
            <property name="windowTitle">
            <string>Dialog</string>
            </property>
            <layout class="QGridLayout" name="gridLayout">
            <item row="0" column="0">
                <widget class="QLabel" name="label">
                <property name="text">
                <string>Relatório de erros :</string>
                </property>
                </widget>
            </item>
            <item row="0" column="1">
                <widget class="QPushButton" name="logBtn">
                <property name="text">
                <string>&gt;&gt;&gt;</string>
                </property>
                <property name="autoDefault">
                <bool>false</bool>
                </property>
                </widget>
            </item>
            <item row="0" column="2" rowspan="15" colspan="4">
                <widget class="QFrame" name="logFrame">
                <property name="frameShape">
                <enum>QFrame::StyledPanel</enum>
                </property>
                <property name="frameShadow">
                <enum>QFrame::Raised</enum>
                </property>
                <layout class="QVBoxLayout" name="verticalLayout">
                <item>
                <widget class="QLabel" name="logLabel">
                </widget>
                </item>
                </layout>
                </widget>
            </item>
            {items}
            <item row="{row_btn}" column="0" colspan="2">
                <widget class="QDialogButtonBox" name="buttonBox">
                <property name="orientation">
                <enum>Qt::Horizontal</enum>
                </property>
                <property name="standardButtons">
                <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
                </property>
                </widget>
            </item>
            </layout>
            <zorder>buttonBox</zorder>
            <zorder>logFrame</zorder>
            <zorder>logBtn</zorder>
            <zorder>layoutWidget</zorder>
            </widget>
            <resources/>
            <connections>
            <connection>
            <sender>buttonBox</sender>
            <signal>accepted()</signal>
            <receiver>Dialog</receiver>
            <slot>accept()</slot>
            <hints>
                <hint type="sourcelabel">
                <x>248</x>
                <y>254</y>
                </hint>
                <hint type="destinationlabel">
                <x>157</x>
                <y>274</y>
                </hint>
            </hints>
            </connection>
            <connection>
            <sender>buttonBox</sender>
            <signal>rejected()</signal>
            <receiver>Dialog</receiver>
            <slot>reject()</slot>
            <hints>
                <hint type="sourcelabel">
                <x>316</x>
                <y>260</y>
                </hint>
                <hint type="destinationlabel">
                <x>286</x>
                <y>274</y>
                </hint>
            </hints>
            </connection>
            </connections>
            </ui>
            """

    def get_le_template(self, field, alias, row, readOnly=""):
        return """<item row="{row}" column="0">
                <widget class="QLabel" name="label_{field}">
                <property name="text">
                <string>{alias}</string>
                </property>
                </widget>
            </item>
            <item row="{row}" column="1">
                <widget class="QLineEdit" name="{field}">
                {readOnly}
                </widget>
            </item>
            """.format(
            alias=alias, field=field, row=row, readOnly=readOnly
        )

    def get_cb_template(self, field, alias, row):
        return """<item row="{row}" column="0">
                <widget class="QLabel" name="label_{field}">
                <property name="text">
                <string>{alias}</string>
                </property>
                </widget>
            </item>
            <item row="{row}" column="1">
                <widget class="QComboBox" name="{field}"/>
            </item>""".format(
            alias=alias, field=field, row=row
        )

    def create_cb(self, field, alias, row):
        return self.get_cb_template(field, alias, row)

    def create_le(self, field, alias, row, setReadOnly=False):
        """if setReadOnly:
            readOnly =u'''<property name="readOnly">
                            <bool>true</bool>
                        </property>'''
            return self.get_le_template(field, row, readOnly)
        else:"""
        return self.get_le_template(field, alias, row)

    def create(self, vlayer, layerData):
        form_path = os.path.join(os.path.dirname(__file__), "forms", vlayer.name())
        with open(form_path, "w") as formFile:
            form = self.get_form_template()
            layerData = layerData["layer_fields"]
            all_items = ""
            rowAttr = 1
            for field in vlayer.fields():
                field_name = field.name()
                field_alias = field.alias()
                if field in ["id", "controle_id", "ultimo_usuario", "data_modificacao"]:
                    all_items += self.create_le(
                        field_name, field_alias, rowAttr, setReadOnly=True
                    )
                elif field_name == "tipo":
                    if "filter" in layerData:
                        all_items += self.create_cb("filter", "filter", rowAttr)
                    all_items += self.create_cb(field_name, field_alias, rowAttr)
                    rowAttr += 1
                elif (field_name in layerData) and layerData[field]:
                    all_items += self.create_cb(field_name, field_alias, rowAttr)
                elif field_name in layerData:
                    all_items += self.create_le(field_name, field_alias, rowAttr)
                rowAttr += 1
            if vlayer.geometryType() in self.lenColumnDict:
                all_items += self.create_le(
                    self.lenColumnDict[vlayer.geometryType()],
                    self.lenColumnDict[vlayer.geometryType()],
                    rowAttr + 1,
                )
            form = form.format(items=unicode(all_items), row_btn=rowAttr + 1)
            formFile.write(form)
        return form_path
