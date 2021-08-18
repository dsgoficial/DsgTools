<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" simplifyDrawingHints="0" readOnly="0" simplifyDrawingTol="1" version="3.7.0-Master" labelsEnabled="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" minScale="1e+8" simplifyLocal="1" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" type="line" name="0" clip_to_extent="1" force_rhr="0">
        <layer pass="0" locked="0" enabled="1" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="213,180,60,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties/>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks type="StringList">
      <Option value="" type="QString"/>
    </activeChecks>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nome">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nomeabrev">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="geometriaaproximada">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="coincidecomdentrode">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="19" type="QString" name="Barragem"/>
              <Option value="2" type="QString" name="Canal"/>
              <Option value="13" type="QString" name="Corredeira"/>
              <Option value="14" type="QString" name="Eclusa"/>
              <Option value="16" type="QString" name="Foz marítima"/>
              <Option value="9" type="QString" name="Laguna"/>
              <Option value="97" type="QString" name="Não aplicável"/>
              <Option value="12" type="QString" name="Queda d´água"/>
              <Option value="10" type="QString" name="Represa/açude"/>
              <Option value="1" type="QString" name="Rio"/>
              <Option value="15" type="QString" name="Terreno sujeito a inundação"/>
              <Option value="11" type="QString" name="Vala"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dentrodepoligono">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="compartilhado">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="eixoprincipal">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="navegabilidade">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecida"/>
              <Option value="1" type="QString" name="Navegável"/>
              <Option value="2" type="QString" name="Não navegável"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="caladomax">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="regime">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="1" type="QString" name="Permanente"/>
              <Option value="2" type="QString" name="Permanente com grande variação"/>
              <Option value="5" type="QString" name="Seco"/>
              <Option value="3" type="QString" name="Temporário"/>
              <Option value="4" type="QString" name="Temporário com leito permanente"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="larguramedia">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="velocidademedcorrente">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="profundidademedia">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_trecho_curso_dagua">
      <editWidget type="">
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
    <alias field="id" index="0" name=""/>
    <alias field="nome" index="1" name=""/>
    <alias field="nomeabrev" index="2" name=""/>
    <alias field="geometriaaproximada" index="3" name=""/>
    <alias field="coincidecomdentrode" index="4" name=""/>
    <alias field="dentrodepoligono" index="5" name=""/>
    <alias field="compartilhado" index="6" name=""/>
    <alias field="eixoprincipal" index="7" name=""/>
    <alias field="navegabilidade" index="8" name=""/>
    <alias field="caladomax" index="9" name=""/>
    <alias field="regime" index="10" name=""/>
    <alias field="larguramedia" index="11" name=""/>
    <alias field="velocidademedcorrente" index="12" name=""/>
    <alias field="profundidademedia" index="13" name=""/>
    <alias field="id_trecho_curso_dagua" index="14" name=""/>
    <alias field="lenght_otf" index="15" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="coincidecomdentrode" expression=""/>
    <default applyOnUpdate="0" field="dentrodepoligono" expression=""/>
    <default applyOnUpdate="0" field="compartilhado" expression=""/>
    <default applyOnUpdate="0" field="eixoprincipal" expression=""/>
    <default applyOnUpdate="0" field="navegabilidade" expression=""/>
    <default applyOnUpdate="0" field="caladomax" expression=""/>
    <default applyOnUpdate="0" field="regime" expression=""/>
    <default applyOnUpdate="0" field="larguramedia" expression=""/>
    <default applyOnUpdate="0" field="velocidademedcorrente" expression=""/>
    <default applyOnUpdate="0" field="profundidademedia" expression=""/>
    <default applyOnUpdate="0" field="id_trecho_curso_dagua" expression=""/>
    <default applyOnUpdate="0" field="lenght_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="nome" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="coincidecomdentrode" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="dentrodepoligono" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="compartilhado" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="eixoprincipal" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="navegabilidade" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="caladomax" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="regime" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="larguramedia" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="velocidademedcorrente" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="profundidademedia" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_trecho_curso_dagua" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="lenght_otf" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="nome"/>
    <constraint exp="" desc="" field="nomeabrev"/>
    <constraint exp="" desc="" field="geometriaaproximada"/>
    <constraint exp="" desc="" field="coincidecomdentrode"/>
    <constraint exp="" desc="" field="dentrodepoligono"/>
    <constraint exp="" desc="" field="compartilhado"/>
    <constraint exp="" desc="" field="eixoprincipal"/>
    <constraint exp="" desc="" field="navegabilidade"/>
    <constraint exp="" desc="" field="caladomax"/>
    <constraint exp="" desc="" field="regime"/>
    <constraint exp="" desc="" field="larguramedia"/>
    <constraint exp="" desc="" field="velocidademedcorrente"/>
    <constraint exp="" desc="" field="profundidademedia"/>
    <constraint exp="" desc="" field="id_trecho_curso_dagua"/>
    <constraint exp="" desc="" field="lenght_otf"/>
  </constraintExpressions>
  <expressionfields>
    <field precision="0" comment="" length="0" typeName="" expression="$length" type="6" name="lenght_otf" subType="0"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns/>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable/>
  <labelOnTop/>
  <widgets/>
  <previewExpression></previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
