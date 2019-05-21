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
from builtins import str
from builtins import object
from qgis import core

class GeneratorCustomForm(object):
    def __init__(self):
        # contrutor
        super(GeneratorCustomForm, self).__init__()

    def getDialogTemplate(self):
        return u'''<?xml version="1.0" encoding="UTF-8"?>
        <ui version="4.0">
        <class>Dialog</class>
        <widget class="QDialog" name="Dialog">
        <property name="geometry">
        <rect>
            <x>0</x>
            <y>0</y>
            <width>680</width>
            <height>600</height>
        </rect>
        </property>
        <property name="minimumSize">
        <size>
            <width>680</width>
            <height>600</height>
        </size>
        </property>
        <property name="maximumSize">
        <size>
            <width>700000</width>
            <height>6000000</height>
        </size>
        </property>
        <property name="windowTitle">
        <string>Dialog</string>
        </property>
        <layout class="QGridLayout" name="gridLayout">
        <item row="1" column="0">
            <widget class="QDialogButtonBox" name="buttonBox">
            <property name="orientation">
            <enum>Qt::Horizontal</enum>
            </property>
            <property name="standardButtons">
            <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
            </property>
            </widget>
        </item>
        <item row="0" column="0">
            <widget class="QTabWidget" name="tabWidget">
            <property name="sizePolicy">
            <sizepolicy hsizetype="MinimumExpanding" vsizetype="MinimumExpanding">
            <horstretch>0</horstretch>
            <verstretch>0</verstretch>
            </sizepolicy>
            </property>
            <property name="currentIndex">
            <number>0</number>
            </property>
            <widget class="QWidget" name="tab">
            <attribute name="title">
            <string>Atributos</string>
            </attribute>
            <layout class="QGridLayout" name="gridLayout_3">
            <item row="0" column="0">
                <widget class="QSplitter" name="splitter">
                <property name="orientation">
                <enum>Qt::Horizontal</enum>
                </property>
                <widget class="QWidget" name="">
                <layout class="QVBoxLayout" name="verticalLayout">
                <item>
                    <widget class="QPushButton" name="logBtn">
                    <property name="sizePolicy">
                    <sizepolicy hsizetype="Minimum" vsizetype="MinimumExpanding">
                    <horstretch>0</horstretch>
                    <verstretch>0</verstretch>
                    </sizepolicy>
                    </property>
                    <property name="minimumSize">
                    <size>
                    <width>0</width>
                    <height>30</height>
                    </size>
                    </property>
                    <property name="maximumSize">
                    <size>
                    <width>16777215</width>
                    <height>30</height>
                    </size>
                    </property>
                    <property name="text">
                    <string>Observações</string>
                    </property>
                    </widget>
                </item>
                <item>
                    <layout class="QGridLayout" name="gridLayout_2">
                    {0}                    
                    </layout>
                </item>
                </layout>
                </widget>
                <widget class="QWidget" name="verticalLayoutWidget_2">
                <layout class="QVBoxLayout" name="verticalLayout_2">
                <item>
                    <widget class="QFrame" name="logFrame">
                    <property name="frameShape">
                    <enum>QFrame::StyledPanel</enum>
                    </property>
                    <property name="frameShadow">
                    <enum>QFrame::Raised</enum>
                    </property>
                    <layout class="QVBoxLayout" name="verticalLayout_4">
                    <item>
                    <widget class="QTextBrowser" name="Browser">
                        <property name="sizePolicy">
                        <sizepolicy hsizetype="MinimumExpanding" vsizetype="MinimumExpanding">
                        <horstretch>0</horstretch>
                        <verstretch>0</verstretch>
                        </sizepolicy>
                        </property>
                        <property name="minimumSize">
                        <size>
                        <width>0</width>
                        <height>0</height>
                        </size>
                        </property>
                        <property name="maximumSize">
                        <size>
                        <width>16777215</width>
                        <height>16777215</height>
                        </size>
                        </property>
                    </widget>
                    </item>
                    </layout>
                    </widget>
                </item>
                </layout>
                </widget>
                </widget>
            </item>
            </layout>
            </widget>
            <widget class="QWidget" name="tab_2">
            <attribute name="title">
            <string>Controle</string>
            </attribute>
            <layout class="QGridLayout" name="gridLayout_5">
            <item row="0" column="0">
                <layout class="QGridLayout" name="gridLayout_4">
                {1}
                </layout>
            </item>
            <item row="1" column="0">
                <spacer name="verticalSpacer">
                <property name="orientation">
                <enum>Qt::Vertical</enum>
                </property>
                <property name="sizeHint" stdset="0">
                <size>
                <width>20</width>
                <height>337</height>
                </size>
                </property>
                </spacer>
            </item>
            </layout>
            </widget>
            </widget>
        </item>
        </layout>
        </widget>
        <tabstops>
        <tabstop>tabWidget</tabstop>
        <tabstop>buttonBox</tabstop>
        </tabstops>
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
        '''
        
    def getComboBoxTemplate(self): 
        return u'''<item row="{row}" column="0">
        <widget class="QLabel" name="label_{field}">
        <property name="sizePolicy">
        <sizepolicy hsizetype="Preferred" vsizetype="MinimumExpanding">
            <horstretch>0</horstretch>
            <verstretch>0</verstretch>
        </sizepolicy>
        </property>
        <property name="minimumSize">
        <size>
            <width>0</width>
            <height>30</height>
        </size>
        </property>
        <property name="maximumSize">
        <size>
            <width>16777215</width>
            <height>30</height>
        </size>
        </property>
        <property name="text">
        <string>{field}</string>
        </property>
        </widget>
        </item>
        <item row="{row}" column="1">
        <widget class="QComboBox" name="{field}">
        <property name="sizePolicy">
        <sizepolicy hsizetype="MinimumExpanding" vsizetype="MinimumExpanding">
            <horstretch>0</horstretch>
            <verstretch>0</verstretch>
        </sizepolicy>
        </property>
        <property name="minimumSize">
        <size>
            <width>175</width>
            <height>30</height>
        </size>
        </property>
        <property name="maximumSize">
        <size>
            <width>16777215</width>
            <height>30</height>
        </size>
        </property>
        </widget>
        </item>'''

    def getLineEditTemplate(self):
        return '''<item row="{row}" column="0">
        <widget class="QLabel" name="label_{field}">
        <property name="sizePolicy">
        <sizepolicy hsizetype="Preferred" vsizetype="MinimumExpanding">
            <horstretch>0</horstretch>
            <verstretch>0</verstretch>
        </sizepolicy>
        </property>
        <property name="minimumSize">
        <size>
            <width>0</width>
            <height>30</height>
        </size>
        </property>
        <property name="maximumSize">
        <size>
            <width>16777215</width>
            <height>30</height>
        </size>
        </property>
        <property name="text">
        <string>{field}</string>
        </property>
        </widget>
        </item>
        <item row="{row}" column="1">
        <widget class="QLineEdit" name="{field}">
        <property name="sizePolicy">
        <sizepolicy hsizetype="MinimumExpanding" vsizetype="MinimumExpanding">
            <horstretch>0</horstretch>
            <verstretch>0</verstretch>
        </sizepolicy>
        </property>
        <property name="minimumSize">
        <size>
            <width>175</width>
            <height>30</height>
        </size>
        </property>
        <property name="maximumSize">
        <size>
            <width>16777215</width>
            <height>30</height>
        </size>
        </property>
        {readOnly}
        </widget>
        </item>'''

    def createComboBox(self, field, row):
        comboBox = self.getComboBoxTemplate()
        comboBox = comboBox.replace(u'{field}', field)
        comboBox = comboBox.replace(u'{row}', str(row))
        return comboBox

    def createLineEdit(self, field, row, readOnly = False):
        lineEdit = self.getLineEditTemplate()
        lineEdit = lineEdit.replace(u'{field}', field)
        lineEdit = lineEdit.replace(u'{row}', str(row))
        if readOnly:
            lineEdit = lineEdit.replace(
                u'{readOnly}',
                u'''<property name="readOnly">
                    <bool>true</bool>
                   </property>'''
            )
        else:
            lineEdit = lineEdit.replace(u'{readOnly}', u'')

        return lineEdit 

    def create(self, formFile, vlayer, withFilter = False):
        dialog = self.getDialogTemplate()
        allWidgetsTabAttr = u""
        allWidgetsTabControl = u""
        rowAttr = 0
        rowControl = 0
        for idx in vlayer.fields().allAttributesList():
            field = vlayer.fields().field(idx).name()
            if field in [u'id', u'controle_id', u'ultimo_usuario', u'data_modificacao']:
                allWidgetsTabControl += self.createLineEdit(field, rowControl, readOnly = True)
                rowControl+=1
            elif field == u'tipo':
                if withFilter:
                    allWidgetsTabAttr += self.createComboBox(u'filter', rowAttr)
                    rowAttr+=1
                allWidgetsTabAttr += self.createComboBox(field, rowAttr)
            elif vlayer.editorWidgetSetup(idx).type() == 'ValueMap':
                allWidgetsTabAttr += self.createComboBox(field, rowAttr)
            elif vlayer.editorWidgetSetup(idx).type() in ['LineEdit', 'UniqueValues']:
                allWidgetsTabAttr += self.createLineEdit(field, rowAttr)
            rowAttr+=1
        if vlayer.geometryType() == 1:
            allWidgetsTabAttr += self.createLineEdit(u'length_otf', rowAttr)            
        elif vlayer.geometryType() == 2:
            allWidgetsTabAttr += self.createLineEdit(u'area_otf', rowAttr)   
        dialog = dialog.replace(u'{1}', str(allWidgetsTabControl))
        dialog = dialog.replace(u'{0}', str(allWidgetsTabAttr))
        formFile.write(dialog.encode("utf-8"))
        formFile.close()