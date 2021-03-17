<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="1e+8" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="250,255,57,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames">
      <value>area_trabalho_nome</value>
      <value>area_trabalho_poligono</value>
      <value>uiData</value>
    </property>
    <property key="variableValues">
      <value>2720-2_4_1</value>
      <value>SRID=31981;POLYGON((637066.631989665 7501991.38616081,632782.778547045 7502029.07822822,632798.219925038 7503812.97150697,632822.687862399 7506642.14901802,637107.829653555 7506604.511548,637098.198115181 7505525.29254473,637066.631989665 7501991.38616081))</value>
      <value>{"uiData": {"layer_data": {"layer_schema": "edgv", "layer_name": "llp_delimitacao_fisica_l", "layer_geom_type": "MULTILINESTRING", "layer_fields": {"data_modificacao": {}, "tipo_comprovacao": {"valueMap": {"Confirmado em campo": 1, "Não possível de confirmar em campo": 2, "Feição não necessita de confirmação": 3, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "tipo": {"valueMap": {"Cerca": 1, "Muro": 2, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "observacao": {}, "tipo_insumo": {"valueMap": {"Fotointerpretado": 1, "Insumo externo": 2, "Processo automático": 3, "Aquisição em campo": 4, "Mapeamento anterior": 5, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "ultimo_usuario": {}, "material_construcao": {"valueMap": {"Desconhecido": 0, "Alvenaria": 1, "Rocha": 4, "Madeira": 5, "Arame": 6, "Tela ou alambrado": 7, "Cerca viva": 8, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "controle_id": {}}, "group_geom": "LINHA", "group_class": "llp"}, "fields_sorted": ["data_modificacao", "tipo_comprovacao", "tipo", "observacao", "tipo_insumo", "ultimo_usuario", "material_construcao", "controle_id"], "form_name": "C:/Users/Proc/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python/plugins\\Ferramentas_Producao\\Tools\\LoadData\\forms\\sisfron_sirgas2000_utm_21S_llp_delimitacao_fisica_l.ui"}}</value>
    </property>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory opacity="1" maxScaleDenominator="1e+8" barWidth="5" sizeType="MM" minimumSize="0" penAlpha="255" width="15" backgroundColor="#ffffff" enabled="0" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" lineSizeType="MM" labelPlacementMethod="XHeight" penWidth="0" scaleBasedVisibility="0" scaleDependency="Area" rotationOffset="270" diagramOrientation="Up" height="15" minScaleDenominator="0" lineSizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" zIndex="0" priority="0" obstacle="0" placement="2" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Cerca" type="QString" value="1"/>
              <Option name="Muro" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="material_construcao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Alvenaria" type="QString" value="1"/>
              <Option name="Arame" type="QString" value="6"/>
              <Option name="Cerca viva" type="QString" value="8"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Madeira" type="QString" value="5"/>
              <Option name="Rocha" type="QString" value="4"/>
              <Option name="Tela ou alambrado" type="QString" value="7"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_comprovacao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Confirmado em campo" type="QString" value="1"/>
              <Option name="Feição não necessita de confirmação" type="QString" value="3"/>
              <Option name="Não possível de confirmar em campo" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_insumo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Aquisição em campo" type="QString" value="4"/>
              <Option name="Fotointerpretado" type="QString" value="1"/>
              <Option name="Insumo externo" type="QString" value="2"/>
              <Option name="Mapeamento anterior" type="QString" value="5"/>
              <Option name="Processo automático" type="QString" value="3"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="observacao">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="data_modificacao">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="controle_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ultimo_usuario">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="length_otf">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lenght_otf">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="id" index="0" field="id"/>
    <alias name="tipo" index="1" field="tipo"/>
    <alias name="material_construcao" index="2" field="material_construcao"/>
    <alias name="tipo_comprovacao" index="3" field="tipo_comprovacao"/>
    <alias name="tipo_insumo" index="4" field="tipo_insumo"/>
    <alias name="observacao" index="5" field="observacao"/>
    <alias name="data_modificacao" index="6" field="data_modificacao"/>
    <alias name="controle_id" index="7" field="controle_id"/>
    <alias name="ultimo_usuario" index="8" field="ultimo_usuario"/>
    <alias name="length_otf" index="9" field="length_otf"/>
    <alias name="" index="10" field="lenght_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="tipo" expression=""/>
    <default applyOnUpdate="0" field="material_construcao" expression=""/>
    <default applyOnUpdate="0" field="tipo_comprovacao" expression=""/>
    <default applyOnUpdate="0" field="tipo_insumo" expression=""/>
    <default applyOnUpdate="0" field="observacao" expression=""/>
    <default applyOnUpdate="0" field="data_modificacao" expression=""/>
    <default applyOnUpdate="0" field="controle_id" expression=""/>
    <default applyOnUpdate="0" field="ultimo_usuario" expression="'3'"/>
    <default applyOnUpdate="0" field="length_otf" expression=""/>
    <default applyOnUpdate="0" field="lenght_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="material_construcao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_comprovacao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_insumo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="observacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="data_modificacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="controle_id" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="ultimo_usuario" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="length_otf" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="lenght_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="tipo" desc=""/>
    <constraint exp="" field="material_construcao" desc=""/>
    <constraint exp="" field="tipo_comprovacao" desc=""/>
    <constraint exp="" field="tipo_insumo" desc=""/>
    <constraint exp="" field="observacao" desc=""/>
    <constraint exp="" field="data_modificacao" desc=""/>
    <constraint exp="" field="controle_id" desc=""/>
    <constraint exp="" field="ultimo_usuario" desc=""/>
    <constraint exp="" field="length_otf" desc=""/>
    <constraint exp="" field="lenght_otf" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
    <field comment="" precision="0" name="lenght_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
  </expressionfields>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="id" type="field" hidden="0" width="-1"/>
      <column name="tipo" type="field" hidden="0" width="-1"/>
      <column name="material_construcao" type="field" hidden="0" width="-1"/>
      <column name="tipo_comprovacao" type="field" hidden="0" width="-1"/>
      <column name="tipo_insumo" type="field" hidden="0" width="-1"/>
      <column name="observacao" type="field" hidden="0" width="-1"/>
      <column name="data_modificacao" type="field" hidden="0" width="-1"/>
      <column name="controle_id" type="field" hidden="0" width="-1"/>
      <column name="ultimo_usuario" type="field" hidden="0" width="-1"/>
      <column name="length_otf" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1">C:/Users/Proc/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\Ferramentas_Producao\Tools\LoadData\forms\sisfron_sirgas2000_utm_21S_llp_delimitacao_fisica_l.ui</editform>
  <editforminit>formOpen</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis import core, gui
import re
global a

class ValidateForm:
	def __init__(self, layer, formValues, logBrowser):
		self.layer = layer 
		self.formValues = formValues
		self.rules = []
		self.logBrowser = logBrowser
		self.validateForm()
		
	def calculateExpression(self, exp):
		for field in self.formValues:
			if field != 'filter':
				if len(self.formValues[field]) == 3:
					value = self.formValues[field][1][self.formValues[field][0]]
				else:
					value = self.formValues[field][0]
				exp = exp.replace('"{0}"'.format(field), "'{0}'".format(str(value)))
				exp = exp.replace("'NULL'".format(field), "NULL")
		r = QgsExpression(exp)
		return r.evaluate()
		
	def validateForm(self):
		self.cleanRulesOnForm()
		logText = ""
		for rule in self.rules:
			for field in rule:
				if field in self.formValues:
					for exp in reversed(rule[field]):
						try:
							result = self.calculateExpression(exp['rule'])
							if bool(result):
								if len(self.formValues[field]) == 3:
									self.formValues[field][2].setStyleSheet(
										"QWidget {background-color: rgb(%s)}"%(
											exp["cor_rgb"]
										)
									)
								else:
									self.formValues[field][1].setStyleSheet(
										"QWidget {background-color: rgb(%s)}"%(
											exp["cor_rgb"]
										)
									)
								logText += u"<p>{0}</p>".format(exp["descricao"])
						except:
							pass
		self.logBrowser.setText(logText)

	def cleanRulesOnForm(self):
		for field in self.formValues:
			if len(self.formValues[field]) == 3:
				self.formValues[field][2].setStyleSheet("")			
			else:
				self.formValues[field][1].setStyleSheet("")

class ManagerForm(QtCore.QObject):
    def __init__(self, dialog, layer, feature):
        super(ManagerForm, self).__init__()
        self.myDialog = dialog
        self.lyr = layer
        self.validadeForm = ""
        self.logBrowser = dialog.findChild(QLabel, "logLabel")
        self.logFrame = dialog.findChild(QFrame, "logFrame")
        self.logFrame.hide()
        self.logBtn = dialog.findChild(QPushButton, "logBtn")
        self.logBtn.setCheckable(True)
        self.logBtn.clicked.connect(self.showLog)
        buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")
        buttonBox.rejected.connect(self.finishedForm)
        buttonBox.accepted.connect(self.finishedForm)
        button_ok = buttonBox.button(QDialogButtonBox.Ok)
        button_ok.setAutoDefault(True)
        button_ok.setDefault(True)
        button_cancel = buttonBox.button(QDialogButtonBox.Cancel)
        button_cancel.setAutoDefault(False)
        button_cancel.setDefault(False)
        self.myDialog.installEventFilter(self)

    def showLog(self, state):
        if state:
            self.logFrame.show()
        else:
            self.logFrame.hide()
		
    def eventFilter(self, o, event):
        if event.type() in [7, 10, 11, 100]:
            self.validateLayerByRules()
        return False
		
    def validateLayerByRules(self):
        formValues = {}
        for cb in self.myDialog.findChildren(QComboBox):
            idx = self.lyr.fields().indexOf(cb.objectName())
            formValues[cb.objectName()] = [
                cb.currentText(),
                self.lyr.editorWidgetSetup(idx).config()['map'] if idx > 0 else self.optFilter.keys(),
                cb
            ]
        for le in self.myDialog.findChildren(QLineEdit):
                formValues[le.objectName()] = [
                le.text(),
                le
            ]
        self.validadeForm = ValidateForm(self.lyr, formValues, self.logBrowser)
		
    def finishedForm(self):
        pass

def formOpen(dialog, layer, featureid):
    try:
        global a
        a = ManagerForm(dialog, layer, featureid)
    except:
        pass]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <editable>
    <field name="controle_id" editable="1"/>
    <field name="data_modificacao" editable="1"/>
    <field name="id" editable="1"/>
    <field name="length_otf" editable="0"/>
    <field name="material_construcao" editable="1"/>
    <field name="observacao" editable="1"/>
    <field name="tipo" editable="1"/>
    <field name="tipo_comprovacao" editable="1"/>
    <field name="tipo_insumo" editable="1"/>
    <field name="ultimo_usuario" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="controle_id"/>
    <field labelOnTop="0" name="data_modificacao"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="length_otf"/>
    <field labelOnTop="0" name="material_construcao"/>
    <field labelOnTop="0" name="observacao"/>
    <field labelOnTop="0" name="tipo"/>
    <field labelOnTop="0" name="tipo_comprovacao"/>
    <field labelOnTop="0" name="tipo_insumo"/>
    <field labelOnTop="0" name="ultimo_usuario"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
